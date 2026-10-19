# powerbi-pipeline

Pipeline de desenvolvimento Power BI PBIP/PBIR em 8 fases, com gate de aprovação humana entre cada uma.

## Comandos

| Comando | O que faz |
|---|---|
| `/iniciar-projeto-bi` | Inicia o pipeline guiado completo, com gates |
| `/retomar-projeto-bi` | Retoma a partir do primeiro gate pendente em `TODO.md` |
| `/status-projeto-bi` | Status do projeto (somente leitura, não abre gates) |
| `/fase-1-requisitos` … `/fase-8-documentacao` | Roda uma fase isolada, em modo avulso |
| `/apresentacao-cliente` | Apresentação executiva (fora da numeração de fases) |

## Fases e agentes

| Fase | Agente | Skills principais |
|---|---|---|
| 1 · Requisitos | `analista-requisitos` | `requirements-discovery` |
| 2 · Power Query | `power-query-reviewer` | `power-query-m` |
| 3 · Modelagem | `data-modeler` | `dimensional-modeling`, `tmdl` |
| 4 · DAX | `dax-specialist` | `dax`, `svg-dax`, `html-dax` |
| 5 · Mockup (HTML/SVG) | `html-mockup-designer` | `html-mockup`, `dataviz-powerbi` |
| 6 · Relatório | `pbir-report-builder` | `pbir`, `dataviz-powerbi` |
| 7 · QA | `bi-qa-validator` | `qa-validation`, `desktop-bridge` |
| 8 · Documentação | `documentador-bi` | `bi-documentation` |

Transversais: `orquestrador-bi` (coordenação), `client-presentation`, `gate-protocol`, `process-orchestration`, `fase-avulsa`, `pbip-repository-governance`.

## Dependências opcionais

Degradam com fallback quando ausentes — o pipeline não quebra:

- MCP `powerbi-modeling-mcp` — validação runtime de medidas e refresh
- CLIs `powerbi-desktop` / `powerbi-report-author` — reload, screenshots e validação PBIR (skill `desktop-bridge`)
- Plugin externo `pbip` — skills `pbip:tmdl`, `pbip:pbir-format`, `pbip:pbip-validator`
- MCP Figma: não é mais usado por padrão; só entra na Fase 5 se o usuário pedir explicitamente (D-24)

## Fase 5: mockup em HTML/SVG

O mockup é um HTML autocontido em `docs/mockups/index.html` (uma seção por página, ou um arquivo por página mais o `index.html`), com páginas no tamanho exato da resolução (1280×720 ou 1920×1080), visuais nativos do Power BI nas posições do grid PBIR, gráficos em SVG inline e o tema do cliente. Junto com ele vai o `docs/mockups/mapa-construcao.md` (tema, resolução e, por página, visual, tipo nativo, medidas, campos e x/y/w/h), que a Fase 6 usa para construir o PBIR. Screenshots por página são opcionais. Detalhes na skill `html-mockup`.

## Decisões do kit

Decisões do plugin que os projetos devem copiar para o `DECISIONS.md` (formato de 5 colunas da skill `gate-protocol`):

| Data | Decisão | Contexto | Impacto | Responsável |
|---|---|---|---|---|
| 2026-09-30 | D-24: Mockup da Fase 5 em HTML/SVG autocontido por padrão; Figma só sob pedido (substitui D-03/D-07 como padrão) | Pedido do usuário. O Figma exigia MCP autenticado, esbarrava em cota de escrita e gerava um artefato que a Fase 6 só conferia por screenshot; o HTML/SVG só depende de escrita de arquivo e anota x/y/w/h iguais aos do `mapa-construcao.md`. Alternativas avaliadas: manter Figma como padrão com fallback textual (D-07); manter a skill `figma-mockup` como stub de compatibilidade (rejeitado: competiria com a nova no roteamento de skills) | Agente `figma-mockup-designer` → `html-mockup-designer` e skill `figma-mockup` → `html-mockup` (catálogo de visuais movido junto); Fase 0 sem pré-check do Figma MCP; Gate 5 passa a ser "mockup HTML/SVG aprovado", com evidência = caminho do `index.html` + screenshots opcionais; Fase 6 consome `mapa-construcao.md` e, como referência, `index.html`. Projetos antigos com `figma-url.md`/`mockup.html` continuam aceitos como fallback da Fase 6 | Maurício Saatkamp |
| 2026-10-06 | D-25: Documentação da Fase 8 somente na pasta local, em .md + .html + .pdf (`docs/documentacao/`, `html/`, `pdf/`); HTML/PDF gerados pelo script `skills/bi-documentation/scripts/exportar_docs.py` a partir dos .md. Notion deixa de ser padrão (só sob pedido explícito) | Pedido do usuário. O workspace Notion bateu no limite de blocos do plano gratuito e a sincronização falhava na Fase 8; arquivos locais versionados no repositório servem de entrega e de histórico. PDF via Microsoft Edge headless (padrão no Windows), sem dependência de pandoc/LaTeX | Fase 8 sempre entrega os três formatos; HTML/PDF nunca editados à mão; `.docx` continua opcional | Usuário (Maurício) |
