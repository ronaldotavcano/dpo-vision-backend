import os
from PIL import Image   
import pytesseract
import pymupdf
import json

caminho = r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

os.makedirs("imagens", exist_ok=True)

def pdf_pra_imagem(caminho_completo):
    # Abre usando o caminho completo (ex: arquivos/doc.pdf)
    teste_do_doc = pymupdf.open(caminho_completo)

    matriz_texto = pymupdf.Matrix(300 / 72, 300 / 72)
    imagem = teste_do_doc[0].get_pixmap(matrix=matriz_texto)

    # Extrai só o nome do arquivo para usar nas imagens e no json
    nome_arquivo = os.path.basename(caminho_completo)
    nome_base, _ = os.path.splitext(nome_arquivo)
    
    caminho_imagem = os.path.join("imagens", f"img_{nome_base}.png")
    imagem.save(caminho_imagem)
    teste_do_doc.close()
    
    imagem_pra_texto(caminho_imagem, nome_arquivo)


def imagem_pra_texto(caminho_imagem, nome_arquivo):
    texto = pytesseract.image_to_string(Image.open(caminho_imagem), lang='por')
    dicionario = {nome_arquivo: texto}
    with open("texto.json", "a", encoding="utf-8") as arquivo_json:
        json.dump(dicionario, arquivo_json, ensure_ascii=False, indent=4)


def listar_docs():
    if not os.path.exists("texto.json"):
        print("Nenhum documento processado ainda.\n")
        return
        
    with open("texto.json", "r", encoding="utf-8") as arquivo_json:
        dicionario = json.load(arquivo_json)
        for chave, valor in dicionario.items():
            print(f"Arquivo: {chave}")
            print(f"Texto: {valor}")
            print("\n")