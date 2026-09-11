from app import pipeline


def test_answer_has_citations():
    resp = pipeline.answer("Сколько дней у клиента, чтобы подать претензию?")
    assert resp.citations
    assert resp.citations[0].doc_id == "R-04"
    assert resp.confidence > 0


def test_unknown_topic_returns_clarification():
    resp = pipeline.answer("Перевозите ли вы опасные грузы?")
    assert "уточняется" in resp.answer
    assert resp.confidence == 0.0
    assert resp.citations == []


def test_tracking_number_returns_status():
    resp = pipeline.answer("Где сейчас груз ГЛ-123456?")
    assert "ГЛ-123456" in resp.answer
    assert "прибыл в пункт выдачи" in resp.answer
    assert resp.citations[0].doc_id == "R-08"


def test_tariff_question_quotes_price():
    resp = pipeline.answer("Сколько стоит Стандарт 10 кг по Москве?")
    assert "950 ₽" in resp.answer
    assert resp.citations[0].clause == "3.2"
