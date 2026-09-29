---
name: fase-avulsa
description: Protocolo do modo avulso — rodar uma única fase do pipeline BI fora do fluxo guiado, via comandos /fase-N-*. Use sempre que um comando de fase avulsa for invocado, para coletar insumos, despachar o agente da fase e encerrar com governança mínima sem abrir gates do pipeline.
---

# Skill: Fase Avulsa

Modo de execução para rodar **uma fase isolada** do pipeline BI, sem o fluxo guiado completo.
Ativado pelos comandos `/fase-1-requisitos` … `/fase-8-documentacao` e `/apresentacao-cliente`.
Complementa — não substitui — o pipeline de `/iniciar-projeto-bi` (D-01/D-21): gates e checkboxes
do `TODO.md` continuam pertencendo ao pipeline guiado.

## Quem executa

A **sessão principal**, como mini-orquestrador de fase única. Subagentes não despacham outros
subagentes nem abrem `AskUserQuestion` (D-08) — toda interação com o usuário acontece aqui,
antes do despacho ou nos checkpoints.

## Protocolo (ordem obrigatória)

### 1. Leitura obrigatória
Ler `AGENTS.md`, `PROJECT_CONTEXT.md`, `TODO.md`, `DECISIONS.md` (em chamadas paralelas).
Placeholders `<preencher>` no `PROJECT_CONTEXT.md` **não bloqueiam** o modo avulso — registre a
lacuna no Handoff de despacho como contexto ausente.

#### 1.1 Bootstrap mínimo (arquivos de governança ausentes)
Se **qualquer** um dos quatro arquivos não existir (típico de projeto já em produção, feito fora do
pipeline), esta sessão cria a **versão mínima** dos ausentes **antes do despacho**, sem perguntar e
sem abrir o fluxo guiado. Nunca sobrescrever um arquivo existente.

- `AGENTS.md` — regras do projeto: escrita no modelo só via TMDL versionado (D-15), medidas na tabela
  de medidas do projeto (D-17), nomenclatura Dashmaker (D-18), nunca reordenar `pageOrder` (página nova
  entra no fim), documentos/planilhas são referência e não fonte, commits são do usuário.
- `PROJECT_CONTEXT.md` — § Projeto (cliente, nome, nome técnico PBIP, status: `em produção`/`novo`),
  § Fontes (lidas de `expressions.tmdl`/partições), § Modelo (tabelas fato/dimensão, tabela de medidas),
  § Relatório (páginas na ordem do `pages.json`), § Stakeholders, § Branding. O que não der para inferir
  por `ls`/`Read` fica `<preencher>`.
- `TODO.md` — Gates 0 a 8 **todos `[ ]`** (numeração canônica da skill `process-orchestration`), seção
  `## Pendências` e seção `## Ponto de retomada` **vazia**. Como nenhum gate fica `[x]`, a guarda do
  passo 2 não dispara.
- `DECISIONS.md` — cabeçalho da tabela de 5 colunas (`ID | Data | Decisão | Motivo | Impacto`) e uma
  linha `D-P01` registrando o bootstrap mínimo (projeto pré-existente adotado pelo kit em modo avulso).

Inferir tudo dos arquivos do PBIP (somente leitura). Informar no resumo final quais arquivos foram
criados. Quem quiser o kit completo com gates roda `/iniciar-projeto-bi` depois — ele reaproveita esses
arquivos (passo 5 do comando: se houver `TODO.md`, oferece retomar em vez de recomeçar).

### 2. Guarda de coerência com o pipeline
Se `TODO.md` tiver a seção `## Ponto de retomada` preenchida, **ou** algum gate `[x]` com gates
`[ ]` ainda pendentes, há um pipeline guiado em andamento. Antes de qualquer despacho, abrir
`AskUserQuestion`:
- `Prosseguir em modo avulso` — segue; o encerramento avulso não mexe nos gates.
- `Usar /retomar-projeto-bi` — encerra o comando e orienta a retomada guiada.
- `Cancelar`

Sem pipeline em andamento, **não perguntar nada** neste passo. Com **todos** os gates `[x]`
(pipeline concluído), também não perguntar — apenas informar que se trata de execução cirúrgica
pós-entrega.

### 3. Coleta condicional de insumos
Regra geral: **resolver primeiro pelos arquivos; perguntar só o irresolvível.** Cada comando de
fase define sua cascata específica (transcrições/PRD na Fase 1, input M na Fase 2, tema+resolução
nas Fases 5/6 — D-20h, etc.). `$ARGUMENTS` do comando, quando presente, vira **escopo cirúrgico**
da fase e entra no Handoff de despacho como restrição de escopo.

### 4. Despacho
Despachar o agente da fase (pelo `name` exato do frontmatter) com o **Handoff de despacho** da
skill `process-orchestration` (Fase e gate alvo / Resumo do PROJECT_CONTEXT / Decisões relevantes /
Pendências herdadas / Artefatos de entrada / Handoff da fase anterior se existir), acrescido de:

- `Modo: avulso` — o agente segue seu contrato normal de fase, devolve o handoff no formato
  canônico e **não grava o CHANGELOG** (quem grava é esta sessão, no encerramento).
