"""Клиент helpdesk заказчика: статус груза по номеру ГЛ-XXXXXX."""
import logging
import re

import httpx

from app import config

log = logging.getLogger("app.helpdesk")

TRACKING_RE = re.compile(r"ГЛ-\d{6}")

# offline-заглушка для тестов и демо: статус по последней цифре номера
_OFFLINE_STATUSES = {
    "0": "принят на складе",
    "1": "принят на складе",
    "2": "в пути",
    "3": "в пути",
    "4": "в пути",
    "5": "прибыл в пункт выдачи",
    "6": "прибыл в пункт выдачи",
    "7": "выдан",
    "8": "выдан",
    "9": "возврат отправителю",
}


class HelpdeskClient:
    def __init__(self, base_url: str = config.HELPDESK_URL, mode: str = config.HELPDESK_MODE,
                 timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.mode = mode
        self.timeout = timeout

    def get_status(self, tracking: str) -> dict:
        if self.mode == "offline":
            return {"tracking": tracking, "status": _OFFLINE_STATUSES[tracking[-1]]}
        try:
            resp = httpx.get(f"{self.base_url}/shipments/{tracking}/status", timeout=self.timeout)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            log.error("status request failed: %d %s (%s)", e.response.status_code,
                      e.response.reason_phrase, httpx.URL(self.base_url).host)
            raise
        except httpx.RequestError as e:
            log.error("status request failed: %s (%s)", type(e).__name__, httpx.URL(self.base_url).host)
            raise
        return resp.json()
