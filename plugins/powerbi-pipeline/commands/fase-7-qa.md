---
description: Roda só a Fase 7 (QA final) em modo avulso, com o agente bi-qa-validator.
---

# Fase 7 Avulsa — QA

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → despacho → aprovação final → encerramento avulso).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades desta fase:

1. **Agente:** `bi-qa-validator` (subagente). Fase alvo: Fase 7. Nenhuma pergunta inicial — a fase é read-only sobre o que existe no repositório.
2. **Despacho em modo completo** (sem fan-out do pipeline): validação cruzada requisitos × Power Query × modelo × DAX × PBIR × documentação, com gravação de `docs/qa/qa-final.md` (template `docs/templates/qa-final-template.md`) e `docs/qa/pendencias.md`. Se `$ARGUMENTS` definir um escopo parcial (ex.: "somente rastreabilidade"), despachar nesse modo — aí o agente **não grava arquivos** e devolve os achados no handoff.
3. **Critério duro:** toda medida TMDL e todo visual PBIR precisam de linha na matriz de rastreabilidade — ausência é reprovação.
4. Artefatos de fases ausentes (ex.: sem mockup, sem documentação) não bloqueiam: o QA reporta a lacuna como achado, não como erro de execução.
5. O agente atualiza pendências no `TODO.md`; a aprovação final e o CHANGELOG seguem o protocolo da skill `fase-avulsa`.
6. No encerramento, sugerir `/fase-8-documentacao` como próximo passo.
