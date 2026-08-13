---
description: Retoma o pipeline guiado de BI a partir do primeiro gate pendente em TODO.md.
---

# Retomar Projeto BI

**Execute a orquestração nesta sessão principal** (não delegue a orquestração a um subagente — mesmo motivo de `/iniciar-projeto-bi`: gates e despacho de fases só funcionam aqui).

1. Leia `.claude/agents/00-orquestrador-bi.md` e adote o papel de Orquestrador BI (§ Modo Guided Pipeline).
2. Leia `TODO.md`. Primeiro a seção `## Ponto de retomada`: se estiver preenchida, retome exatamente dali (e limpe a seção após retomar). Senão, identifique o primeiro gate `[ ]` pendente e retome a partir dele.
3. Não recomece do zero. Use a skill `gate-protocol` nos gates, sempre nesta sessão.
