---
name: process-orchestration
description: Skill para orquestrar o ciclo completo de projetos Power BI PBIP/PBIR com gates, TODOs, handoffs, riscos e critérios de aceite.
---

# Skill: Process Orchestration para Power BI PBIP/PBIR

## Quando usar
Use esta skill quando o agente precisar coordenar fases, controlar pendências, definir próximos passos, registrar decisões ou validar passagem entre etapas.

## Objetivo
Garantir que o projeto siga um fluxo controlado, rastreável e auditável, reduzindo alterações aleatórias no modelo, no relatório ou nos requisitos.

## Artefatos controlados
- `TODO.md`
- `DECISIONS.md`
- `CHANGELOG.md`
- `PROJECT_CONTEXT.md`
- `docs/levantamento-requisitos/`
- `docs/handoffs/`
- `docs/qa/`

## Gates obrigatórios

> Numeração canônica — idêntica ao `TODO.md` e ao § Modo Guided Pipeline do `00-orquestrador-bi`.

### Gate 0 — Análise do projeto (gate de modo)
Critérios:
- Os 5 arquivos de governança foram lidos e `powerbi/`/`docs/` inventariados.
- Versionamento git verificado (proposto `git init` se ausente).
- Figma MCP pré-checado (pendência registrada se indisponível).
- CLIs do Desktop Bridge pré-checados (pendência registrada se ausentes — ver `docs/setup-desktop-bridge.md`).
- Resumo de status apresentado e modo escolhido (continuar / recomeçar / cancelar).

### Gate 1 — Requisitos levantados e aprovados
Critérios:
- Transcrições/anotações foram lidas (ou questionário guiado respondido).
- Dores foram identificadas e perguntas de negócio mapeadas.
- KPIs candidatos listados; cada KPI tem fórmula de negócio ou critério de cálculo.
- Cada KPI tem granularidade, dimensão de análise e fonte provável.
- Existe matriz de rastreabilidade (`docs/levantamento-requisitos/matriz-rastreabilidade.md`).
- Pendências para o cliente foram registradas.
- `requisitos-aprovados.md` gravado somente após o "Aprovar" do gate.

### Gate 2a — Power Query diagnosticado
Critérios:
- Consultas críticas foram analisadas.
- Tipos de dados foram validados.
- Etapas pesadas foram identificadas.
- Riscos de query folding foram documentados.
- Impactos no modelo foram listados.

### Gate 2b — Alterações M aplicadas
Critérios:
- Alterações aprovadas no 2a foram aplicadas nas partitions/expressões TMDL (ou documentadas em `docs/power-query/` quando ainda não há `powerbi/`).
- Validação de sintaxe executada e anexada ao gate.
- Validação runtime: refresh executado via Desktop Bridge/MCP e resultado anexado (skill `desktop-bridge`); sem bridge disponível, pendência runtime registrada no TODO.md.

### Gate 3a — Proposta de modelo aprovada
Critérios:
- Fatos e dimensões estão identificados.
- Relacionamentos propostos com cardinalidade e direção de filtro justificadas.
- Tabela calendário foi considerada.
- Chaves técnicas e de negócio foram documentadas.

### Gate 3b — TMDL aplicado
Critérios:
- Tabelas/relacionamentos aplicados em TMDL; dicionário de dados atualizado em `docs/dicionario-dados/`.
- Validação de sintaxe executada e anexada ao gate.
- Validação runtime: PBIP reaberto no Desktop + refresh executado via Desktop Bridge/MCP e resultado anexado (skill `desktop-bridge`); sem bridge disponível, pendência runtime registrada no TODO.md.

### Gate 4a — Matriz de viabilidade aprovada (D-04)
Critérios:
- `docs/dax/matriz-viabilidade.md` gerada com status 🟢/🟡/🔴 por KPI.
- Nenhuma medida criada antes da aprovação da matriz.

### Gate 4b — Medidas criadas
Critérios:
- Medidas derivam de requisitos aprovados (apenas KPIs 🟢/🟡).
- Medidas base foram criadas antes das derivadas.
- Formatação e display folders definidos; medidas relevantes têm descrição.
- Validação de sintaxe executada e anexada ao gate.
- Validação runtime: cada medida nova testada com `EVALUATE {[Medida]}` via MCP (skill `desktop-bridge`); sem bridge disponível, pendência runtime registrada no TODO.md.

