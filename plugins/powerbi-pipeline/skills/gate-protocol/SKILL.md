---
name: gate-protocol
description: Padrão único de gate de aprovação humana entre fases do pipeline BI. Use sempre que um agente concluir uma fase e o orquestrador precisar pedir aprovação ao usuário antes de seguir.
---

# Skill: Gate Protocol

## Quem executa
Gates são **sempre** executados na sessão principal (o orquestrador em modo Guided Pipeline). Subagentes nunca abrem gates: eles devolvem o handoff (resumo + artefatos + riscos) e quem abre o `AskUserQuestion` é a sessão principal, após receber o handoff.

## Quando usar
Sempre que uma fase ou subfase do pipeline termina e é preciso decisão humana para seguir.

## Estrutura obrigatória de um gate (Gates 1–8)

1. **Resumo executivo** (3 a 5 bullets) — o que foi produzido.
2. **Artefatos** — lista de arquivos criados/alterados com caminho.
3. **Riscos e pendências** — itens que ficaram em aberto. Nos gates 2b e 3b: se a validação runtime foi executada via Desktop Bridge (skill `desktop-bridge`), anexar o resultado do refresh; senão, incluir a pendência runtime manual: "executar refresh no Power BI Desktop para validar as alterações".
4. **Validação técnica executada** (comando + resultado) — obrigatório nos gates que alteram TMDL/PBIR (2b, 3b, 4b e 6). No Gate 6, quando o Desktop Bridge estiver disponível, anexar também os screenshots de todas as páginas (`docs/qa/screenshots-gate6/`) ao resumo do gate — a aprovação humana deve ver a renderização real, não só o JSON.
5. **AskUserQuestion** com exatamente estas 3 opções:
   - `Aprovar e seguir para a próxima fase`
   - `Pedir ajustes` (notas: campo livre que volta para o agente)
   - `Pausar projeto`

## Gate 0 — exceção (gate de modo)
A Fase 0 não produz entregável; seu gate usa 3 opções próprias (`Continuar do ponto pendente` / `Recomeçar da Fase 1` / `Cancelar`) e dispensa a lista de artefatos e a validação técnica. É o único gate fora do padrão acima — os Gates 1–8 usam sempre as 3 opções fixas de aprovação.

## Encerramento de fase (Pós-aprovação — ordem obrigatória)

Ao receber "Aprovar", executar **nesta ordem**:

1. Gravar entrada em `CHANGELOG.md` usando o template de `docs/templates/changelog-entry-template.md`, consolidando o trabalho da fase a partir do handoff do agente (**single-writer**: no pipeline guiado, só o orquestrador grava o CHANGELOG — uma entrada por fase, nunca uma do agente e outra do gate).
2. Se houver decisão estrutural, adicionar linha em `DECISIONS.md` no formato de **5 colunas**:
   `| AAAA-MM-DD | <decisão> | <contexto/alternativas> | <impacto> | <agente/pessoa> |`
3. Marcar o checkbox do gate em `TODO.md` como `[x]`, preenchendo as sublinhas do gate:
   - `Aprovado em: <AAAA-MM-DD> por <usuário>`
   - `Artefatos: <caminhos>`
4. Gravar o handoff da fase em `docs/handoffs/fase-N-handoff.md` (formato na skill `process-orchestration`). Em fases com sub-gates (2a/2b, 3a/3b, 4a/4b), gravar uma única vez, após o gate "b".
5. Se o diretório for repositório git, criar commit de checkpoint: `gate-<N>: <resumo curto>`.
6. Anunciar a próxima fase.

## Pós-ajustes
Devolver as notas do usuário ao **mesmo subagente da fase, continuando-o via `SendMessage`** — o contexto dele (arquivos lidos, skills carregadas, diagnóstico) é preservado e a rodada de ajuste fica quase instantânea. Redespachar um subagente novo apenas se o da fase não existir mais (ex.: sessão retomada). Re-executar o gate ao terminar.

## Pós-pausa
Preencher a seção `## Ponto de retomada` do `TODO.md` (Data, Fase/gate atual, Última ação concluída, Próxima ação exata, Notas pendentes do usuário, Arquivos em rascunho) e encerrar a orquestração com a instrução de usar `/retomar-projeto-bi`. Ao retomar, limpar a seção (voltar ao estado "vazio").

## Anti-padrões
- Abrir gate sem os elementos da "Estrutura obrigatória" preenchidos.
- Marcar `[x]` antes de gravar `CHANGELOG.md` (a ordem do Encerramento de fase importa para auditoria).
- Aceitar resposta livre no lugar das 3 opções fixas.
- Abrir `AskUserQuestion` dentro de um subagente (não funciona — gates rodam na sessão principal).
- Editar um handoff já gravado em `docs/handoffs/` (handoffs são snapshots imutáveis).
