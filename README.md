# DPO Vision 

## Descrição do Projeto
O DPO Vision é um módulo avançado de análise de documentos impulsionado por Inteligência Artificial e OCR, projetado para atuar como uma ferramenta interna focada em compliance. O objetivo principal é otimizar as auditorias de conformidade com a LGPD para a DPOnet (https://dponet.com.br), automatizando a leitura, a busca semântica e a marcação visual de termos críticos em contratos e documentos digitalizados, reduzindo drasticamente o tempo de análise manual.

## O Problema
Atualmente, após a emissão de um parecer técnico sobre um contrato por uma pelo DAI, a validação das informações da LGPD exige que o auditor vasculhe o documento inteiro manualmente para encontrar a base daquele parecer ou termos específicos. Esse processo gera um consumo de tempo desnecessário e pouco escalável.

## A Solução
Uma aplicação web onde o auditor faz o upload de contratos (incluindo PDFs escaneados) e define o contexto a ser filtrado. Através de OCR e busca semântica, o sistema processa o arquivo, localiza os trechos relevantes e retorna o documento visualmente grifado na própria tela, além de disponibilizar o download do PDF final com todas as marcações.

## Principais Recursos
- **Processamento de OCR Integrado:** Capacidade de extrair textos de PDFs convencionais e arquivos escaneados.
- **Busca Semântica por Contexto:** Filtro inteligente que entende comandos específicos (ex: "identificar pontos sobre LGPD") utilizando IA, superando buscas simples por palavras-chave.
- **Visualizador de PDF Interativo:** Interface web ágil e responsiva que renderiza as marcações visuais diretamente na tela do usuário.
- **Exportação e Integração:** Função dedicada para baixar o documento processado e visualmente destacado.

##  Tecnologias e Bibliotecas Utilizadas

### Backend & Processamento de Documentos
- **PyMuPDF:** Manipulação de alta performance para ler PDFs, encontrar coordenadas exatas no texto e injetar as marcações visuais (highlights) no arquivo final.
- **Pytesseract (OCR):** Motor integrado para ler e extrair textos de documentos escaneados.

### Dependências

- **Python:** Versão 3.14.4
- **Pymupdf** Versão 2.0
- **Pytesseract** Versão 0.3.13

### Como Rodar

```py
python3 -m venv .venv
source ./venv/bin/activate
pip install -r requirements.txt
```

