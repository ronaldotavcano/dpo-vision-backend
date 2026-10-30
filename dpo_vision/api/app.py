from fastapi import FastAPI, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from dpo_vision.application.ocr import ProcessDocument
from dpo_vision.domain.errors import InvalidDocumentError, OcrUnavailableError
from dpo_vision.infrastructure.ocr import TesseractPdfProcessor

app = FastAPI(title="API Tesseract")


def get_processor() -> ProcessDocument:
    return ProcessDocument(TesseractPdfProcessor())


@app.post("/tesseract")
async def executar_tesseract(arquivo: UploadFile):
    try:
        content = await arquivo.read()
        result = await run_in_threadpool(get_processor().execute, content)
    except InvalidDocumentError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except OcrUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        await arquivo.close()
    return {"mensagem": "Arquivo recebido.", "nome_arquivo": arquivo.filename, "dados": result.as_tsv()}
