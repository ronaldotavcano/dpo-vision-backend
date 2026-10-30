# DPO Vision 

## Descrição do Projeto
O DPO Vision é um módulo avançado de análise de documentos impulsionado por Inteligência Artificial e OCR, projetado para atuar como uma ferramenta interna focada em compliance. O objetivo principal é otimizar as auditorias de conformidade com a LGPD para a DPOnet (https://dponet.com.br), automatizando a leitura, a busca semântica e a marcação visual de termos críticos em contratos e documentos digitalizados, reduzindo drasticamente o tempo de análise manual.

## O Problema
Atualmente, após a emissão de um parecer técnico sobre um contrato por uma pelo DAI, a validação das informações da LGPD exige que o auditor vasculhe o documento inteiro manualmente para encontrar a base daquele parecer ou termos específicos. Esse processo gera um consumo de tempo desnecessário e pouco escalável.

## A Solução
Uma aplicação web onde o auditor faz o upload de contratos (incluindo PDFs escaneados) e define o contexto a ser filtrado. Através de OCR e busca semântica, o sistema processa o arquivo, localiza os trechos relevantes e retorna o documento visualmente grifado na própria tela, além de disponibilizar o download do PDF final com todas as marcações.

## Recursos planejados
- **Processamento de OCR Integrado:** Capacidade de extrair textos de PDFs convencionais e arquivos escaneados.
- **Busca Semântica por Contexto:** Filtro inteligente que entende comandos específicos (ex: "identificar pontos sobre LGPD") utilizando IA, superando buscas simples por palavras-chave.
- **Visualizador de PDF Interativo:** Interface web ágil e responsiva que renderiza as marcações visuais diretamente na tela do usuário.
- **Exportação e Integração:** Função dedicada para baixar o documento processado e visualmente destacado.

##  Tecnologias e Bibliotecas Utilizadas

### Frontend planejado (fora deste repositorio)
- **Vue.js:** Construção da interface em formato Saas, simulando como seria o sistema da DPO.
- **Tailwind CSS:** Estilização rápida e responsiva, garantindo que o módulo se integre visualmente aos padrões internos.
- **vue-pdf:** Renderização interativa do contrato e das marcações diretamente no navegador do auditor.

### Backend & Processamento de Documentos (atual e planejado)
- **PyMuPDF:** Manipulação de alta performance para ler PDFs, encontrar coordenadas exatas no texto e injetar as marcações visuais (highlights) no arquivo final.
- **Pytesseract (OCR):** Motor integrado para ler e extrair textos de documentos escaneados.
- **LangChain:** Framework responsável pela busca semântica, processando o contexto desejado pelo auditor com o uso de modelos de linguagem (LLMs).


## Estado e execucao do backend

A API atualmente executa OCR em todas as paginas de um PDF. Busca semantica, destaques, exportacao e frontend sao funcionalidades planejadas; veja [o PRD](agent/PRD.md).

1. Instale Python, o Tesseract OCR e os dados de idioma portugues (`por`).
2. Instale as dependencias: `python -m pip install -r requirements.txt`.
3. Se o Tesseract nao estiver no PATH, defina `TESSERACT_CMD` com o caminho completo do executavel. Defina `TESSERACT_LANG` para outro idioma se necessario (padrao: `por`). No PowerShell, por exemplo: `$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"`.
4. Inicie a API com `python -m uvicorn api_tesseract:app --reload` e acesse `http://127.0.0.1:8000/docs`. Envie um PDF no campo multipart `arquivo` de `POST /tesseract`. A resposta `dados` contem TSV com os numeros das paginas.
O backend e acessado pela API e esta organizado em `dpo_vision/domain`, `application`, `infrastructure` e `api`.
