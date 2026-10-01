---
description: Roda só a Fase 5 (mockup HTML/SVG autocontido) em modo avulso, com o agente html-mockup-designer.
---

# Fase 5 Avulsa — Mockup (HTML/SVG)

**Execute nesta sessão principal** em modo avulso: invoque a skill `fase-avulsa` e siga o protocolo dela (leitura obrigatória → guarda de coerência → coleta condicional → despacho → aprovação final → encerramento avulso).

Escopo cirúrgico passado pelo usuário (pode estar vazio): `$ARGUMENTS`

Especificidades desta fase:

1. **Agente:** `html-mockup-designer` (subagente, skill `html-mockup`). Fase alvo: Fase 5.
2. **Renderizador (D-24): sempre HTML/SVG autocontido.** Não faça pré-check de Figma e não aborte por Figma indisponível. O entregável é `docs/mockups/index.html` — uma seção por página (ou um arquivo por página mais o `index.html`), autocontido e offline, com páginas no tamanho exato da resolução, visuais em coordenadas absolutas iguais às do mapa (anotadas em `data-x/y/w/h`) e **todo gráfico em SVG inline**. Inclui ajuste à janela por `transform: scale()` mais botão de 100%. Figma **apenas** se o usuário pedir explicitamente nesta execução: o HTML é gerado mesmo assim e a cópia no Figma é feita por esta sessão, a partir do mesmo mapa, depois do handoff.
3. **Coleta condicional (D-20h — subagentes nunca perguntam):** perguntar via `AskUserQuestion`, **aqui**, apenas o que não estiver já registrado (ex.: em `docs/mockups/mapa-construcao.md` de execução anterior): (a) resolução das páginas — `1280×720` ou `1920×1080`; (b) tema/paleta — theme.json ou identidade visual do cliente. Entregar as respostas no Handoff de despacho.
4. **Insumos funcionais:** `docs/levantamento-requisitos/requisitos-aprovados.md` e `docs/dax/matriz-viabilidade.md` (apenas KPIs 🟢/🟡). Sem matriz de viabilidade, o mockup usa a lista de KPIs dos requisitos — registrar o desvio como risco no handoff.
5. **Entregáveis:** `docs/mockups/mapa-construcao.md` (montado **antes** de desenhar — contrato Fase 5 → Fase 6, D-16, com resolução e tema no cabeçalho), `docs/mockups/index.html` (canônico) e `docs/mockups/mockup.md`. Opcional: `docs/mockups/screenshots/pagina-NN.png` (se houver navegador headless). Somente sob pedido explícito: `docs/mockups/figma-url.md`.
6. **Aprovação final:** apresentar o caminho do `index.html` (para o usuário abrir no navegador), os screenshots se houver e o resultado da conferência HTML × mapa.
7. No encerramento, sugerir `/fase-6-relatorio` como próximo passo.
