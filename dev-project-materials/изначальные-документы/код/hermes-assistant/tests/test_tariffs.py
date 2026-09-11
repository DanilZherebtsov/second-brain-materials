import pytest

from app.tariffs import TARIFFS, find_tariff, quote_price


def test_find_standard():
    assert find_tariff("Сколько стоит Стандарт до Твери?").name == "Стандарт"


def test_find_express():
    assert find_tariff("Посчитайте экспресс, 3 кг").name == "Экспресс"


def test_quote_price_standard_moscow():
    # (690 + 26 × 10) × 1,0
    assert quote_price(TARIFFS["Стандарт"], 10, "moscow") == 950


def test_quote_price_express_cfo():
    # (1 190 + 39 × 5) × 1,3
    assert quote_price("Экспресс", 5, "cfo") == pytest.approx(1800.5)


def test_express_plus_not_confused_with_express():
    assert find_tariff("Сколько стоит Экспресс+ 10 кг по Москве?").name == "Экспресс+"
