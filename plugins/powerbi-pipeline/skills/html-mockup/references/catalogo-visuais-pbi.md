# Catálogo de Visuais Power BI para Mockups HTML/SVG

> Referência da skill `html-mockup`. Leia junto com a skill `pbir`, `references/visual-design-system.md` §§1–4 (paleta, tipografia, configuração de página e grid com posições exatas). Este catálogo **não** duplica grid, posições, paleta nem tipografia — a fonte canônica é sempre o design system.

## Bloco A — Visuais permitidos no mockup

Somente visuais nativos que a Fase 6 constrói com os templates do design system (§§5–9). Qualquer elemento do mockup deve ser um destes:

| Visual | Quando usar | Representação fiel no HTML/SVG |
|---|---|---|
| Card (KPI) | valor único | fundo branco, label 12px cinza no topo, valor 28px, accent bar 4px na cor do KPI (design system §8) |
| Barras horizontais | ranking / categorias longas | ordenado descendente, data labels no fim das barras, **sem** eixo de valores, **sem** gridlines |
| Colunas | comparação temporal curta (≤ 13 pontos) | data labels ON + eixo de valores OFF — nunca ambos visíveis |
| Linha | tendência temporal | eixo Y sutil + gridlines sutis, **sem** data labels, sem marcadores (exceto 1 ponto de destaque) |
| Tabela / Matriz | detalhe linha a linha | cabeçalho destacado, tipografia do design system §2 |
| Slicer (dropdown) | filtro de página | 170×55 no header bar, com rótulo do campo filtrado |
| TextBox | título da página | 16px branco sobre o header bar |
| Shape | header bar | retângulo 1280×64 na cor primária da paleta do projeto |

## Bloco B — Tabela de decisão: pergunta de negócio → visual

| Pergunta | Visual |
|---|---|
| Qual o valor de X? | Card |
| Quem são os maiores/menores? (ranking) | Barras horizontais |
| Como X evolui no tempo? (tendência) | Linha |
| Como X se compara entre poucos períodos/categorias? | Colunas |
| Quais os detalhes item a item? | Tabela/Matriz |

## Bloco C — Visuais proibidos no mockup

| Visual | Motivo |
|---|---|
| Gauge / velocímetro | anti-padrão da skill `dataviz-powerbi` (Princípios SWD, item 5); baixa densidade informacional |
| Pie / donut | anti-padrão SWD (item 5) — usar barras horizontais |
| Radar | fora dos templates da Fase 6; leitura difícil |
| Sankey | visual custom (não nativo); a Fase 6 não constrói |
| Word cloud | visual custom; sem valor analítico |
| Efeitos 3D / gradientes / sombras decorativas | clutter (SWD item 2) |
| Infográficos livres / ilustração como dado | não construível em PBIR |
| Sparkline solto fora de tabela | não é visual nativo standalone |

> Exceção: micro-gráficos **dentro** de célula de tabela/matriz ou de cartão (sparkline, barra de progresso, bullet, pill) são construíveis via medida SVG (skill `svg-dax`, D-22) — no mockup, representá-los dentro da tabela/cartão correspondente e registrar no mapa de construção a medida SVG prevista.

Se o cliente pedir um visual proibido: registrar a solicitação como nota no mapa de construção, propor o equivalente permitido (Bloco B) e escalar ao orquestrador para decisão no Gate 5.

## Bloco D — Template do `mapa-construcao.md`

Gravar em `docs/mockups/mapa-construcao.md`, uma seção por página:

```markdown
# Mapa de Construção — <NomeDoProjeto>

> Contrato Fase 5 → Fase 6. Cada linha vira um visual PBIR. Posições em px no canvas da resolução definida no despacho (1280×720 → grid §4; 1920×1080 → grid §4B do design system).

- **Resolução:** 1280×720
- **Tema:** <theme.json do cliente | identidade visual (cores primária/secundária) | paleta padrão do design system>
- **Mockup:** `docs/mockups/index.html`

## Página 1 — <Nome da página> (<pergunta de negócio central>)

| ID | Elemento | Tipo nativo (visualType) | Medida DAX | Campos (categoria/eixo) | x | y | w | h |
|----|----------|--------------------------|------------|--------------------------|---|---|---|---|
| P1-01 | Cards de receita | cardVisual | [Receita Total], [Margem %] | — | 30 | 76 | 600 | 90 |
| P1-02 | Ranking por UF | barChart | [Receita Total] | dGeografia[UF] | 30 | 178 | 600 | 240 |
```

Regras do template:

1. Toda medida citada deve existir com status 🟢 ou 🟡 em `docs/dax/matriz-viabilidade.md`.
2. Toda posição deve vir da tabela "Posições exatas" do design system (§4 ou §4B, conforme a resolução). Desvios exigem nota de justificativa abaixo da tabela da página.
3. Todo visual do HTML (`data-id` = coluna ID, com `data-x/y/w/h` iguais às colunas x, y, w, h) deve ter linha correspondente aqui — e vice-versa.
