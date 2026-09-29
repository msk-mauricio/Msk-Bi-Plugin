---
description: Roda só a Fase 6 (relatório PBIR) em modo avulso, com o agente pbir-report-builder.
---

# Fase 6 Avulsa — Relatório PBIR

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → coleta condicional → despacho → aprovação final → encerramento avulso).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades desta fase:

1. **Agente:** `pbir-report-builder` (subagente). Fase alvo: Fase 6.
2. **Coleta condicional (D-20h — o agente devolve o handoff se faltar):** tema e resolução (`1280×720` ou `1920×1080`). Resolver na ordem: cabeçalho de `docs/mockups/mapa-construcao.md` → handoff da Fase 5 → `AskUserQuestion` **aqui**. Nunca despachar sem os dois resolvidos.
3. **Referência de layout, em ordem de fallback:** `docs/mockups/mapa-construcao.md` (fonte primária — construir a partir dele, sem interpretar imagem) → `docs/mockups/mockup.html` (render HTML+SVG da Fase 5; ler o HTML, não interpretar screenshot) → `figma-url.md` + `screenshots/` (projetos antigos) → `mockup-textual.md` → `docs/apresentacoes-cliente/proposta-executiva.md`. Sem nenhum deles, confirmar com o usuário o layout desejado antes de despachar.
4. **Insumos técnicos:** medidas aprovadas no TMDL (`powerbi/*.SemanticModel/definition/tables/`) — o agente lê, nunca modifica; cria o shell `.Report/` se não existir.
5. **Validação obrigatória antes de encerrar (D-06):** despachar o agente `pbip:pbip-validator` sobre `powerbi/` **nesta sessão** e só abrir a aprovação final com validação limpa. Com Desktop Bridge disponível, anexar screenshots das páginas (`docs/qa/screenshots-gate6/`) ao resumo.
6. **Rastreabilidade:** colunas "Visual" e "Página" da matriz de rastreabilidade atualizadas — visual sem linha na matriz é falha de QA.
7. No encerramento, sugerir `/fase-7-qa` como próximo passo.
