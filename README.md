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
- **Gemini API:** Analisa o texto extraído e seleciona palavras relevantes para o contexto informado pelo auditor.


## Estado e execucao do backend

A API executa OCR em todas as páginas e envia o texto e o prompt à API do Gemini, que seleciona palavras relevantes. O frontend, a geração de PDF marcado e a exportação ainda são planejados; veja [o PRD](agent/PRD.md).

1. Instale Python, o Tesseract OCR e os dados de idioma portugues (`por`).
2. Instale as dependencias: `python -m pip install -r requirements.txt`.
3. Se o Tesseract nao estiver no PATH, defina `TESSERACT_CMD` com o caminho completo do executavel. Defina `TESSERACT_LANG` para outro idioma se necessario (padrao: `por`). No PowerShell, por exemplo: `$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"`.
4. No arquivo `.env` da raiz do projeto, preencha `GEMINI_API_KEY` com sua chave. Opcionalmente, altere `GEMINI_MODEL` (padrão: `gemini-2.5-flash`). O arquivo `.env.example` serve de modelo e o `.env` não é incluído no Git. Variáveis já definidas no ambiente têm prioridade.
5. Inicie a API com `python -m uvicorn api_tesseract:app --reload` e acesse `http://127.0.0.1:8000/docs`. Envie `arquivo` (PDF) e `prompt` (texto não vazio) como campos multipart de `POST /tesseract`.

A resposta inclui `mensagem`, `nome_arquivo`, `dados` (TSV do Tesseract) e `palavras_selecionadas`. Cada palavra selecionada contém `id`, `texto`, `pagina` (começando em 1), `coordenadas` (`x`, `y`, `largura`, `altura`) e `pagina_largura` e `pagina_altura`. As coordenadas são pixels da imagem renderizada pelo OCR, com origem no canto superior esquerdo; dimensione-as proporcionalmente ao tamanho da página exibida. Considere a orientação da página renderizada e teste a integração com PDFs rotacionados.

O Gemini recebe somente o texto extraído e o prompt, sem IDs ou coordenadas. O backend associa as palavras ou trechos retornados ao OCR e marca todas as ocorrências correspondentes; trechos que o modelo alterar e que não correspondam ao texto extraído não são marcados.

Exemplo de chamada no PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:8000/tesseract -F "arquivo=@contrato.pdf" -F "prompt=Identifique os trechos sobre tratamento de dados pessoais"
```

PDF inválido ou prompt vazio retorna 400; campo obrigatório ausente retorna 422; falha no OCR, configuração ausente ou falha do Gemini retorna 503. O texto extraído e o prompt são enviados ao Google; avalie as regras de privacidade aplicáveis antes de processar documentos reais.
O backend e acessado pela API e esta organizado em `dpo_vision/domain`, `application`, `infrastructure` e `api`.


Notas Mapelli: Configurar o env antes de tentar rodar:

Rodar isso no powershell
$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe" <- Caminho do tesseract na sua máquina
$env:TESSERACT_LANG = "por"

python -m uvicorn api_tesseract:app --reload
