---
description: Gera a apresentação executiva para o cliente em modo avulso, com o agente client-presentation.
---

# Apresentação para Cliente (avulsa)

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → coleta condicional → despacho → aprovação final → encerramento avulso). Este comando não corresponde a uma fase numerada — é o papel primário do agente `client-presentation` (ele não participa da Fase 5, cujo mockup é HTML/SVG do `html-mockup-designer` — D-24).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades:

1. **Agente:** `client-presentation` (subagente), em **modo apresentação**: gera `docs/apresentacoes-cliente/proposta-executiva.md` e `docs/apresentacoes-cliente/narrativa-valor.md` (template `docs/templates/proposta-dashboard-template.md`). Deixar explícito no despacho que não é para gerar mockup (nem `mockup-textual.md`): o mockup visual é da Fase 5.
2. **Coleta condicional:** o insumo é o levantamento de requisitos (`docs/levantamento-requisitos/`). Se não existir, `AskUserQuestion`: `Os requisitos estão em outro caminho` / `Vou colar um resumo do projeto` / `Rodar /fase-1-requisitos primeiro` / `Cancelar`.
3. O agente não altera PBIP/PBIR/TMDL, Power Query nem DAX.
4. Na aprovação final, revisar KPIs propostos e próximos passos com o cliente antes de encerrar.
5. **Sem fase numerada:** no encerramento avulso não há handoff de fase (o registro fica só no `CHANGELOG.md`) e o commit opcional usa `apresentacao-cliente: <resumo curto>`.
