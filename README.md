# DPO Vision

O DPO Vision é um backend de apoio à análise de documentos para auditores de privacidade. Ele recebe um PDF e um prompt, reconhece o texto e identifica palavras ou trechos relacionados ao que foi solicitado. O objetivo é ajudar na revisão humana de documentos, sem determinar automaticamente sua conformidade com a LGPD.

## Estado atual

- A API recebe PDFs por upload e executa OCR com Tesseract em todas as páginas, inclusive em PDFs que já possuem texto.
- O texto reconhecido e o prompt são enviados à API do Gemini. O Gemini retorna palavras ou trechos; o backend associa os resultados ao OCR e devolve suas páginas e coordenadas.
- A resposta fornece dados para um frontend desenhar as marcações. O visualizador, a geração de um PDF marcado e o download desse PDF ainda não estão implementados neste repositório.
- A qualidade depende do OCR e da resposta do modelo. O resultado deve ser revisado por uma pessoa.

Mais detalhes sobre o produto e as próximas etapas estão no [PRD](agent/PRD.md).

## Requisitos

- Python e as dependências de [requirements.txt](requirements.txt).
- Tesseract OCR instalado, com os dados do idioma português (`por`) ou de outro idioma configurado.
- Uma chave da API Gemini e acesso ao modelo escolhido.

## Instalação do Tesseract no Windows

1. Acesse a [página do instalador mantido pela UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) e baixe o instalador adequado para seu Windows.
2. Execute o instalador. Na seleção de componentes, inclua os dados do idioma **Portuguese** (`por`), em **Additional language data**, caso ainda não estejam selecionados.
3. Conclua a instalação e anote a pasta escolhida. O caminho normalmente é `C:\Program Files\Tesseract-OCR\tesseract.exe`.
4. No PowerShell, verifique a versão e os idiomas instalados, ajustando o caminho se necessário:

   ```powershell
   & "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
   & "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
   ```

   A lista deve incluir `por`. Se não incluir, execute novamente o instalador e adicione o idioma português.

5. Na configuração do projeto abaixo, informe o caminho do executável em `TESSERACT_CMD` e use `TESSERACT_LANG=por`.

Para outros sistemas, consulte a [documentação de instalação do Tesseract](https://github.com/tesseract-ocr/tessdoc/blob/main/Installation.md).

## Configuração e execução

1. Instale as dependências:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Copie `.env.example` para `.env` caso o arquivo ainda não exista. No PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

3. Edite `.env` conforme sua instalação:

   ```env
   GEMINI_API_KEY=sua-chave
   GEMINI_MODEL=gemini-3.1-flash-lite
   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   TESSERACT_LANG=por
   ```

   Ajuste `TESSERACT_CMD` para o caminho do executável na sua máquina; ele pode ser omitido se o Tesseract estiver no `PATH`. `TESSERACT_LANG` usa `por` por padrão. O modelo do exemplo foi usado com sucesso em um teste, mas a disponibilidade pode variar por chave e ao longo do tempo. Se `GEMINI_MODEL` não estiver definido, o código usa `gemini-2.5-flash`, que pode não estar disponível para sua conta.

   A API carrega o `.env` da raiz na inicialização. Variáveis já definidas no ambiente têm prioridade. O `.env` é ignorado pelo Git; reinicie a API após alterá-lo.

4. Inicie a API:

   ```powershell
   python -m uvicorn api_tesseract:app --reload
   ```

5. Acesse `http://127.0.0.1:8000/docs` para testar a rota.

## API

### `POST /tesseract`

Envie os seguintes campos `multipart/form-data`:

- `arquivo`: PDF a ser analisado.
- `prompt`: texto não vazio descrevendo o que deve ser encontrado.

Exemplo no PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:8000/tesseract -F "arquivo=@contrato.pdf" -F "prompt=Identifique os trechos sobre tratamento de dados pessoais"
```

Exemplo de resposta; os valores de OCR e coordenadas são ilustrativos:

```json
{
  "mensagem": "Arquivo processado.",
  "nome_arquivo": "contrato.pdf",
  "dados": "level\tpage_num\t...\n...",
  "palavras_selecionadas": [
    {
      "id": 1,
      "texto": "dados",
      "pagina": 1,
      "coordenadas": {"x": 100, "y": 200, "largura": 80, "altura": 30},
      "pagina_largura": 2480,
      "pagina_altura": 3508
    }
  ]
}
```

`dados` contém o TSV produzido pelo Tesseract. Os números de `pagina` começam em 1. As coordenadas das palavras são medidas em pixels na imagem da página renderizada para OCR, a 300 DPI, com origem no canto superior esquerdo. O frontend deve escalá-las proporcionalmente às dimensões exibidas e verificar a orientação da página, especialmente em PDFs rotacionados.

O Gemini recebe o texto extraído e o prompt, sem IDs ou coordenadas. O backend compara os trechos retornados com as palavras do OCR, ignorando diferenças entre maiúsculas e minúsculas e pontuação nas bordas. Todas as ocorrências correspondentes são selecionadas; trechos que não correspondam ao texto reconhecido não são marcados. Uma correspondência não atravessa páginas.

A API retorna 400 para PDF inválido ou prompt vazio, 422 para campos obrigatórios ausentes e 503 para falhas do OCR ou do Gemini, incluindo chave ausente. O Gemini pode demorar ou ficar indisponível; o backend não configura atualmente um limite explícito de tempo para a chamada.

O texto extraído e o prompt são enviados ao Google. Avalie o tratamento e as regras de privacidade dos documentos antes de processá-los.

## Organização

O backend usa FastAPI, PyMuPDF, Pytesseract e o SDK do Gemini. O código está organizado em `dpo_vision/domain`, `application`, `infrastructure` e `api`; `api_tesseract.py` é o ponto de entrada para o Uvicorn. O frontend planejado não está neste repositório.
