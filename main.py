import processamento
import json
import os
import requests

URL_TESSERACT = "http://127.0.0.1:8000/tesseract"

while True:
    print("Teste de OCR")
    print("\n")
    print("1 - Listar docs")
    print("2 - Processar doc unico")
    print("3 - Processar todos os docs")
    print("4 - Enviar arquivo para a API Tesseract")
    print("5 - Sair")
    opcao = input("Escolha uma opção: ")

    match opcao:
        case "1":
            processamento.listar_docs()
        case "2":
            nome_arquivo = input("Digite o nome do arquivo: ")
            if not nome_arquivo.endswith(".pdf"):
                nome_arquivo = nome_arquivo + ".pdf"
            
            caminho_arquivo = os.path.join("arquivos", nome_arquivo)
            if os.path.exists(caminho_arquivo):
                processamento.pdf_pra_imagem(caminho_arquivo)
                processamento.listar_docs()
            else:
                print(f"O arquivo '{nome_arquivo}' não foi encontrado dentro da pasta 'arquivos'.")
        case "3":
            if os.path.exists("arquivos"):
                for arquivo in os.listdir("arquivos"):
                    if arquivo.lower().endswith(".pdf"):
                        caminho_arquivo = os.path.join("arquivos", arquivo)
                        processamento.pdf_pra_imagem(caminho_arquivo)
                print("Todos os documentos foram processados!")
            else:
                print("A pasta 'arquivos' não existe.")
        case "4":
            nome_arquivo = input("Digite o nome do arquivo (com a extensão): ").strip()
            pasta_arquivos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arquivos")
            caminho_arquivo = os.path.join(pasta_arquivos, nome_arquivo)

            if not os.path.isfile(caminho_arquivo):
                print(f"O arquivo '{nome_arquivo}' não foi encontrado dentro da pasta 'arquivos'.")
                continue

            try:

                with open(caminho_arquivo, "rb") as arquivo:
                    resposta = requests.post(
                        URL_TESSERACT,
                        files={"arquivo": arquivo},
                        timeout=30,
                    )

                resposta.raise_for_status()
                print("Resposta da API:")
                print(json.dumps(resposta.json(), ensure_ascii=False, indent=4))
            except requests.exceptions.ConnectionError:
                print("Não foi possível conectar à API. Inicie-a em outro terminal:")
                print(r".\.venv\Scripts\python.exe -m uvicorn api_ocr.api_tesseract:app --reload")
            except requests.exceptions.RequestException as erro:
                print(f"Erro ao fazer a requisição: {erro}")
            except OSError as erro:
                print(f"Erro ao ler o arquivo: {erro}")
        case "5":
            break
        case _:
            print("Opção inválida. Tente novamente.")
