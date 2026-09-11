"""Счётчики запросов, ответов и латентности для ежедневной сводки в лог."""
import logging
import math
import threading

log = logging.getLogger("app.metrics")


class Metrics:
    def __init__(self):
        self._lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        self.requests = 0
        self.answered = 0
        self.latencies_ms: list[int] = []

    def observe(self, latency_ms: int, answered: bool) -> None:
        with self._lock:
            self.requests += 1
            if answered:
                self.answered += 1
            self.latencies_ms.append(latency_ms)

    def p95_latency_ms(self) -> int:
        if not self.latencies_ms:
            return 0
        data = sorted(self.latencies_ms)
        return data[max(0, math.ceil(0.95 * len(data)) - 1)]

    def daily_summary(self) -> None:
        with self._lock:
            log.info("daily requests=%d answered=%d escalations=0 p95_latency_ms=%d",
                     self.requests, self.answered, self.p95_latency_ms())
            self.reset()


metrics = Metrics()
