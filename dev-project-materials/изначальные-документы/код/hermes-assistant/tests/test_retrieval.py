import pytest

from app import kb_loader, retrieval

DOCS = kb_loader.load_regulations()


def test_all_regulations_loaded():
    assert sorted(DOCS) == [f"R-0{i}" for i in range(1, 9)]


def test_chunk_fixed_keeps_text_and_size():
    text = DOCS["R-04"].text
    chunks = retrieval.chunk_fixed(text, size=400)
    assert all(len(c.text) <= 400 for c in chunks)
    assert "".join(c.text for c in chunks) == text
    assert chunks[0].doc_id == "R-04"


def test_chunk_by_clauses_one_clause_per_chunk():
    chunks = retrieval.chunk_by_clauses(DOCS["R-04"].text)
    assert [c.clause for c in chunks] == [f"4.{i}" for i in range(1, 10)]
    assert all(c.text.startswith(c.clause + ".") for c in chunks)
    assert all(c.title == "Повреждение, недостача и претензии" for c in chunks)


@pytest.mark.parametrize("chunking", ["fixed", "clauses"])
def test_search_finds_damage_regulation(chunking):
    index = retrieval.build_index(DOCS, chunking=chunking)
    hits = index.search("Груз пришёл с повреждением, куда писать претензию?")
    assert hits
    assert hits[0].chunk.doc_id == "R-04"
