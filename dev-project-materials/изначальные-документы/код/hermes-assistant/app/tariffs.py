"""Тарифы «Гермес-Логистики» (регламент R-03) и расчёт стоимости перевозки."""
import re
from dataclasses import dataclass
from typing import Optional, Union


@dataclass(frozen=True)
class Tariff:
    name: str
    base: int      # базовая ставка, ₽
    per_kg: int    # ₽ за килограмм
    days: str      # срок доставки
    clause: str    # пункт R-03


# порядок — как в R-03
TARIFFS = {
    "Эконом": Tariff("Эконом", 450, 18, "5–7 рабочих дней", "3.1"),
    "Стандарт": Tariff("Стандарт", 690, 26, "3–4 рабочих дня", "3.2"),
    "Экспресс": Tariff("Экспресс", 1190, 39, "1–2 рабочих дня", "3.3"),
    "Экспресс+": Tariff("Экспресс+", 1890, 55, "в тот же или на следующий день", "3.4"),
}

# коэффициенты зон (R-03, п. 3.5)
ZONES = {"moscow": 1.0, "cfo": 1.3, "other": 1.6}
ZONE_NAMES = {"moscow": "Москва и МО", "cfo": "ЦФО", "other": "остальные регионы"}

_MOSCOW_RE = re.compile(r"\b(москв|московск|подмосков)|\bмо\b")
# крупные города ЦФО
_CFO_RE = re.compile(
    r"\b(тул|твер|калуг|рязан|ярослав|владимир|воронеж|смоленск|иванов|костром"
    r"|брянск|курск|белгород|липецк|тамбов|орел|орл)"
)


def find_tariff(text: str) -> Optional[Tariff]:
    for name, tariff in TARIFFS.items():
        if name.lower() in text.lower():
            return tariff
    return None


def detect_zone(text: str) -> str:
    t = text.lower().replace("ё", "е")
    if _MOSCOW_RE.search(t):
        return "moscow"
    if _CFO_RE.search(t):
        return "cfo"
    return "other"


def quote_price(tariff: Union[Tariff, str], weight_kg: float, zone: str) -> float:
    """(база + ₽/кг × вес) × коэффициент зоны."""
    t = tariff if isinstance(tariff, Tariff) else TARIFFS[tariff]
    return round((t.base + t.per_kg * weight_kg) * ZONES[zone], 2)
