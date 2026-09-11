"""Поиск по регламентам: чанкинг + BM25 в памяти.

Свой индекс в памяти вместо Elasticsearch: на наших объёмах (до ~5 000 документов)
хватает с запасом, отдельный кластер не нужен (И.М. 12.06).
"""
import logging
import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from app import config
from app.kb_loader import HEADER_RE, Regulation

log = logging.getLogger("app.retrieval")

CLAUSE_RE = re.compile(r"^(\d+\.\d+)\.\s", re.M)

# ниже этого скора считаем, что в базе ничего нет
MIN_SCORE = 3.0

K1 = 1.5
B = 0.75


@dataclass
class Chunk:
    doc_id: str
    title: str
    clause: Optional[str]
    text: str


@dataclass
class Hit:
    chunk: Chunk
    score: float


# ---------- нормализация ----------

_WORD_RE = re.compile(r"[a-zа-я0-9]+")

_STOP = frozenset("""
а без бы был была были быть в вам вас весь все во вот вы где да для до его ее если есть еще
же за и из или им их к как какая какие каким каких какое какой какую ко когда кто куда ли
либо мне можно мы на над надо не нет ни но нужно ну о об он она они оно от по под при про
с сколько со так там то тоже тот ту ты у уже чем что чтобы эта эти это этот я
""".split())

_REFLEXIVE = ("ся", "сь")

# грубый стемминг: отрезаем одно распространённое окончание
_ENDINGS = tuple(sorted((
    "иями", "ями", "ами", "ией", "иям", "иях", "ием", "ого", "его", "ому", "ему", "ыми", "ими",
    "ает", "яет", "еет", "ует", "ают", "яют", "уют", "ать", "ять", "еть", "ить", "аем", "яем",
    "ая", "яя", "ое", "ее", "ые", "ие", "ый", "ий", "ой", "ей", "ом", "ем", "ам", "ям", "ах",
    "ях", "ов", "ев", "ую", "юю", "ых", "их", "ым", "им", "ия", "ию", "ии", "ть",
    "а", "я", "о", "е", "ы", "и", "у", "ю", "ь", "й",
), key=len, reverse=True))


def normalize(text: str) -> str:
    return text.lower().replace("ё", "е")


def stem(word: str) -> str:
    if len(word) <= 4:
        return word
    for r in _REFLEXIVE:
        if word.endswith(r) and len(word) > 5:
            word = word[:-2]
            break
    for end in _ENDINGS:
        if word.endswith(end) and len(word) - len(end) >= 3:
            return word[: -len(end)]
    return word


def tokenize(text: str) -> list[str]:
    return [stem(w) for w in _WORD_RE.findall(normalize(text)) if len(w) > 1 and w not in _STOP]


def topic_of(text: str, max_words: int = 4) -> str:
    """Короткая метка темы запроса для логов."""
    words = [w for w in _WORD_RE.findall(normalize(text)) if len(w) > 2 and w not in _STOP]
    return " ".join(words[:max_words]) or "-"


# ---------- чанкинг ----------

def _header(text: str) -> tuple[str, str]:
    m = HEADER_RE.search(text)
    return (m.group(1), m.group(2)) if m else ("", "")


def chunk_fixed(text: str, size: int = 400) -> list[Chunk]:
    """Режем текст на куски по size символов подряд."""
    doc_id, title = _header(text)
    starts = [(m.start(), m.group(1)) for m in CLAUSE_RE.finditer(text)]
    chunks = []
    for i in range(0, len(text), size):
        piece = text[i:i + size]
        if not piece.strip():
            continue
        # пункт, начало которого попало в кусок; если кусок из середины пункта — None
        clause = next((num for pos, num in starts if i <= pos < i + size), None)
        chunks.append(Chunk(doc_id=doc_id, title=title, clause=clause, text=piece))
    return chunks


def chunk_by_clauses(text: str) -> list[Chunk]:
    """Один чанк = один пункт регламента «X.Y. …» (эксперимент, И.М. 09.07)."""
    doc_id, title = _header(text)
    matches = list(CLAUSE_RE.finditer(text))
    chunks = []
    for j, m in enumerate(matches):
        end = matches[j + 1].start() if j + 1 < len(matches) else len(text)
        chunks.append(Chunk(doc_id=doc_id, title=title, clause=m.group(1),
                            text=text[m.start():end].strip()))
    return chunks


# ---------- индекс ----------

class Index:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self._tokens = [tokenize(c.text) for c in chunks]
        self._tf = [Counter(toks) for toks in self._tokens]
        self._df = Counter(t for toks in self._tokens for t in set(toks))
        self._avgdl = sum(len(t) for t in self._tokens) / max(len(chunks), 1)

    def _idf(self, term: str) -> float:
        n, df = len(self.chunks), self._df[term]
        return math.log(1 + (n - df + 0.5) / (df + 0.5))

    def search(self, query: str, k: int = config.TOP_K) -> list[Hit]:
        terms = set(tokenize(query))
        scored = []
        for i, tf in enumerate(self._tf):
            dl = len(self._tokens[i])
            score = 0.0
            for t in terms:
                f = tf.get(t, 0)
                if not f:
                    continue
                score += self._idf(t) * f * (K1 + 1) / (f + K1 * (1 - B + B * dl / self._avgdl))
            if score > 0:
                scored.append((score, i))
        scored.sort(key=lambda x: (-x[0], x[1]))
        if not scored or scored[0][0] < MIN_SCORE:
            log.warning("empty_result query_topic=%s", topic_of(query))
            return []
        return [Hit(chunk=self.chunks[i], score=round(s, 3)) for s, i in scored[:k]]


def build_index(docs: dict[str, Regulation], chunking: Optional[str] = None) -> Index:
    # TODO: clauses вроде лучше — замерить на eval и включить по умолчанию (И.М. 09.07)
    chunking = chunking or config.CHUNKING
    chunks: list[Chunk] = []
    for doc in docs.values():
        if chunking == "clauses":
            chunks.extend(chunk_by_clauses(doc.text))
        else:
            chunks.extend(chunk_fixed(doc.text, size=config.CHUNK_SIZE))
    log.info("index built chunking=%s docs=%d chunks=%d", chunking, len(docs), len(chunks))
    return Index(chunks)
