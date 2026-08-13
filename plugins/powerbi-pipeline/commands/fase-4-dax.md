---
description: Roda só a Fase 4 (medidas DAX) em modo avulso, com o agente dax-specialist.
---

# Fase 4 Avulsa — Medidas DAX

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → coleta condicional → despacho → checkpoint a/b → encerramento avulso).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades desta fase:

1. **Agente:** `dax-specialist` (subagente). Fase alvo: Fase 4.
2. **Pré-requisito duro do agente:** medidas finais exigem requisito aprovado. Coleta condicional:
   1. Há `docs/levantamento-requisitos/requisitos-aprovados.md` ou matriz de rastreabilidade validada? → seguir, sem perguntar.
   2. Senão, `AskUserQuestion`: `Os requisitos estão em outro caminho` / `Vou colar a lista de KPIs agora` (gravar como `requisitos-aprovados.md` com a nota "aprovação expressa em modo avulso") / `Rodar /fase-1-requisitos primeiro` / `Cancelar`.
3. **Checkpoint a/b obrigatório (D-04):** primeira rodada gera/atualiza `docs/dax/matriz-viabilidade.md` (🟢/🟡/🔴); medidas só após `Aplicar alterações`, pelo **mesmo subagente** via `SendMessage`, e **limitadas aos KPIs 🟢/🟡**.
4. **Validações que permanecem:** **D-17** — toda medida na tabela dedicada `Medidas` (criar na primeira medida do projeto); nomes de negócio com espaço + display folders (D-18); sintaxe TMDL antes do handoff final; se o Desktop estiver aberto, validar cada medida nova com `EVALUATE {[Medida]}` via MCP (senão, pendência runtime no `TODO.md`); atualizar a coluna "Medida DAX" da matriz de rastreabilidade.
5. No encerramento, sugerir `/fase-5-mockup` ou `/fase-6-relatorio` como próximo passo.
