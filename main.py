import processamento
import json
import os

while True:
    print("Teste de OCR")
    print("\n")
    print("1 - Listar docs")
    print("2 - Processar doc unico")
    print("3 - Processar todos os docs")
    print("4 - Sair")
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
            break
        case _:
            print("Opção inválida. Tente novamente.")