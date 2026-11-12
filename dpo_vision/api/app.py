from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from dpo_vision.application.ocr import AnalyzeDocument
from dpo_vision.domain.errors import InvalidDocumentError, OcrUnavailableError, SemanticSearchUnavailableError
from dpo_vision.infrastructure.gemini import GeminiSemanticSearch
from dpo_vision.infrastructure.ocr import TesseractPdfProcessor

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

app = FastAPI(title="API Tesseract")


def get_processor() -> AnalyzeDocument:
    return AnalyzeDocument(TesseractPdfProcessor(), GeminiSemanticSearch())


@app.post("/tesseract")
async def executar_tesseract(arquivo: UploadFile, prompt: str = Form(...)):
    try:
        if not prompt.strip():
            raise HTTPException(status_code=400, detail="O prompt não pode estar vazio.")
        content = await arquivo.read()
        result, words = await run_in_threadpool(get_processor().execute, content, prompt)
    except InvalidDocumentError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except OcrUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except SemanticSearchUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        await arquivo.close()
    return {"mensagem": "Arquivo processado.", "nome_arquivo": arquivo.filename,
            "dados": result.as_tsv(), "palavras_selecionadas": words}
