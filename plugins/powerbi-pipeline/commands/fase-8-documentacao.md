---
description: Roda só a Fase 8 (documentação e handover) em modo avulso, com o agente documentador-bi.
---

# Fase 8 Avulsa — Documentação

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → despacho → aprovação final → encerramento avulso).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades desta fase:

1. **Agente:** `documentador-bi` (subagente). Fase alvo: Fase 8. Nenhuma pergunta inicial.
2. **Escopo:** sem `$ARGUMENTS`, produzir o conjunto completo em `docs/documentacao/` (documentação funcional, técnica, catálogo de medidas, guia de uso, release notes) + atualização de `docs/dicionario-dados/` e `README.md`. Com `$ARGUMENTS` (ex.: "somente catálogo de medidas"), despachar com escopo parcial — o agente produz apenas os arquivos daquele escopo.
3. **Formatos de saída (D-25, padrão):** a documentação fica **somente na pasta local** do projeto, em três formatos: os `.md` em `docs/documentacao/` (fonte) + `docs/documentacao/html/` (uma página HTML autocontida por `.md` e um `index.html`) + `docs/documentacao/pdf/` (um PDF por `.md`). Depois de escrever/atualizar os `.md`, rodar `python "${CLAUDE_PLUGIN_ROOT}/skills/bi-documentation/scripts/exportar_docs.py" docs/documentacao --titulo "<Cliente> · <Projeto>"` e conferir que o script informa a mesma quantidade de HTML e PDF que de `.md`. HTML e PDF são sempre regenerados a partir dos `.md` — nunca editados à mão. **Não publicar no Notion** nem em outro destino externo, salvo pedido explícito do usuário.
4. QA da Fase 7 (`docs/qa/qa-final.md`) é o insumo preferencial; a ausência não bloqueia — documentar o que existe e registrar a lacuna como pendência.
5. Opcional (perguntar só se o usuário mencionar entrega ao cliente): `.docx` brandado via skill `bi-documentation`, com branding do `PROJECT_CONTEXT.md`.
6. Este agente não altera Power Query, TMDL operacional, PBIR nem DAX — apenas documentação.
