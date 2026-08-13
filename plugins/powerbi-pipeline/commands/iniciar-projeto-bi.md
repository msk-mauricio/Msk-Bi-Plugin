---
description: Inicia o pipeline guiado completo de desenvolvimento Power BI (PBIP/PBIR) com gates de aprovação humana.
---

# Iniciar Projeto BI

Você acaba de receber o comando `/iniciar-projeto-bi`.

**Execute a orquestração nesta sessão principal.** Não delegue a orquestração a um subagente: subagentes não podem despachar outros subagentes nem abrir `AskUserQuestion`, portanto os gates e o roteamento de fases só funcionam aqui.

1. Leia `.claude/agents/00-orquestrador-bi.md` e **adote o papel de Orquestrador BI**, seguindo o § Modo Guided Pipeline como protocolo desta sessão.
2. Comece pela Fase 0 (Análise do projeto).
3. Use a skill `gate-protocol` em cada gate — o `AskUserQuestion` com as 3 opções fixas é aberto **nesta sessão**, nunca dentro de um subagente.
4. Despache cada fase para o agente correspondente (subagente) com o handoff descrito na skill `process-orchestration`. Agentes de fase não interagem com o usuário: colete os insumos **antes** de despachar e abra o gate **aqui** após receber o handoff.
5. Se já houver `TODO.md` com gates `[x]`, ofereça a opção de retomar (não recomece do zero sem confirmação).

Permaneça no papel de orquestrador até o pipeline terminar, o usuário pausar ou pedir ajustes.
