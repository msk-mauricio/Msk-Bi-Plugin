---
description: Roda só a Fase 2 (revisão de Power Query) em modo avulso, com o agente power-query-reviewer.
---

# Fase 2 Avulsa — Power Query Review

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → coleta condicional → despacho → checkpoint a/b → encerramento avulso).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades desta fase:

1. **Agente:** `power-query-reviewer` (subagente). Fase alvo: Fase 2.
2. **Coleta condicional** (pré-condição de `02-power-query-reviewer` — resolver por arquivos antes de perguntar):
   1. Há arquivos em `docs/power-query/input/` (`.pq`, `.m`, `.xlsx`, `.txt`, `.png`)? → usar, sem perguntar.
   2. Senão, há partitions em `powerbi/*.SemanticModel/definition/tables/`? → confirmar uso direto das partitions TMDL.
   3. Senão, `AskUserQuestion`: `Vou colar o M aqui` (gravar em `docs/power-query/input/entrada-colada.m`) / `O M está em outro caminho` / `Cancelar`.
3. **Checkpoint a/b obrigatório:** primeira rodada é só diagnóstico (`docs/power-query/auditoria-<AAAA-MM-DD>.md`); alterações em partitions TMDL apenas após `Aplicar alterações`, pelo **mesmo subagente** via `SendMessage`.
4. **Validações que permanecem:** sintaxe TMDL antes do handoff final; nomenclatura Dashmaker (D-18); registro da pendência "refresh test no Power BI Desktop" no `TODO.md` (ou refresh real via Desktop Bridge/MCP, se o Desktop estiver aberto — D-15: escrita só via arquivos).
5. **Greenfield:** sem `powerbi/`, a fase entrega o M validado e documentado em `docs/power-query/`; a materialização em partitions é da Fase 3 (`/fase-3-modelagem` — sugerir no encerramento).
