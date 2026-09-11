"""Замер качества поиска: recall@k на eval/questions.jsonl.

Попадание (hit) — эталонный фрагмент (snippet) целиком лежит хотя бы в одном из top-k чанков.

    python eval/run_eval.py --chunking fixed
    python eval/run_eval.py --chunking clauses --k 3
"""
import argparse
import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import kb_loader, retrieval  # noqa: E402


def load_questions(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="recall@k для чанкинга fixed|clauses")
    parser.add_argument("--chunking", choices=["fixed", "clauses"], default="fixed")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--questions", default=str(ROOT / "eval" / "questions.jsonl"))
    args = parser.parse_args()

    logging.basicConfig(level=logging.ERROR)

    docs = kb_loader.load_regulations()
    index = retrieval.build_index(docs, chunking=args.chunking)
    questions = load_questions(Path(args.questions))

    hits, misses = 0, []
    for q in questions:
        found = index.search(q["q"], k=args.k)
        if any(q["snippet"] in h.chunk.text for h in found):
            hits += 1
        else:
            top = f"{found[0].chunk.doc_id} п.{found[0].chunk.clause}" if found else "ничего"
            misses.append((q, top))

    recall = hits / len(questions) if questions else 0.0
    print(f"chunking={args.chunking}  k={args.k}  чанков={len(index.chunks)}  вопросов={len(questions)}")
    print(f"recall@{args.k} = {recall:.2f}  ({hits}/{len(questions)})")
    if misses:
        print("\nПромахи:")
        for q, top in misses:
            print(f"  - {q['q']}\n    эталон: {q['expected_doc']} п.{q['expected_clause']}"
                  f" «{q['snippet']}»; top-1: {top}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