### Gate 5 — Mockup Figma aprovado
Critérios:
- Figma MCP verificado antes de iniciar (D-07); fallback textual usado se indisponível.
- URL do arquivo Figma gravada em `docs/mockups/figma-url.md` (ou `docs/mockups/mockup-textual.md` no fallback).
- Screenshots por página em `docs/mockups/screenshots/`.
- `docs/mockups/mapa-construcao.md` presente (no caminho Figma) e coerente com a matriz de viabilidade: cada linha referencia medida 🟢/🟡 e cada elemento do mockup tem linha correspondente.
- Páginas do mockup cobrem os KPIs 🟢/🟡 da matriz de viabilidade.

### Gate 6 — Relatório PBIR implementado
Critérios:
- Páginas respondem perguntas de negócio.
- Visuais usam medidas aprovadas.
- Layout segue o mockup aprovado e boas práticas de DataViz.
- Filtros e navegação foram verificados.
- **`pbip:pbip-validator` executado sem erros antes da aprovação humana (D-06).**
- Se Desktop Bridge disponível: `powerbi-report-author validate` limpo, reload executado com sucesso e screenshots por página capturados em `docs/qa/screenshots-gate6/` e revisados (sem banners de erro, visuais em branco ou slicers vazios) — anexados ao resumo do gate.

### Gate 7 — QA final
Critérios:
- Requisitos, DAX e visuais estão rastreados na matriz de rastreabilidade.
- Não há alteração não documentada.
- Riscos e pendências foram registrados.
- QA visual executada com screenshots quando o Desktop Bridge estiver disponível (seção "QA visual" do relatório).
- Relatório em `docs/qa/qa-final.md` e pendências em `docs/qa/pendencias.md`.

### Gate 8 — Documentação e handover
Critérios:
- Documentação técnica e funcional em `docs/documentacao/`.
- Catálogo de medidas e dicionário de dados atualizados.
- Guia de uso e release notes criados.
- Pendências conhecidas consolidadas para o cliente.

## Handoff de despacho (orquestrador → agente)
Ao despachar um agente de fase, o orquestrador inclui no prompt:

```md
## Handoff de despacho
### Fase e gate alvo
### Resumo do PROJECT_CONTEXT (5 bullets)
### Decisões de DECISIONS.md relevantes à fase
### Pendências herdadas
### Artefatos de entrada (caminhos)
### Handoff da fase anterior: docs/handoffs/fase-(N-1)-handoff.md (se existir)
```

## Regra de handoff entre agentes (agente → orquestrador)
Todo handoff de conclusão deve conter:

```md
## Handoff

### Fase concluída

### Arquivos analisados

### Arquivos alterados

### Decisões registradas

### Pendências

### Riscos

### Contexto essencial para a próxima fase (máx. 10 bullets)

### Próximo agente recomendado
```

## Persistência de handoffs
Ao aprovar o gate final da fase N, o orquestrador grava o handoff em `docs/handoffs/fase-N-handoff.md` (um único arquivo por fase; em fases com sub-gates, gravar após o gate "b"). Handoffs são snapshots imutáveis — nunca editar um handoff já gravado. O agente da fase N+1 recebe o caminho no despacho e o lê antes de reler artefatos extensos.

## Política de alteração
Antes de modificar arquivos, o agente deve produzir:
1. Diagnóstico.
2. Plano.
3. Arquivos afetados.
4. Riscos.
5. Critério de reversão.

Depois de modificar: seguir `gate-protocol` § Encerramento de fase (CHANGELOG → DECISIONS quando houver decisão estrutural → TODO).

## Níveis de prioridade
- **P0 Crítico:** quebra modelo, relatório ou cálculo principal.
- **P1 Alto:** afeta resultado, performance ou entendimento executivo.
- **P2 Médio:** melhora governança, nomenclatura ou manutenção.
- **P3 Baixo:** melhoria estética, documentação ou refinamento.
