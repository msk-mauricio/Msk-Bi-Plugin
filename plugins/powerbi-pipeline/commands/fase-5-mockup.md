---
description: Roda só a Fase 5 (mockup Figma) em modo avulso, com o agente figma-mockup-designer (fallback client-presentation).
---

# Fase 5 Avulsa — Mockup Figma

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → coleta condicional → despacho → aprovação final → encerramento avulso).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades desta fase:

1. **Agente:** `figma-mockup-designer` (subagente). Fase alvo: Fase 5.
2. **Pré-check obrigatório (D-07), antes de qualquer pergunta:** verificar o Figma MCP nesta sessão (tool `whoami`, tipicamente `mcp__plugin_figma_figma__whoami`; carregar via ToolSearch se deferred). Indisponível/não autenticado → informar como resolver (`/mcp`) e oferecer o **fallback**: agente `client-presentation` gera `docs/mockups/mockup-textual.md`.
3. **Coleta condicional (D-20h — subagentes nunca perguntam):** perguntar via `AskUserQuestion`, **aqui**, apenas o que não estiver já registrado (ex.: em `docs/mockups/mapa-construcao.md` de execução anterior): (a) resolução das páginas — `1280×720` ou `1920×1080`; (b) tema/paleta — theme.json ou identidade visual do cliente. Entregar as respostas no Handoff de despacho.
4. **Insumos funcionais:** `docs/levantamento-requisitos/requisitos-aprovados.md` e `docs/dax/matriz-viabilidade.md` (apenas KPIs 🟢/🟡). Sem matriz de viabilidade, o mockup usa a lista de KPIs dos requisitos — registrar o desvio como risco no handoff.
5. **Entregáveis:** `docs/mockups/mapa-construcao.md` (montado **antes** de desenhar — contrato Fase 5 → Fase 6, D-16, com resolução e tema no cabeçalho), arquivo Figma (3–6 frames na resolução definida), `docs/mockups/figma-url.md`, `docs/mockups/screenshots/`.
6. No encerramento, sugerir `/fase-6-relatorio` como próximo passo.