- Escopo de `$ARGUMENTS`, se houver.
- Handoffs anteriores em `docs/handoffs/` são opcionais ("se existir") — usar
  `fase-(N-1)-handoff.md` (pipeline) ou, na falta dele, `fase-(N-1)-handoff-avulso.md`
  (execução avulsa anterior); sem nenhum dos dois, indicar os artefatos brutos equivalentes
  (ex.: `docs/levantamento-requisitos/`).

### 5. Checkpoint (fases com sub-passos a/b — Fases 2, 3 e 4)
O agente devolve primeiro **diagnóstico/proposta** (equivalente ao sub-gate "a"). Abrir
`AskUserQuestion`:
- `Aplicar alterações`
- `Pedir ajustes` (notas voltam ao **mesmo subagente** via `SendMessage` — D-20a; nunca redespachar)
- `Encerrar sem aplicar` (encerramento avulso registra só o diagnóstico)

Após `Aplicar`, o **mesmo subagente** aplica e devolve o handoff final com a validação de sintaxe
anexada. Fases sem sub-passos (1, 5, 6, 7, 8) vão direto ao passo 6.

### 6. Aprovação final
Apresentar resumo executivo + artefatos + riscos (estrutura herdada do `gate-protocol`, sem tocar
em gates) e abrir `AskUserQuestion`:
- `Aprovar e encerrar`
- `Pedir ajustes` (mesmo subagente via `SendMessage`; repetir este passo ao terminar)
- `Encerrar sem aprovar` (artefatos permanecem como rascunho; registrar como rascunho no CHANGELOG)

### 7. Encerramento avulso (ordem obrigatória)
1. Gravar entrada no `CHANGELOG.md` (template `docs/templates/changelog-entry-template.md`) — no
   modo avulso o single-writer é **esta sessão principal** (D-21), que consolida uma entrada única
   por execução a partir do handoff do agente, com `Agente: <agente da fase> (modo avulso)`.
   O subagente da fase nunca grava o CHANGELOG.
2. Se houver decisão estrutural, linha de 5 colunas em `DECISIONS.md`.
3. `TODO.md`: **não marcar gates `[x]`**. Registrar apenas pendências geradas (ex.: "refresh test
   no Power BI Desktop").
4. **Somente no desfecho `Aprovar e encerrar`** (e, nas Fases 2/3/4, com alterações efetivamente
   aplicadas): gravar o handoff em `docs/handoffs/fase-N-handoff-avulso.md` — caminho próprio do
   modo avulso, que não colide com os snapshots imutáveis do pipeline (`fase-N-handoff.md` é
   exclusivo do encerramento de gate do `gate-protocol`). Uma nova execução avulsa da mesma fase
   pode sobrescrever a versão avulsa anterior. Comandos sem fase numerada (ex.:
   `/apresentacao-cliente`) pulam este passo — o registro fica só no CHANGELOG. Nos desfechos
   `Encerrar sem aplicar`/`Encerrar sem aprovar`, não gravar handoff.
5. Se for repositório git, oferecer commit de checkpoint: `fase-avulsa-<N>: <resumo curto>`;
   comandos sem fase numerada usam `<comando>: <resumo curto>` (ex.:
   `apresentacao-cliente: proposta executiva`). A recusa não bloqueia.
6. Sugerir o próximo passo natural (próximo comando de fase ou `/iniciar-projeto-bi`).

## Validações que o modo avulso NÃO dispensa

Cerimônia de gate é do pipeline; **qualidade técnica não é cerimônia**:

- Sintaxe TMDL validada **após aplicar as edições e antes do handoff final** (Fases 2/3/4) — o
  subagente valida via skill `pbip:tmdl`/CLI e anexa o resultado; o agente `pbip:pbip-validator`,
  quando necessário, é despachado por esta sessão (subagentes não despacham agentes — D-08).
- D-04: matriz de viabilidade **antes** de qualquer medida (Fase 4).
- D-17: medidas sempre na tabela dedicada `Medidas` (Fase 4).
- D-19: `dCalendario` marcada como tabela de datas (Fase 3).
- D-06: `pbip:pbip-validator` limpo **antes da aprovação final** da Fase 6 (nunca abrir a
  aprovação com PBIR não validado), com o resultado anexado ao resumo apresentado ao usuário.
- D-07: pré-check do Figma MCP antes da Fase 5 (fallback: `client-presentation`).
- D-15: escrita no modelo exclusivamente via arquivos TMDL versionados (MCP só leitura/runtime).
- Nomenclatura Dashmaker (D-18) em tudo que for criado.

## Anti-padrões

- Marcar gate `[x]` no `TODO.md` em modo avulso.
- Pular o CHANGELOG porque "foi só uma fase" (execução sem rastro é o principal defeito do kit).
- Perguntar ao usuário algo que um `ls`/`Read` resolveria.
- Redespachar um subagente novo para ajustes quando o da fase ainda existe (D-20a).
- Editar um handoff já existente em `docs/handoffs/`.
- Deixar o subagente da fase interagir com o usuário (não funciona — D-08).
