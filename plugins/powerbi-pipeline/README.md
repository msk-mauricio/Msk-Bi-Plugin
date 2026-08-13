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
| 5 · Mockup | `figma-mockup-designer` | `figma-mockup` |
| 6 · Relatório | `pbir-report-builder` | `pbir`, `dataviz-powerbi` |
| 7 · QA | `bi-qa-validator` | `qa-validation`, `desktop-bridge` |
| 8 · Documentação | `documentador-bi` | `bi-documentation` |

Transversais: `orquestrador-bi` (coordenação), `client-presentation`, `gate-protocol`, `process-orchestration`, `fase-avulsa`, `pbip-repository-governance`.

## Dependências opcionais

Degradam com fallback quando ausentes — o pipeline não quebra:

- MCP `powerbi-modeling-mcp` — validação runtime de medidas e refresh
- CLIs `powerbi-desktop` / `powerbi-report-author` — reload, screenshots e validação PBIR (skill `desktop-bridge`)
- Plugin externo `pbip` — skills `pbip:tmdl`, `pbip:pbir-format`, `pbip:pbip-validator`
- MCP Figma — Fase 5
