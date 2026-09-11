"""HTTP API ассистента оператора и статика виджета."""
import contextvars
import logging
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import __version__, config, kb_loader, pipeline
from app.metrics import metrics
from app.schemas import ChatRequest, ChatResponse, RegulationOut

request_id_var = contextvars.ContextVar("request_id", default="-")


class _RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


_handler = logging.StreamHandler()
_handler.addFilter(_RequestIdFilter())
_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s request_id=%(request_id)s %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[_handler])

log = logging.getLogger("app.main")

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("startup version=%s chunking=%s llm_provider=modelapi llm_timeout_s=%s llm_retries=%d",
             __version__, config.CHUNKING, config.LLM_TIMEOUT_S, config.LLM_RETRIES)
    pipeline.get_index()  # грузим регламенты и строим индекс при старте
    yield
    metrics.daily_summary()


app = FastAPI(title="hermes-assistant", version=__version__, lifespan=lifespan)

# виджет открывается из helpdesk заказчика
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    token = request_id_var.set(uuid.uuid4().hex[:8])
    try:
        return await call_next(request)
    finally:
        request_id_var.reset(token)


@app.exception_handler(RequestValidationError)
async def on_validation_error(request: Request, exc: RequestValidationError):
    for err in exc.errors():
        loc = ".".join(str(p) for p in err.get("loc", ()))
        log.warning("RequestValidationError %s: %s", loc, err.get("msg"))
    return await request_validation_exception_handler(request, exc)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    log.info('chat.request session=%s text="%s"', req.session_id, req.message)
    return pipeline.answer(req.message)


@app.get("/api/regulations/{doc_id}", response_model=RegulationOut)
def get_regulation(doc_id: str) -> RegulationOut:
    reg = kb_loader.get_regulation(doc_id)
    if reg is None:
        raise HTTPException(status_code=404, detail=f"Регламент {doc_id} не найден")
    return RegulationOut(doc_id=reg.doc_id, title=reg.title, text=reg.text)


# статика виджета монтируется последней, чтобы не перекрывать API
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="widget")
