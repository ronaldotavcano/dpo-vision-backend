# PRD - DPO Vision

## Problema e publico
Auditores de privacidade da DPOnet precisam localizar evidencias em contratos para conferir pareceres de conformidade com a LGPD. A leitura manual de documentos extensos e digitalizados consome tempo. O produto deve apoiar a analise humana; nao determina conformidade juridica automaticamente.

## Objetivo e resultado esperado
Permitir que o auditor envie um PDF, informe o contexto de analise, examine trechos relevantes no documento e baixe uma copia com destaques. Medir tempo de analise, sucesso do processamento e qualidade dos trechos selecionados com uma amostra avaliada por auditores; metas numericas dependem de uma linha de base.

## Estado atual
O backend oferece OCR em portugues para todas as paginas via `POST /tesseract`. O OCR usa PyMuPDF e Tesseract. Busca semantica, selecao de trechos, destaques, exportacao e visualizador ainda nao estao implementados. O frontend nao esta neste repositorio.

## Jornada e requisitos
1. O auditor envia um PDF legivel ou digitalizado e informa o contexto desejado.
2. O backend extrai texto por pagina, usando OCR quando necessario, preservando posicoes suficientes para relacionar trechos e paginas.
3. Um provedor de busca semantica configuravel identifica trechos relacionados ao contexto e devolve referencias de pagina e coordenadas. O auditor revisa os resultados no visualizador web.
4. O backend gera uma copia PDF com as marcacoes selecionadas e permite seu download. O documento original permanece intacto.
5. Erros de entrada, processamento ou dependencias sao apresentados de modo compreensivel. Dados de documentos devem ter tratamento, acesso e retencao definidos antes de uso em producao.

## Contratos e arquitetura
A API existente aceita `POST /tesseract` com multipart `arquivo` e retorna `mensagem`, `nome_arquivo` e `dados` (TSV Tesseract, com numero de pagina). PDFs invalidos retornam 400; falha ou indisponibilidade do Tesseract retorna 503.

Para as proximas etapas, definir contratos versionados para submissao e resultado do processamento, consulta semantica com identificadores de pagina e coordenadas, selecao de trechos e download do PDF marcado. Esses contratos serao acordados com o frontend antes da implementacao; ainda nao existem rotas para essas funcoes. A porta `SemanticSearchPort` representa a integracao futura, nao um provedor funcional.

A aplicacao separa dominio, casos de uso e portas, infraestrutura e API. A skill aplicada esta em `skills/clean-architecture-python/SKILL.md`; ela orienta dependencias voltadas para o dominio e o uso de portas e adaptadores.

## Criterios de aceitacao
- PDFs de uma ou mais paginas sao processados integralmente; falhas de arquivo ou OCR sao informadas ao cliente.
- O usuario pode consultar um contexto e revisar resultados associados a pagina e a localizacao correta; a qualidade sera avaliada com documentos de referencia e revisores humanos.
- O PDF exportado abre corretamente e contem os destaques selecionados nas paginas correspondentes, sem modificar o original.
- O visualizador externo integra os contratos acordados e oferece acesso ao download.

## Etapas e dependencias
1. Consolidar arquitetura, OCR multipagina, compatibilidade da API e documentacao - iniciado neste repositorio.
2. Definir contratos com o frontend e implementar extracao de texto e coordenadas confiaveis para PDFs nativos e digitalizados.
3. Escolher o provedor semantico, avaliar privacidade, custo e qualidade, implementar o adaptador e avaliar resultados.
4. Implementar marcacao e exportacao e integrar o visualizador web em projeto separado.
5. Validar com auditores, estabelecer metas mensuraveis e preparar a operacao.

## Riscos e decisoes pendentes
Qualidade do OCR depende do documento e do idioma; imagens grandes afetam memoria e tempo de processamento. Dados pessoais podem exigir controles adicionais e regras de retencao. O provedor semantico e suas condicoes de uso ainda nao foram escolhidos; sua integracao deve ser aprovada conforme a politica aplicavel. Autenticacao, limites de upload, persistencia, concorrencia e operacao em producao exigem definicao antes da implantacao.
