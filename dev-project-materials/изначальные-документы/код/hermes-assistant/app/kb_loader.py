"""Загрузка регламентов из kb/regulations/*.md."""
import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

from app import config

log = logging.getLogger("app.kb_loader")

HEADER_RE = re.compile(r"^#\s*(R-\d+)\.\s*(.+?)\s*$", re.M)


@dataclass
class Regulation:
    doc_id: str
    title: str
    text: str


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(config.BASE_DIR).as_posix()
    except ValueError:
        return str(path)


def load_regulations(kb_dir: Optional[Path] = None) -> dict[str, Regulation]:
    kb_dir = Path(kb_dir or config.KB_DIR)
    docs: dict[str, Regulation] = {}
    for path in sorted(kb_dir.glob("*.md")):
        try:
            with open(path, encoding="utf-8", errors="strict") as f:
                text = f.read()
        except UnicodeDecodeError as e:
            log.error(
                "UnicodeDecodeError: '%s' codec can't decode byte 0x%02x in position %d — %s",
                e.encoding, e.object[e.start], e.start, _display_path(path),
            )
            continue
        m = HEADER_RE.search(text)
        if not m:
            log.warning("skip %s: нет заголовка вида '# R-0X. Название'", _display_path(path))
            continue
        docs[m.group(1)] = Regulation(doc_id=m.group(1), title=m.group(2), text=text)
    log.info("kb load: %d/%d regulations loaded (chunking=%s)",
             len(docs), len(list(kb_dir.glob("*.md"))), config.CHUNKING)
    return docs


@lru_cache(maxsize=1)
def get_regulations() -> dict[str, Regulation]:
    return load_regulations()


def get_regulation(doc_id: str) -> Optional[Regulation]:
    return get_regulations().get(doc_id)


def get_clause_text(doc_id: str, clause: str) -> Optional[str]:
    reg = get_regulation(doc_id)
    if reg is None:
        return None
    m = re.search(rf"^{re.escape(clause)}\.\s*(.+)$", reg.text, re.M)
    return m.group(1).strip() if m else None
