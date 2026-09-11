"""Генерация ответа: OfflineLLM (без сети, для тестов и демо) и ModelApiClient (МодельАПИ)."""
import logging
import re

import httpx

from app import config

log = logging.getLogger("app.llm")

SYSTEM_PROMPT = (
    "Ты — помощник оператора поддержки «Гермес-Логистики». Отвечай на «вы», коротко и вежливо, "
    "только по приведённым пунктам регламентов. Если ответа в пунктах нет — напиши «Информация уточняется»."
)

_CLAUSE_NUM_RE = re.compile(r"^\s*\d+\.\d+\.\s*")
_CLEAN_START_RE = re.compile(r"\s*(#|\d+\.\d+\.\s)")
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _first_sentences(text: str, n: int = 2) -> str:
    clean_start = bool(_CLEAN_START_RE.match(text))
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    flat = " ".join(_CLAUSE_NUM_RE.sub("", ln).strip() for ln in lines)
    sentences = [s for s in _SENT_SPLIT_RE.split(flat) if s]
    if not clean_start and sentences:
        if len(sentences) > 1:
            sentences = sentences[1:]  # кусок начался с середины фразы
        else:
            head = sentences[0].split(" ", 1)[-1] if text[:1].isalnum() else sentences[0]
            sentences = ["…" + head]
    return " ".join(sentences[:n])


class OfflineLLM:
    """Детерминированный экстрактивный ответ: 1–2 первых предложения лучшего чанка."""

    def complete(self, question: str, chunks: list) -> str:
        body = _first_sentences(chunks[0].text) if chunks else ""
        return f"Здравствуйте! {body} Если остались вопросы — напишите, пожалуйста.".replace("  ", " ")


class ModelApiClient:
    def __init__(self, url: str = config.MODELAPI_URL, api_key: str = config.MODELAPI_KEY,
                 timeout: float = config.LLM_TIMEOUT_S):
        self.url = url
        self.api_key = api_key
        self.timeout = timeout

    def complete(self, question: str, chunks: list) -> str:
        # TODO: ретраи и fallback на TokenFlow (И.М. 25.06)
        context = "\n\n".join(f"[{c.doc_id} п.{c.clause}] {c.text}" for c in chunks)
        payload = {
            "system": SYSTEM_PROMPT,
            "prompt": f"Пункты регламентов:\n{context}\n\nВопрос клиента: {question}",
            "max_tokens": 400,
            "temperature": 0.1,
        }
        try:
            resp = httpx.post(self.url, json=payload, timeout=self.timeout,
                              headers={"Authorization": f"Bearer {self.api_key}"})
            resp.raise_for_status()
        except httpx.TimeoutException as e:
            log.error("ModelApiClient timeout after %.1fs (attempt 1/%d) — httpx.%s",
                      self.timeout, config.LLM_RETRIES + 1, type(e).__name__)
            raise
        except httpx.HTTPStatusError as e:
            log.error("HTTPStatusError %d %s from МодельАПИ", e.response.status_code,
                      e.response.reason_phrase)
            if e.response.status_code == 429:
                log.error("fallback provider not configured (TOKENFLOW_KEY missing)")
            raise
        return resp.json()["text"].strip()


def get_llm():
    if config.LLM_MODE == "modelapi":
        return ModelApiClient()
    return OfflineLLM()
