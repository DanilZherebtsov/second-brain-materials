"""Ответ оператору: тариф → статус груза → поиск по регламентам."""
import logging
import re
import time
from typing import Optional

import httpx

from app import config, kb_loader, retrieval
from app.helpdesk import TRACKING_RE, HelpdeskClient
from app.llm import get_llm
from app.metrics import metrics
from app.schemas import ChatResponse, Citation
from app.tariffs import TARIFFS, ZONE_NAMES, Tariff, detect_zone, find_tariff, quote_price

log = logging.getLogger("app.pipeline")

NOT_FOUND = "Информация уточняется. Попробуйте переформулировать вопрос."
# TODO: эскалация на старшего смены — ждём от заказчика критерии «сложного» (И.М. 15.07)

TARIFF_WORDS = ("тариф", "стоимость", "сколько стоит")
_TARIFF_MENTION_RE = re.compile(r"(эконом|стандарт|экспресс)\s*(\+|плюс)?", re.I)
_WEIGHT_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*кг", re.I)

# статус из helpdesk → пункт R-08
STATUS_CLAUSES = {
    "принят на складе": "8.2",
    "в пути": "8.3",
    "прибыл в пункт выдачи": "8.4",
    "выдан": "8.5",
    "возврат отправителю": "8.6",
}

_index: Optional[retrieval.Index] = None
_llm = get_llm()
_helpdesk = HelpdeskClient()


def get_index() -> retrieval.Index:
    global _index
    if _index is None:
        _index = retrieval.build_index(kb_loader.get_regulations(), config.CHUNKING)
    return _index


def _title(doc_id: str) -> str:
    reg = kb_loader.get_regulation(doc_id)
    return reg.title if reg else doc_id


def _rub(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ") + " ₽"


def _is_tariff_question(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in TARIFF_WORDS) or any(name.lower() in t for name in TARIFFS)


def _requested_tariff(text: str) -> Optional[str]:
    # как тариф назвал клиент — для разбора жалоб на тарифы
    m = _TARIFF_MENTION_RE.search(text)
    if not m:
        return None
    return m.group(1).capitalize() + ("+" if m.group(2) else "")


def _parse_weight(text: str) -> Optional[float]:
    m = _WEIGHT_RE.search(text)
    return float(m.group(1).replace(",", ".")) if m else None


def _answer_tariff(message: str, tariff: Tariff) -> ChatResponse:
    requested = _requested_tariff(message)
    if requested and requested != tariff.name:
        log.warning("tariff_mismatch requested=%r resolved=%r", requested, tariff.name)
    weight = _parse_weight(message)
    if weight is not None:
        zone = detect_zone(message)
        price = quote_price(tariff, weight, zone)
        text = (f"Здравствуйте! Доставка груза {weight:g} кг по тарифу «{tariff.name}» "
                f"({ZONE_NAMES[zone]}) стоит {_rub(price)}, срок — {tariff.days}.")
    else:
        text = (f"Здравствуйте! Тариф «{tariff.name}»: {_rub(tariff.base)} плюс {tariff.per_kg} ₽ за кг, "
                f"срок — {tariff.days}. Итоговая стоимость зависит от веса и зоны доставки.")
    citation = Citation(doc_id="R-03", title=_title("R-03"), clause=tariff.clause)
    return ChatResponse(answer=text, citations=[citation], confidence=0.9)


def _answer_status(tracking: str) -> ChatResponse:
    try:
        info = _helpdesk.get_status(tracking)
    except httpx.HTTPError:
        return ChatResponse(
            answer=f"Не удалось получить статус груза {tracking}: сервис недоступен. Попробуйте позже.",
            citations=[], confidence=0.0)
    status = str(info.get("status", "")).strip()
    clause = STATUS_CLAUSES.get(status.lower(), "8.7")
    hint = kb_loader.get_clause_text("R-08", clause) or ""
    text = f"Здравствуйте! Груз {tracking} сейчас в статусе «{status}». {hint}".strip()
    citation = Citation(doc_id="R-08", title=_title("R-08"), clause=clause)
    return ChatResponse(answer=text, citations=[citation], confidence=0.95)


def _answer_from_kb(message: str) -> ChatResponse:
    hits = get_index().search(message, k=config.TOP_K)
    if not hits:
        return ChatResponse(answer=NOT_FOUND, citations=[], confidence=0.0)
    best = hits[0]
    if best.chunk.clause is None:
        log.warning("answer_without_citation topic=%s", retrieval.topic_of(message))
    citations, seen = [], set()
    for h in hits:
        key = (h.chunk.doc_id, h.chunk.clause)
        if key in seen:
            continue
        seen.add(key)
        citations.append(Citation(doc_id=h.chunk.doc_id, title=h.chunk.title, clause=h.chunk.clause))
    text = _llm.complete(message, [h.chunk for h in hits])
    confidence = round(min(0.95, best.score / (best.score + 4.0)), 2)
    return ChatResponse(answer=text, citations=citations, confidence=confidence)


def answer(message: str) -> ChatResponse:
    started = time.perf_counter()
    tariff = find_tariff(message) if _is_tariff_question(message) else None
    tracking = TRACKING_RE.search(message)
    if tariff:
        resp = _answer_tariff(message, tariff)
    elif tracking:
        resp = _answer_status(tracking.group(0))
    else:
        resp = _answer_from_kb(message)
    resp.latency_ms = int((time.perf_counter() - started) * 1000)

    answered = resp.confidence > 0
    if answered:
        top = resp.citations[0] if resp.citations else None
        log.info("answered doc=%s clause=%s confidence=%.2f latency_ms=%d",
                 top.doc_id if top else None, top.clause if top else None,
                 resp.confidence, resp.latency_ms)
    metrics.observe(resp.latency_ms, answered)
    return resp
