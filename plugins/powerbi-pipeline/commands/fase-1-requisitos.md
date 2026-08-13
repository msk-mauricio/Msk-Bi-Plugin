---
description: Roda só a Fase 1 (levantamento de requisitos) em modo avulso, com o agente analista-requisitos.
---

# Fase 1 Avulsa — Levantamento de Requisitos

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → coleta condicional → despacho → aprovação final → encerramento avulso).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades desta fase:

1. **Agente:** `analista-requisitos` (subagente). Fase alvo: Fase 1.
2. **Coleta condicional** (cascata de `01-analista-requisitos` § Detecção de entrada — resolver por arquivos antes de perguntar):
   1. Há transcrições em `docs/transcricoes/` (`.txt`, `.md`, `.docx`)? → usar (Ramo A), sem perguntar.
   2. Senão, há `docs/levantamento-requisitos/requisitos-aprovados.md` ou `PRD.md`? → resumir e confirmar reaproveitamento (Ramo B).
   3. Senão, `AskUserQuestion`: `Tenho transcrição em outro caminho` / `Quero responder o questionário guiado` / `Vou colar um resumo livre` / `Cancelar` (Ramos C/D/E — o questionário do Ramo D roda aqui, em blocos, nunca no subagente).
3. **Regra dura:** `docs/levantamento-requisitos/requisitos-aprovados.md` só é gravado **após** o `Aprovar e encerrar` da aprovação final — antes disso o levantamento fica em `levantamento-requisitos.md`.
4. A matriz de rastreabilidade nasce com as colunas Medida DAX / Visual / Página vazias (template `docs/templates/matriz-rastreabilidade-template.md`); quem as preenche são as Fases 4 e 6 (guiadas ou avulsas).
5. No encerramento, sugerir `/fase-2-power-query` ou `/fase-4-dax` (se o modelo já existir) como próximo passo.
