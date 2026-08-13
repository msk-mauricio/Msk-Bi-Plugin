---
description: Roda só a Fase 3 (modelagem dimensional TMDL) em modo avulso, com o agente data-modeler.
---

# Fase 3 Avulsa — Modelagem

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → coleta condicional → despacho → checkpoint a/b → encerramento avulso).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades desta fase:

1. **Agente:** `data-modeler` (subagente). Fase alvo: Fase 3.
2. **Coleta condicional:**
   - Se `powerbi/` **não existe** (greenfield, Passo 0 de scaffolding do agente): o nome técnico vem de `PROJECT_CONTEXT.md` § Projeto; se estiver `<preencher>`, perguntar **aqui** o nome técnico PBIP (sem espaços/acentos, ex.: `VendasVarejo`) antes de despachar. O scaffolding usa o M aprovado em `docs/power-query/` (se houver) nas partitions e cria **apenas** o SemanticModel — o `.Report/` é da Fase 6.
   - Se `powerbi/` existe: revisão do modelo existente, sem pergunta.
3. **Checkpoint a/b obrigatório:** primeira rodada é proposta de modelo (fatos/dimensões, relacionamentos, cardinalidade, riscos); TMDL só é alterado após `Aplicar alterações`, pelo **mesmo subagente** via `SendMessage`.
4. **Validações que permanecem:** sintaxe TMDL antes do handoff final; **D-19** — `dCalendario` marcada como tabela de datas (`dataCategory: Time` + `isKey`), inclusive verificando calendário pré-existente; nomenclatura Dashmaker (D-18) preservando `sourceColumn`; dicionário em `docs/dicionario-dados/`; pendência "refresh test no Power BI Desktop" no `TODO.md`.
5. No encerramento, sugerir `/fase-4-dax` como próximo passo.
