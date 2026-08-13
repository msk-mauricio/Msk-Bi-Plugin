---
description: Roda só a Fase 8 (documentação e handover) em modo avulso, com o agente documentador-bi.
---

# Fase 8 Avulsa — Documentação

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → despacho → aprovação final → encerramento avulso).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades desta fase:

1. **Agente:** `documentador-bi` (subagente). Fase alvo: Fase 8. Nenhuma pergunta inicial.
2. **Escopo:** sem `$ARGUMENTS`, produzir o conjunto completo em `docs/documentacao/` (documentação funcional, técnica, catálogo de medidas, guia de uso, release notes) + atualização de `docs/dicionario-dados/` e `README.md`. Com `$ARGUMENTS` (ex.: "somente catálogo de medidas"), despachar com escopo parcial — o agente produz apenas os arquivos daquele escopo.
3. QA da Fase 7 (`docs/qa/qa-final.md`) é o insumo preferencial; a ausência não bloqueia — documentar o que existe e registrar a lacuna como pendência.
4. Opcional (perguntar só se o usuário mencionar entrega ao cliente): `.docx` brandado via skill `bi-documentation`, com branding do `PROJECT_CONTEXT.md`.
5. Este agente não altera Power Query, TMDL operacional, PBIR nem DAX — apenas documentação.
