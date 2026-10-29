
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/tesseract files={"arquivo": arquivo_aberto}.


from fastapi import FastAPI, UploadFile
from PIL import Image   
import pytesseract
import pymupdf
import json
import io

caminho = r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

app = FastAPI(title="API Tesseract")


@app.post("/tesseract")
async def executar_tesseract(arquivo: UploadFile):
    
    conteudo = await arquivo.read()

    doc = pymupdf.open(stream=conteudo, filetype="pdf")

    matriz = pymupdf.Matrix(300 / 72, 300 / 72)
    imagem = doc[0].get_pixmap(matrix=matriz)

    imagem_pil = Image.open(io.BytesIO(imagem.tobytes("png")))

    data = pytesseract.image_to_data(imagem_pil, lang='por')


    return {
        "mensagem": "Arquivo recebido.",
        "nome_arquivo": arquivo.filename,
        "dados": data
    }
