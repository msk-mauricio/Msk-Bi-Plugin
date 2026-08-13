# Visual Design System — Padrão para Páginas PBIR

Este arquivo é a **fonte de verdade** para criação de novas páginas e visuais no formato PBIR.
Sempre que o usuário pedir para criar uma página, gráfico, card ou qualquer visual,
use os templates e configurações abaixo como base.

> **Projeto de referência:** os valores exatos deste arquivo foram extraídos do relatório ValeVerdeBI
> (5 páginas: 4 em 1280×720 + 1 exemplo em 1920×1080), que é o padrão visual aprovado do kit.

---

## 0. Perguntas obrigatórias ANTES de gerar páginas/visuais

Antes de gerar qualquer página ou conjunto de visuais, **sempre pergunte ao usuário** (via `AskUserQuestion` quando disponível):

1. **"O relatório tem tema (custom theme JSON)?"**
   - **Tem tema** → use as **cores do tema**: `ThemeDataColor` para preenchimentos (ex.: tile do cardVisual), `dataColors` do tema para séries, e as cores estruturais (`background`, `foreground`, `tableAccent`) para os demais elementos. A paleta da §1 vira apenas fallback.
   - Como verificar: `definition/report.json` → `themeCollection.customTheme`, e o arquivo JSON correspondente em `StaticResources/RegisteredResources/`.
   - **Não tem tema** → use a paleta da §1 e ofereça criar o tema (§10).
2. **"Página em 1280×720 ou 1920×1080?"**
   - **1280×720** → grid da §4 (padrão).
   - **1920×1080** → grid da §4B (posições e fontes maiores — não basta escalar ×1.5 cegamente; use os valores da tabela).

Não pule essas duas perguntas nem assuma resposta — elas mudam posições, fontes e cores de todos os templates abaixo.

---

## 1. Paleta de Cores

| Token | Hex | Uso |
|-------|-----|-----|
| GREEN_DARK | `#1A3C34` | Header bar, títulos de gráfico, accent bar de card |
| GREEN_MID | `#2E7D32` | Cor primária: barras de gráfico, linhas, accent bar principal |
| GREEN_LIGHT | `#558B2F` | Variação verde: 4ª cor de dados, accent bar alternativo |
| GREEN_SOFT | `#81C784` | Verde suave para backgrounds ou 4ª série |
| GREEN_PALE | `#A5D6A7` | Verde claro para áreas de destaque |
| ORANGE_ACC | `#F57C00` | Cor de destaque: cancelamentos, alertas, 2ª série |
| ORANGE_LIGHT | `#FFB74D` | Laranja suave para variações |
| BG_PAGE | `#F4F6F5` | Fundo da página (cinza muito claro) |
| WHITE | `#FFFFFF` | Fundo dos cards e visuais |
| TEXT_DARK | `#1A1A1A` | Texto principal |
| TEXT_GRAY | `#757575` | Texto secundário, labels, eixos |
| BORDER_COL | `#E0E4E2` | Bordas de visuais |
| SHADOW_COL | `#B0BEC5` | Cor da sombra |
| GRIDLINE | `#EEEEEE` | Linhas de grade dos gráficos |

### Ordem de cores para séries de dados (dataColors)
```json
["#2E7D32", "#F57C00", "#558B2F", "#81C784", "#1A3C34", "#A5D6A7", "#F57C00", "#FFB74D"]
```

---

## 2. Tipografia

> Sufixos `L` (inteiro) e `D` (decimal) são apenas o tipo do literal JSON — o valor é sempre em **pontos** (9L = 9pt).
> A coluna "1920×1080" mostra o tamanho equivalente na página grande (§4B); demais valores valem para 1280×720.

| Classe | Fonte | 1280×720 | 1920×1080 | Cor | Uso |
|--------|-------|----------|-----------|-----|-----|
| Callout (valor do card) | wf_standard-font, helvetica, arial, sans-serif | 22L | 26D | (herdado) | Valor principal do cardVisual |
| Title (título de gráfico) | Segoe UI Semibold | 10D | 14D | #1A3C34 | Título dentro do visualContainerObjects |
| Header (cabeçalho da página) | Segoe UI Semibold | 16px | 24pt | #FFFFFF | TextBox no header bar (textRuns usa unidade explícita) |
| Label (label do card) | Segoe UI | 9L | 14D | #757575 | Label do cardVisual |
| Eixos de gráfico | (herdado do tema) | 9D | 9–10D | (herdado) | categoryAxis, valueAxis |
| Data labels | (herdado do tema) | 9D | 9D | #757575 | Nos gráficos de barra |
| Tabelas (tableEx) | (herdado do tema) | 9D | 10D | #1A1A1A | columnHeaders e values |
| Slicer header | Segoe UI | 9L | 11D | #1A1A1A | Cabeçalho do slicer |
| Slicer items | Segoe UI | 9L | 11D | #1A1A1A | Itens do dropdown |

---

## 3. Configuração da Página

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
  "name": "<PAGE_HEX_ID>",
  "displayName": "<Nome da Página>",
  "displayOption": "FitToPage",
  "height": 720,
  "width": 1280,
  "objects": {
    "background": [{
      "properties": {
        "color": { "solid": { "color": { "expr": { "Literal": { "Value": "'#F4F6F5'" } } } } },
        "transparency": { "expr": { "Literal": { "Value": "0D" } } }
      }
    }]
  }
}
```

---

## 4. Grid de Layout Padrão (1280 × 720)

```
┌──────────────────────────────────────────────────────────────────┐
│ HEADER BAR (shape verde)  TextBox 16px    [Slicer Ano][Slicer Mês]│ y:0   h:64
├──────────────────────────────────────────────────────────────────┤
│ CARD STRIP — 1 único cardVisual com N tiles (2 a 6 KPIs)         │ y:76  h:90
├────────────────────────────────┬─────────────────────────────────┤
│ Visual sup. esquerdo (606w)    │ Visual sup. direito (605w)      │ y:178 h:240
├────────────────────────────────┼─────────────────────────────────┤
│ Visual inf. esquerdo (606w)    │ Visual inf. direito (605w)      │ y:430 h:275
└────────────────────────────────┴─────────────────────────────────┘
```

### Posições exatas

| Elemento | x | y | width | height | z |
|----------|---|---|-------|--------|---|
| Header bar (shape) | 0 | 0 | 1280 | 64 | 0 |
| TextBox título | 30 | 14 | 580 | 42 | 11000 |
| Slicer Ano | 900 | **3** | 170 | **57** | 10000 |
| Slicer Mês | 1085 | **3** | 170 | **57** | 9000 |
| Card strip (1 cardVisual multi-tile) | 30 | 76 | 1225 | 90 | 5000–8000 |
| Visual sup. esquerdo | 30 | 178 | 606 | 240 | 1000–4000 |
| Visual sup. direito | 651 | 178 | 605 | 240 | 1000–4000 |
| Visual inf. esquerdo | 30 | 430 | 606 | 275 | 1000–4000 |
| Visual inf. direito | 651 | 430 | 605 | 275 | 1000–4000 |

### Convenção de z-order (usar sempre)

`shape header = 0` → `gráficos/tabelas = 1000–4000` → `cardVisual = 5000–8000` → `slicers = 9000–10000` → `textbox título = 11000`.

### Margem padrão
- Margem esquerda/direita: **30px**
- Gap entre gráficos: **~15px** (coluna esquerda termina em x=636, direita começa em x=651)
- Cards: o gap entre tiles é interno ao cardVisual (`cellPadding: 15`), não há gap de posicionamento

### Quantidade variável de visuais (3, 5, …)

O padrão é 2×2, mas a quantidade de gráficos varia conforme o projeto:

- **3 visuais** → 2 na linha superior (y=178, h=240) + 1 em **largura total** na linha inferior (x=30, y=430, w=1226, h=275) — padrão usado na página "Financeiro e Logística" do projeto de referência.
- **5+ visuais** → mantenha as duas linhas e divida uma delas em 3 colunas (w≈398 cada, gaps de ~15px), priorizando a linha inferior para o detalhamento.
- Nunca deixe "buracos" no grid: um visual sozinho numa linha ocupa a largura total (w=1226).

---

## 4B. Grid de Layout 1920 × 1080

Página de exemplo "1920 x 1080" do projeto de referência. **Não é uma escala ×1.5 cega** — use os valores abaixo.

### Posições exatas

| Elemento | x | y | width | height | z |
|----------|---|---|-------|--------|---|
| Header bar (shape) | 0 | 0 | 1920 | 104 | 0 |
| TextBox título (24pt) | 30 | 25 | 708 | 66 | 11000 |
| Slicer Ano | 1527 | 14 | 172 | 78 | 10000 |
| Slicer Mês | 1713 | 14 | 185 | 78 | 9000 |
| Card strip (1 cardVisual multi-tile) | 22 | 122 | 1878 | 128 | 5000–8000 |
| Visual sup. esquerdo | 22 | 265 | 928 | 390 | 1000–4000 |
| Visual sup. direito | 968 | 265 | 930 | 390 | 1000–4000 |
| Visual inf. esquerdo | 22 | 673 | 928 | 390 | 1000–4000 |
| Visual inf. direito | 970 | 673 | 928 | 390 | 1000–4000 |

### Fontes na página 1920×1080 (o que muda vs. 1280×720)

| Elemento | 1280×720 | 1920×1080 |
|---|---|---|
| TextBox do header | `"16px"` | `"24pt"` |
| Título de visual (`title.fontSize`) | 10D | **14D** |
| tableEx `columnHeaders`/`values` | 9D | **10D** |
| `categoryAxis` | 9D | **10D** |
| `valueAxis` / data labels | 9D | 9D |
| Slicer `header`/`items` | 9L | **11D** |
| cardVisual `value` | 22L | **26D** |
| cardVisual `label` | 9L | **14D** |

Todo o resto (cores, bordas 8px, sombra, paddings de contêiner 14/16/16/16, padrões SWD) permanece idêntico ao 1280×720.

---

## 5. Template: Header Bar (Shape)

⚠️ **REGRA CRÍTICA para shapes:** A cor visível de uma shape vem EXCLUSIVAMENTE do `visualContainerObjects.background.color`. Os objects internos `fill` e `outline` devem ter `show: false`. Se você usar `fill.fillColor`, o Power BI ignora e renderiza a cor padrão do tema (geralmente roxa). Isso é um bug comum — a cor da shape é controlada pelo container, não pelo fill interno.

Cor do header no projeto de referência: `#2F6848`. **Se o relatório tiver tema, derive a cor do header do tema** (cor primária escura) em vez de fixar esse hex. Em página 1920×1080, use `height: 104`.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.8.0/schema.json",
  "name": "<HEX_ID>",
  "position": { "x": 0, "y": 0, "z": 0, "height": 64, "width": 1280 },
  "visual": {
    "visualType": "shape",
    "objects": {
      "fill": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}}],
      "outline": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}}]
    },
    "visualContainerObjects": {
      "background": [{"properties":{"show":{"expr":{"Literal":{"Value":"true"}}},"color":{"solid":{"color":{"expr":{"Literal":{"Value":"'#2F6848'"}}}}},"transparency":{"expr":{"Literal":{"Value":"0L"}}}}}],
      "border": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}}]
    },
    "drillFilterOtherVisuals": true
  }
}
```

---

## 6. Template: TextBox (Título da Página)

⚠️ **REGRA CRÍTICA para textbox:** O campo `paragraphs` deve ser um **array nativo de objetos JSON**, NÃO uma string JSON encodada dentro de `expr.Literal`. Se você usar `{"expr":{"Literal":{"Value":"[{...}]"}}}`, o Power BI não consegue parsear e renderiza o textbox vazio. O formato correto é `"paragraphs": [{"textRuns": [...]}]` — array direto, sem wrapper de expressão.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.8.0/schema.json",
  "name": "<HEX_ID>",
  "position": { "x": 30, "y": 14, "z": 11000, "height": 42, "width": 580 },
  "visual": {
    "visualType": "textbox",
    "objects": {
      "general": [{"properties":{
        "paragraphs": [{"textRuns":[{"value":"<TÍTULO DA PÁGINA>","textStyle":{"fontFamily":"Segoe UI Semibold","fontSize":"16px","fontWeight":"bold","color":"#FFFFFF"}}]}]
      }}]
    },
    "visualContainerObjects": {
      "background": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}}]
    },
    "drillFilterOtherVisuals": true
  }
}
```

Em página **1920×1080**: `position { "x": 30, "y": 25, "z": 11000, "height": 66, "width": 708 }` e `fontSize: "24pt"` no textStyle.

---

## 7. Template: Slicer (Dropdown)

⚠️ **REGRA CRÍTICA de altura/posição do slicer em 1280×720:** No header bar, os slicers ficam em **y = 3** com **altura máxima de 57px** (57 é o padrão; nunca ultrapasse). Quando o header do slicer está visível (`header.show: true`), a altura mínima deve ser **55px** — com `height: 40`, o Power BI não consegue renderizar o título + o dropdown juntos (o título fica cortado ou o dropdown some). Use `height: 40` APENAS se `header.show: false` (slicer sem título).

| header.show | height | y | Uso |
|-------------|--------|---|-----|
| `true` | **55–57 (máx. 57)** | **3** | Padrão — slicer com título visível no header bar 1280×720 |
| `false` | 40 | 3 | Slicer compacto sem título |

Em página **1920×1080**: `y: 14`, `height: 78`, `width: 172–185` (Ano em x=1527, Mês em x=1713), fontes `header`/`items` em **11D**.

**Sincronização entre páginas (padrão do kit):** todo slicer de Ano/Mês replica em todas as páginas com o mesmo `syncGroup` (`SyncAno` / `SyncMes`), com `fieldChanges` e `filterChanges` `true` — ver bloco no template abaixo.

**Pré-seleção opcional:** para abrir o relatório já filtrado (ex.: ano corrente), adicione em `objects.general.filter` um filtro `In` sobre a coluna do slicer (padrão usado no slicer de Ano do projeto de referência).

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.8.0/schema.json",
  "name": "<HEX_ID>",
  "position": { "x": "<X>", "y": 3, "z": 9000, "height": 57, "width": 170 },
  "visual": {
    "visualType": "slicer",
    "query": {
      "queryState": {
        "Values": {
          "projections": [{
            "field": { "Column": { "Expression": { "SourceRef": { "Entity": "<ENTIDADE>" } }, "Property": "<COLUNA>" } },
            "queryRef": "<ENTIDADE>.<COLUNA>",
            "nativeQueryRef": "<COLUNA>",
            "active": true
          }]
        }
      }
    },
    "objects": {
      "data": [{"properties":{"mode":{"expr":{"Literal":{"Value":"'Dropdown'"}}}}}],
      "header": [{"properties":{
        "show":{"expr":{"Literal":{"Value":"true"}}},
        "fontFamily":{"expr":{"Literal":{"Value":"'Segoe UI'"}}},
        "textSize":{"expr":{"Literal":{"Value":"9L"}}},
        "fontColor":{"solid":{"color":{"expr":{"Literal":{"Value":"'#1A1A1A'"}}}}}
      }}],
      "selection": [{"properties":{"selectAllCheckboxEnabled":{"expr":{"Literal":{"Value":"true"}}}}}],
      "items": [{"properties":{
        "textSize":{"expr":{"Literal":{"Value":"9L"}}},
        "fontColor":{"solid":{"color":{"expr":{"Literal":{"Value":"'#1A1A1A'"}}}}}
      }}]
    },
    "visualContainerObjects": {
      "dropShadow": [{"properties":{
        "show":{"expr":{"Literal":{"Value":"true"}}},
        "color":{"solid":{"color":{"expr":{"Literal":{"Value":"'#B0BEC5'"}}}}},
        "preset":{"expr":{"Literal":{"Value":"'Custom'"}}},
        "shadowSpread":{"expr":{"Literal":{"Value":"0L"}}},
        "shadowBlur":{"expr":{"Literal":{"Value":"8L"}}},
        "angle":{"expr":{"Literal":{"Value":"90L"}}},
        "shadowDistance":{"expr":{"Literal":{"Value":"3L"}}},
        "transparency":{"expr":{"Literal":{"Value":"75L"}}}
      }}],
      "background": [{"properties":{"show":{"expr":{"Literal":{"Value":"true"}}},"color":{"solid":{"color":{"expr":{"Literal":{"Value":"'#FFFFFF'"}}}}}}}],
      "border": [{"properties":{
        "show":{"expr":{"Literal":{"Value":"true"}}},
        "color":{"solid":{"color":{"expr":{"Literal":{"Value":"'#E0E4E2'"}}}}},
        "radius":{"expr":{"Literal":{"Value":"8L"}}}
      }}],
      "subTitle": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}}],
      "padding": [{"properties":{
        "top":{"expr":{"Literal":{"Value":"2L"}}},
        "bottom":{"expr":{"Literal":{"Value":"0L"}}},
        "left":{"expr":{"Literal":{"Value":"4L"}}},
        "right":{"expr":{"Literal":{"Value":"4L"}}}
      }}]
    },
    "syncGroup": {
      "groupName": "Sync<CAMPO>",
      "fieldChanges": true,
      "filterChanges": true
    },
    "drillFilterOtherVisuals": true
  }
}
```

### Modos de slicer e restrições de tipo de dado (mecânica)

| Tipo / modo | Uso | Observação técnica |
|---|---|---|
| `slicer` + `data.mode: 'Dropdown'` | padrão do kit | — |
| `slicer` + `data.mode: 'Basic'` | lista visível | — |
| `slicer` + `data.mode: 'Between'` | range de datas | o date picker requer coluna Date/DateTime renderizável; sobre chave inteira/texto pode não renderizar |
| `listSlicer` | slicer moderno de lista/hierarquia | tipo moderno |
| `advancedSlicerVisual` | slicer moderno de botões/tiles | tipo moderno |

⚠️ **Armadilha `Between` + chave numérica/texto:** `Between` sobre coluna inteira (ex.: `AnoMesNumero`, convenção deste kit) ou coluna texto **pode falhar silenciosamente** — o date picker pode não renderizar (sem erro), degradando para um controle inutilizável; trate como não suportado. Para range temporal, aponte o slicer para a coluna de data real da `dCalendario`; para grão ano/mês use `Dropdown`.

**Altura mecânica do `Between`:** com width 216 as duas datas renderizam lado a lado (altura ≈60px + paddings); com width 200 empilham verticalmente (altura ≈84px + paddings) — o breakpoint fica entre esses valores. Nota: o slicer padrão deste kit tem width 170, faixa em que o `Between` empilha; reserve altura/largura em vez de encolher o controle (encolher apenas esconde o clipping, não o resolve).

---

## 8. Template: Card Visual (KPI) — faixa única multi-tile

### ⚠️ REGRA PRINCIPAL: mais de 1 KPI = UM ÚNICO `cardVisual` com N tiles

**Sempre que a página tiver mais de 1 card de KPI, use UM ÚNICO visual `cardVisual` com todas as medidas em `Data.projections`** (um tile por medida) — NUNCA vários visuais de card separados lado a lado. O `autoGrid: true` distribui os tiles na faixa automaticamente.

- **Quantidade de tiles varia por página**: 2, 3, 4, 5 ou 6 KPIs — basta adicionar/remover projections; nenhum recálculo de posição é necessário.
- **`displayName` na projection** renomeia o rótulo do tile (ex.: `"Clientes Compradores no Período"` → `"Compradores no Período"`).
- **Gap entre tiles** = `layout.cellPadding: 15` (interno ao visual, não é gap de posicionamento).
- **1 KPI apenas**: mesmo template, com 1 projection.
- **Posição da faixa**: 1280×720 → `x:30, y:76, w:1225, h:90` · 1920×1080 → `x:22, y:122, w:1878, h:128`.
- O visual "quadro de cards" (chrome branco, cantos arredondados, contorno) é desenhado pelo **tile** (`fillCustom` + `shapeCustomRectangle` + `outline`), e o **contêiner fica 100% limpo** (background/border/dropShadow/title/subTitle `show: false`, padding 0).

### Configurações do Card (extraídas do padrão de referência)

| Propriedade | Valor | Notas |
|-------------|-------|-------|
| visualType | `cardVisual` | Tipo moderno de card (não `card` legado) |
| Data.projections | 1 medida por tile (2–6 tiles) | `displayName` opcional renomeia o rótulo |
| layout.maxTiles | `10L` | |
| layout.cellPadding | `15L` | Gap entre tiles |
| layout.calloutSize | `54D` | |
| layout.showFixedSize | `false` | |
| layout.contentOrder | `'callout_referenceLabel_image'` | |
| layout.autoGrid | `true` | Distribui os tiles na faixa |
| layout.paddingUniform (selector default) | `0L` | |
| value (selector default) | `22L`, bold, `wf_standard-font, helvetica, arial, sans-serif` | **26D** no 1920×1080 |
| label (selector default) | show true, `9L`, `Segoe UI`, bold false, matchValueAlignment true | **14D** no 1920×1080 |
| spacing.verticalSpacing (selector default) | `3L` | |
| padding (selector default) | `'Custom'`: top 15, left 10, right 5, bottom 5; paddingUniform 15; paddingIndividual false | |
| **fillCustom** | global `show: true` + default `fillColor` = **`ThemeDataColor {ColorId: 0, Percent: 0}`**, transparency 0 | fundo do tile **herda do TEMA** — nunca hardcode |
| **shapeCustomRectangle** (selector default) | `rectangleRoundedCurve: 8L` | cantos arredondados do tile |
| **outline** | global `show: false` + default `show: true, weight: 1D` | contorno do tile (padrão dual-entry) |
| accentBar (selector default) | `show: false` | ligar por medida via `selector.metadata` se quiser destaque |
| divider / border (objects, selector default) | `show: false` | |
| Container (visualContainerObjects) | title, subTitle, background, dropShadow, border → TODOS `show: false`; padding 0/0/0/0 | o chrome é do tile, não do container |

> Lembrete (também nas gotchas da SKILL): os objetos do cardVisual com instance selector `{"id": "default"}` (`outline`, `accentBar`, `layout`, `padding`) **não cascateiam do tema** — sempre defina-os per-visual como acima.

### Accent bars por KPI (opcional — padrão é OFF)

No padrão de referência a accent bar fica **desligada** (`show: false` no selector default). Se o projeto pedir destaque por KPI, ligue por medida via `selector.metadata`:

| KPI | Cor | Hex |
|-----|-----|-----|
| Receita / Faturamento | Verde primário | `#2E7D32` |
| Margem / Percentual | Laranja accent | `#F57C00` |
| Ticket Médio / Valor médio | Verde escuro | `#1A3C34` |
| Volume / Quantidade | Verde oliva | `#558B2F` |

### JSON completo (faixa multi-tile — padrão)

> ⚠️ **`cardCalloutArea` só renderiza em cards multi-valor** (2+ medidas em `Data`) — neste template multi-tile ele é ativo. Note também o padrão **dual-entry** do `outline` e do `fillCustom`: a entrada global controla o `show` e a entrada com `selector {"id": "default"}` carrega os valores; sem a dupla entrada a propriedade pode ser silenciosamente ignorada.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.8.0/schema.json",
  "name": "<HEX_ID>",
  "position": { "x": 30, "y": 76, "z": 6000, "height": 90, "width": 1225 },
  "visual": {
    "visualType": "cardVisual",
    "query": {
      "queryState": {
        "Data": {
          "projections": [
            {
              "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TABELA_MEDIDAS>" } }, "Property": "<MEDIDA_1>" } },
              "queryRef": "<TABELA_MEDIDAS>.<MEDIDA_1>",
              "nativeQueryRef": "<MEDIDA_1>",
              "displayName": "<RÓTULO_CURTO_1>"
            },
            {
              "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TABELA_MEDIDAS>" } }, "Property": "<MEDIDA_2>" } },
              "queryRef": "<TABELA_MEDIDAS>.<MEDIDA_2>",
              "nativeQueryRef": "<MEDIDA_2>"
            }
          ]
        }
      },
      "sortDefinition": {
        "sort": [{ "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TABELA_MEDIDAS>" } }, "Property": "<MEDIDA_1>" } }, "direction": "Descending" }],
        "isDefaultSort": true
      }
    },
    "objects": {
      "accentBar": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}},"selector":{"id":"default"}}],
      "outline": [
        {"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}},
        {"properties":{"show":{"expr":{"Literal":{"Value":"true"}}},"weight":{"expr":{"Literal":{"Value":"1D"}}}},"selector":{"id":"default"}}
      ],
      "layout": [
        {"properties":{
          "maxTiles":{"expr":{"Literal":{"Value":"10L"}}},
          "cellPadding":{"expr":{"Literal":{"Value":"15L"}}},
          "calloutSize":{"expr":{"Literal":{"Value":"54D"}}},
          "showFixedSize":{"expr":{"Literal":{"Value":"false"}}},
          "contentOrder":{"expr":{"Literal":{"Value":"'callout_referenceLabel_image'"}}},
          "autoGrid":{"expr":{"Literal":{"Value":"true"}}}
        }},
        {"properties":{"paddingUniform":{"expr":{"Literal":{"Value":"0L"}}}},"selector":{"id":"default"}}
      ],
      "label": [{"properties":{
        "show":{"expr":{"Literal":{"Value":"true"}}},
        "fontFamily":{"expr":{"Literal":{"Value":"'Segoe UI'"}}},
        "fontSize":{"expr":{"Literal":{"Value":"9L"}}},
        "bold":{"expr":{"Literal":{"Value":"false"}}},
        "matchValueAlignment":{"expr":{"Literal":{"Value":"true"}}}
      },"selector":{"id":"default"}}],
      "spacing": [{"properties":{"verticalSpacing":{"expr":{"Literal":{"Value":"3L"}}}},"selector":{"id":"default"}}],
      "value": [{"properties":{
        "fontFamily":{"expr":{"Literal":{"Value":"'wf_standard-font, helvetica, arial, sans-serif'"}}},
        "fontSize":{"expr":{"Literal":{"Value":"22L"}}},
        "bold":{"expr":{"Literal":{"Value":"true"}}}
      },"selector":{"id":"default"}}],
      "padding": [{"properties":{
        "paddingSelection":{"expr":{"Literal":{"Value":"'Custom'"}}},
        "leftMargin":{"expr":{"Literal":{"Value":"10L"}}},
        "rightMargin":{"expr":{"Literal":{"Value":"5L"}}},
        "topMargin":{"expr":{"Literal":{"Value":"15L"}}},
        "bottomMargin":{"expr":{"Literal":{"Value":"5L"}}},
        "paddingUniform":{"expr":{"Literal":{"Value":"15L"}}},
        "paddingIndividual":{"expr":{"Literal":{"Value":"false"}}}
      },"selector":{"id":"default"}}],
      "divider": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}},"selector":{"id":"default"}}],
      "cardCalloutArea": [{"properties":{
        "paddingIndividual":{"expr":{"Literal":{"Value":"false"}}},
        "paddingTop":{"expr":{"Literal":{"Value":"0L"}}},
        "paddingBottom":{"expr":{"Literal":{"Value":"0L"}}}
      },"selector":{"id":"default"}}],
      "border": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}},"selector":{"id":"default"}}],
      "fillCustom": [
        {"properties":{"show":{"expr":{"Literal":{"Value":"true"}}}}},
        {"properties":{
          "fillColor":{"solid":{"color":{"expr":{"ThemeDataColor":{"ColorId":0,"Percent":0}}}}},
          "transparency":{"expr":{"Literal":{"Value":"0D"}}}
        },"selector":{"id":"default"}}
      ],
      "shapeCustomRectangle": [{"properties":{"rectangleRoundedCurve":{"expr":{"Literal":{"Value":"8L"}}}},"selector":{"id":"default"}}]
    },
    "visualContainerObjects": {
      "title": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}}],
      "subTitle": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}}],
      "padding": [{"properties":{
        "top":{"expr":{"Literal":{"Value":"0L"}}},
        "bottom":{"expr":{"Literal":{"Value":"0L"}}},
        "left":{"expr":{"Literal":{"Value":"0L"}}},
        "right":{"expr":{"Literal":{"Value":"0L"}}}
      }}],
      "background": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}}],
      "dropShadow": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}}],
      "border": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}}}}],
      "spacing": [
        {"properties":{
          "customizeSpacing":{"expr":{"Literal":{"Value":"true"}}},
          "spaceBelowSubTitle":{"expr":{"Literal":{"Value":"16D"}}},
          "spaceAbovePlotArea":{"expr":{"Literal":{"Value":"16D"}}}
        }},
        {"properties":{"verticalSpacing":{"expr":{"Literal":{"Value":"2D"}}}},"selector":{"id":"default"}}
      ]
    },
    "drillFilterOtherVisuals": true
  }
}
```

Adicione uma projection por KPI (2 a 6). Em **1920×1080**: `position { "x": 22, "y": 122, "z": 6000, "height": 128, "width": 1878 }`, `value.fontSize: 26D`, `label.fontSize: 14D`.

### Reference label (comparativo abaixo do valor — opcional)

Padrão usado no projeto de referência para exibir um comparativo (ex.: "Ano Anterior") dentro de um tile, com cor condicional verde/vermelha. Três objetos por tile-alvo, todos com `selector.metadata` apontando para a medida do tile:

```json
"referenceLabel": [{
  "properties": { "value": { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TABELA_MEDIDAS>" } }, "Property": "<MEDIDA_COMPARATIVA>" } } } },
  "selector": { "data": [{"dataViewWildcard":{"matchingOption":0}}], "metadata": "<TABELA_MEDIDAS>.<MEDIDA_DO_TILE>", "id": "field-<UUID>", "order": 0 }
}],
"referenceLabelTitle": [{
  "properties": {
    "titleContentType": { "expr": { "Literal": { "Value": "'custom'" } } },
    "titleText": { "expr": { "Literal": { "Value": "'Ano Anterior'" } } }
  },
  "selector": { "metadata": "<TABELA_MEDIDAS>.<MEDIDA_DO_TILE>", "id": "field-<UUID>" }
}],
"referenceLabelValue": [
  {
    "properties": { "valueFontColor": { "solid": { "color": { "expr": { "Conditional": { "Cases": [
      { "Condition": { "Comparison": { "ComparisonKind": 2, "Left": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TABELA_MEDIDAS>" } }, "Property": "<MEDIDA_CONDICAO>" } }, "Right": { "Literal": { "Value": "<LIMIAR>D" } } } }, "Value": { "Literal": { "Value": "'#499f79'" } } },
      { "Condition": { "Comparison": { "ComparisonKind": 3, "Left": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TABELA_MEDIDAS>" } }, "Property": "<MEDIDA_CONDICAO>" } }, "Right": { "Literal": { "Value": "<LIMIAR>D" } } } }, "Value": { "Literal": { "Value": "'#A50000'" } } }
    ] } } } } } },
    "selector": { "data": [{"dataViewWildcard":{"matchingOption":0}}], "metadata": "<TABELA_MEDIDAS>.<MEDIDA_DO_TILE>" }
  },
  { "properties": { "valueBold": { "expr": { "Literal": { "Value": "true" } } } }, "selector": { "metadata": "<TABELA_MEDIDAS>.<MEDIDA_DO_TILE>" } }
]
```

Cores do padrão: `#499f79` (positivo) e `#A50000` (negativo). `ComparisonKind`: 2 = `>=`, 3 = `<`. O `id: "field-<UUID>"` é um UUID novo prefixado com `field-`, repetido entre `referenceLabel` e `referenceLabelTitle`.

---

## 9. Template: Gráfico (Chart)

### Princípios de visualização limpa (SWD — Storytelling with Data)

1. **Sem título de eixo** — `showAxisTitle: false` em categoryAxis e valueAxis (o título do gráfico já dá contexto)
2. **Sem subtítulo** — `subTitle show: false` no `visualContainerObjects`
3. **Font dos eixos: 9D** — pequena e discreta, cor cinza (#757575)
4. **DataLabels vs Eixo — NUNCA ambos** — se dataLabels ON → valueAxis OFF + gridlines OFF. Se valueAxis ON → dataLabels OFF + gridlines sutis (#EEEEEE)
5. **Data labels** — preferencialmente em gráficos de barra/coluna, tamanho 9D, cor #757575. Quando ativados, ocultar valueAxis.
6. **Legenda** — posição Top, tamanho 9D, apenas quando há 2+ séries. Para 2 séries, prefira label direto na série.
7. **Título narrativo** — `Segoe UI Semibold`, 10D, cor #1A3C34. Comunique o insight ("Receita cresceu 12%") ao invés de apenas o tema ("Receita Mensal"). Sempre com `titleWrap: true`.
8. **Sort** — sempre explícito (Ascending para temporal, Descending para ranking)
9. **Cor estratégica** — cinza (#999999) para contexto/referência, cor primária (#2E7D32) para destaque. Máximo 3 cores por gráfico.
10. **Sem marcadores em linhas** — `showMarker: false` por padrão (exceto ponto de destaque isolado)
11. **Barras > espaço** — barras devem ser mais largas que o gap entre elas
12. **Sem 3D, gradientes ou sombras em barras** — simplicidade sempre
13. **Sem borda do gráfico** se não agrega informação — use espaço branco para separar

### ⚠️ Query Wells — REGRA CRÍTICA

| visualType | Well do Eixo/Categoria | Well dos Valores |
|------------|------------------------|------------------|
| `lineChart` | `Category` | `Y` |
| `clusteredBarChart` | `Category` | `Y` |
| `clusteredColumnChart` | `Category` | `Y` |
| `slicer` | `Values` | — |
| `cardVisual` | — | `Data` |

**NUNCA use `"Values"` como query well em gráficos (lineChart, clusteredBarChart, clusteredColumnChart).** O well correto para medidas nesses visuais é `"Y"`. Se usar "Values", o gráfico renderiza sem dados.

### Template de query para gráficos (1 série)

```json
"query": {
  "queryState": {
    "Category": {
      "projections": [{
        "field": { "Column": { "Expression": { "SourceRef": { "Entity": "<ENTIDADE_CATEGORIA>" } }, "Property": "<COLUNA_CATEGORIA>" } },
        "queryRef": "<ENTIDADE_CATEGORIA>.<COLUNA_CATEGORIA>",
        "nativeQueryRef": "<COLUNA_CATEGORIA>",
        "active": true
      }]
    },
    "Y": {
      "projections": [{
        "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TABELA_MEDIDAS>" } }, "Property": "<NOME_MEDIDA>" } },
        "queryRef": "<TABELA_MEDIDAS>.<NOME_MEDIDA>",
        "nativeQueryRef": "<NOME_MEDIDA>"
      }]
    }
  },
  "sortDefinition": {
    "sort": [{ "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TABELA_MEDIDAS>" } }, "Property": "<NOME_MEDIDA>" } }, "direction": "<Ascending|Descending>" }]
  }
}
```

### Template de query para gráficos (2 séries no Y)

```json
"query": {
  "queryState": {
    "Category": {
      "projections": [{
        "field": { "Column": { "Expression": { "SourceRef": { "Entity": "<ENTIDADE_CATEGORIA>" } }, "Property": "<COLUNA_CATEGORIA>" } },
        "queryRef": "<ENTIDADE_CATEGORIA>.<COLUNA_CATEGORIA>",
        "nativeQueryRef": "<COLUNA_CATEGORIA>",
        "active": true
      }]
    },
    "Y": {
      "projections": [
        {
          "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TABELA_MEDIDAS>" } }, "Property": "<MEDIDA_1>" } },
          "queryRef": "<TABELA_MEDIDAS>.<MEDIDA_1>",
          "nativeQueryRef": "<MEDIDA_1>"
        },
        {
          "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TABELA_MEDIDAS>" } }, "Property": "<MEDIDA_2>" } },
          "queryRef": "<TABELA_MEDIDAS>.<MEDIDA_2>",
          "nativeQueryRef": "<MEDIDA_2>"
        }
      ]
    }
  },
  "sortDefinition": {
    "sort": [{ "field": { "Column": { "Expression": { "SourceRef": { "Entity": "<ENTIDADE_CATEGORIA>" } }, "Property": "<COLUNA_CATEGORIA>" } }, "direction": "Ascending" }]
  }
}
```

### VisualContainerObjects padrão (aplicar em TODOS os gráficos)

```json
"visualContainerObjects": {
  "dropShadow": [{"properties":{
    "show":{"expr":{"Literal":{"Value":"true"}}},
    "color":{"solid":{"color":{"expr":{"Literal":{"Value":"'#B0BEC5'"}}}}},
    "preset":{"expr":{"Literal":{"Value":"'Custom'"}}},
    "shadowSpread":{"expr":{"Literal":{"Value":"0L"}}},
    "shadowBlur":{"expr":{"Literal":{"Value":"8L"}}},
    "angle":{"expr":{"Literal":{"Value":"90L"}}},
    "shadowDistance":{"expr":{"Literal":{"Value":"3L"}}},
    "transparency":{"expr":{"Literal":{"Value":"75L"}}}
  }}],
  "background": [{"properties":{
    "show":{"expr":{"Literal":{"Value":"true"}}},
    "color":{"solid":{"color":{"expr":{"Literal":{"Value":"'#FFFFFF'"}}}}},
    "transparency":{"expr":{"Literal":{"Value":"0D"}}}
  }}],
  "border": [{"properties":{
    "show":{"expr":{"Literal":{"Value":"true"}}},
    "color":{"solid":{"color":{"expr":{"Literal":{"Value":"'#E0E4E2'"}}}}},
    "radius":{"expr":{"Literal":{"Value":"8L"}}},
    "width":{"expr":{"Literal":{"Value":"1D"}}}
  }}],
  "title": [{"properties":{
    "show":{"expr":{"Literal":{"Value":"true"}}},
    "text":{"expr":{"Literal":{"Value":"'<TÍTULO DO GRÁFICO>'"}}},
    "titleWrap":{"expr":{"Literal":{"Value":"true"}}},
    "fontColor":{"solid":{"color":{"expr":{"Literal":{"Value":"'#1A3C34'"}}}}},
    "fontSize":{"expr":{"Literal":{"Value":"10D"}}},
    "bold":{"expr":{"Literal":{"Value":"true"}}},
    "fontFamily":{"expr":{"Literal":{"Value":"'''Segoe UI Semibold'', wf_segoe-ui_semibold, helvetica, arial, sans-serif'"}}}
  }}],
  "subTitle": [{"properties":{"show":{"expr":{"Literal":{"Value":"false"}}},"fontSize":{"expr":{"Literal":{"Value":"'12'"}}}}}],
  "spacing": [{"properties":{
    "customizeSpacing":{"expr":{"Literal":{"Value":"true"}}},
    "verticalSpacing":{"expr":{"Literal":{"Value":"2D"}}},
    "spaceBelowSubTitle":{"expr":{"Literal":{"Value":"16D"}}}
  }}],
  "padding": [{"properties":{
    "top":{"expr":{"Literal":{"Value":"14D"}}},
    "bottom":{"expr":{"Literal":{"Value":"16D"}}},
    "left":{"expr":{"Literal":{"Value":"16D"}}},
    "right":{"expr":{"Literal":{"Value":"16D"}}}
  }}]
}
```

### Objects padrão para eixos (aplicar em TODOS os gráficos)

```json
"objects": {
  "categoryAxis": [{"properties":{
    "showAxisTitle":{"expr":{"Literal":{"Value":"false"}}},
    "fontSize":{"expr":{"Literal":{"Value":"9D"}}},
    "innerPadding":{"expr":{"Literal":{"Value":"30L"}}}
  }}],
  "valueAxis": [{"properties":{
    "showAxisTitle":{"expr":{"Literal":{"Value":"false"}}},
    "fontSize":{"expr":{"Literal":{"Value":"9D"}}},
    "gridlineShow":{"expr":{"Literal":{"Value":"true"}}},
    "gridlineColor":{"solid":{"color":{"expr":{"Literal":{"Value":"'#EEEEEE'"}}}}}
  }}]
}
```

### Cores por série (dataPoint)

Para gráficos com 2 séries (ex: valor atual vs comparação):
```json
"dataPoint": [
  {"properties":{"fill":{"solid":{"color":{"expr":{"Literal":{"Value":"'#2E7D32'"}}}}}},"selector":{"metadata":"<MEDIDA_1>"}},
  {"properties":{"fill":{"solid":{"color":{"expr":{"Literal":{"Value":"'#F57C00'"}}}}}},"selector":{"metadata":"<MEDIDA_2>"}}
]
```

Para gráficos com 1 série:

⚠️ **`fill` sem selector em gráfico de 1 série deixa as barras/colunas INVISÍVEIS** (os dados só aparecem no tooltip). `fill` exige selector `metadata`; para a cor base de série única a propriedade correta é `dataPoint.defaultColor`:

```json
"dataPoint": [{"properties":{"defaultColor":{"solid":{"color":{"expr":{"Literal":{"Value":"'#2E7D32'"}}}}}}}]
```

### Data labels (apenas para gráficos de barra)

```json
"dataLabels": [{"properties":{
  "show":{"expr":{"Literal":{"Value":"true"}}},
  "fontSize":{"expr":{"Literal":{"Value":"9D"}}},
  "color":{"solid":{"color":{"expr":{"Literal":{"Value":"'#757575'"}}}}}
}}]
```

### Legenda (para gráficos com 2+ séries)

```json
"legend": [{"properties":{
  "show":{"expr":{"Literal":{"Value":"true"}}},
  "fontSize":{"expr":{"Literal":{"Value":"9D"}}},
  "position":{"expr":{"Literal":{"Value":"'Top'"}}}
}}]
```

### Line chart: estilos de linha

```json
"lineStyles": [
  {"properties":{"strokeWidth":{"expr":{"Literal":{"Value":"3D"}}},"lineStyle":{"expr":{"Literal":{"Value":"'solid'"}}}},"selector":{"metadata":"<MEDIDA_PRINCIPAL>"}},
  {"properties":{"strokeWidth":{"expr":{"Literal":{"Value":"2D"}}},"lineStyle":{"expr":{"Literal":{"Value":"'dashed'"}}}},"selector":{"metadata":"<MEDIDA_COMPARAÇÃO>"}}
]
```

---

## 10. Tema Customizado (JSON para RegisteredResources)

Salvar como `Coinest_Inspired_Green.json` em `StaticResources/RegisteredResources/`:

```json
{
  "$schema": "https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.153.json",
  "name": "Coinest_Inspired_Green",
  "dataColors": ["#2E7D32", "#F57C00", "#558B2F", "#81C784", "#1A3C34", "#A5D6A7", "#F57C00", "#FFB74D"],
  "background": "#F4F6F5",
  "foreground": "#1A1A1A",
  "tableAccent": "#2E7D32",
  "textClasses": {
    "callout": { "fontSize": 24, "fontFace": "Segoe UI Semibold", "color": "#1A1A1A" },
    "title": { "fontSize": 14, "fontFace": "Segoe UI Semibold", "color": "#1A3C34" },
    "header": { "fontSize": 12, "fontFace": "Segoe UI Semibold", "color": "#1A1A1A" },
    "label": { "fontSize": 10, "fontFace": "Segoe UI", "color": "#757575" }
  },
  "visualStyles": {
    "*": {
      "*": {
        "background": [{ "color": { "solid": { "color": "#FFFFFF" } }, "transparency": 0 }],
        "border": [{ "show": true, "color": { "solid": { "color": "#E0E4E2" } }, "radius": 8 }],
        "dropShadow": [{ "show": true, "color": { "solid": { "color": "#B0BEC5" } }, "shadowBlur": 8, "shadowDistance": 3, "transparency": 75 }]
      }
    }
  }
}
```

### Mecânica do theme JSON (não altera a paleta do kit)

- **`$schema`**: declare sempre — habilita validação estrutural do tema no editor e no QA.
- **Formato de cor**: dentro de `visualStyles`, TODA cor usa o wrapper `{"solid": {"color": "#hex"}}`. Cor como string pura (`"color": "#E0E4E2"`) diverge do formato do schema; propriedades fora do formato do schema tendem a não ser aplicadas (fallback para o default do Power BI).
- **Camada por tipo de visual**: além do wildcard `"*"/"*"`, o tema aceita blocos por tipo — as chaves devem usar os nomes MODERNOS (`tableEx`, `pivotTable`, `cardVisual`, `textbox`, `slicer`; `barChart` e `clusteredBarChart` são entradas separadas). Chaves legadas (`table`, `card`) não atingem os visuais modernos.
- **Wildcard de padding/background**: expandir o wildcard só é seguro se cada tipo de visual afetado for verificado e receber override explícito quando necessário (textbox e cardVisual quebram com padding/background herdados; `tableEx` precisa de grow-to-fit) — sem alterar os valores do kit.
- **`$id: "default"`**: alguns objetos do `cardVisual` no tema exigem o discriminador `"$id": "default"` no item do array (ex.: `value`, `label`) para o estilo se aplicar à instância default. Atenção: os objetos de instance selector do `cardVisual` (`outline`, `accentBar`, `layout`, `padding`) **não cascateiam do tema** — devem ser definidos per-visual em `visual.objects` (ver template §8); o padrão `$id` no tema aplica-se apenas a objetos que cascateiam.
- **Chaves opcionais disponíveis no schema** (preencher com cores DA PALETA DO KIT, se/quando o design decidir): `good`/`neutral`/`bad` (trio de sentimento para KPIs/CF), `maximum`/`center`/`minimum`/`null` (defaults de gradientes divergentes), `firstLevelElements` (= `foreground`), `secondLevelElements` (eixos/subtítulos), `thirdLevelElements` (gridlines), `fourthLevelElements` (rótulos esmaecidos), `secondaryBackground`. Sem elas, o conditional formatting cai nos defaults do Power BI.
- **Limites da engine**: não há controle por textClass de letter-spacing nem de tabular figures; a classe `title` propaga para a classe derivada `largeTitle` (títulos de visual). Fontes com renderização idêntica em Desktop/Service/mobile/embedded: Segoe UI, DIN, Georgia, Consolas, Arial, Calibri, Tahoma, Verdana — fontes fora da lista exigem cadeia de fallback (`'MinhaFonte', "Segoe UI", sans-serif`).
- **Cache por nome de arquivo**: ao editar um tema existente, o Desktop pode não refletir a mudança no reload — renomeie o arquivo (e atualize `report.json`) ou feche/reabra o Desktop.

---

## 11. Boas Práticas de Data Storytelling (baseado em Cole Nussbaumer Knaflic — Storytelling with Data)

Estas regras são fundamentais para criar visualizações limpas, claras e eficazes. Cada elemento desnecessário em um gráfico consome carga cognitiva do público. O objetivo é reduzir o "ruído" para que os dados falem por si.

### 11.1 Regra de Ouro: Rótulos de Dados vs Eixo de Valores

**Quando há rótulos de dados (dataLabels: show true), o eixo de valores (valueAxis) deve ser ocultado (show: false).** Mostrar ambos é redundância — a mesma informação aparece duas vezes. Escolha um:

| Cenário | dataLabels | valueAxis | gridlines |
|---------|-----------|-----------|-----------|
| Valores exatos são importantes (barras, colunas) | `show: true` | `show: false` | `show: false` |
| Tendência geral importa mais (linhas, áreas) | `show: false` | `show: true` | sutil `#EEEEEE` |
| Poucos pontos de dados (≤5 barras) | `show: true` | `show: false` | `show: false` |
| Muitos pontos de dados (>12) | `show: false` | `show: true` | sutil |

Regra prática para PBIR:
- Em `clusteredBarChart` e `clusteredColumnChart`: prefira dataLabels ON + valueAxis OFF + gridlines OFF
- Em `lineChart`: prefira valueAxis ON + gridlines sutis + dataLabels OFF (exceto ponto de destaque)

### 11.2 Eliminação de Clutter (Desordem Visual)

Remova sistematicamente tudo que não carrega informação:

| Elemento | Ação | Justificativa |
|----------|------|---------------|
| **Borda do gráfico** | `border show: false` ou cor muito sutil | Bordas não informam; use espaço em branco |
| **Gridlines** | Remover ou tornar muito sutis (#EEEEEE, 1px) | Se tem dataLabels, remover completamente |
| **Marcadores de linha** | Não usar em lineChart (exceto destaque) | Poluem a visualização sem agregar |
| **Títulos de eixo** | `showAxisTitle: false` sempre | O contexto já está no título do gráfico |
| **Tick marks** | Reduzir ao mínimo necessário | Menos marcas = menos ruído visual |
| **Efeitos 3D** | Jamais usar | Distorcem a comparação de valores |
| **Gradientes/sombras em barras** | Não usar | Simplicidade > decoração |
| **SubTítulo do visual** | `subTitle show: false` | Raramente necessário |
| **Legenda separada** | Preferir label direto na série | Evita "ida e volta" do olhar |

### 11.3 Uso Estratégico de Cor

Cor deve ser usada com parcimônia e intenção. A filosofia SWD é: **projete em cinza primeiro, depois adicione UMA cor de destaque.**

**Regras práticas para PBIR:**

1. **1 série de dados** → Use apenas a cor primária (#2E7D32). Sem legenda.
2. **2 séries comparativas** → Cor primária para o destaque + cinza (#999999) para a referência (ex: ano atual vs anterior)
3. **Destaque estratégico** → Use cor forte (#F57C00 laranja ou #2E7D32 verde) APENAS no elemento que conta a história. O restante em cinza neutro.
4. **Nunca usar mais de 3 cores** em um único gráfico — se precisar de mais, repense a visualização.
5. **Evite vermelho+verde juntos** — inacessível para daltônicos. Use laranja (#F57C00) no lugar de vermelho.
6. **Consistência** — a mesma medida deve ter a mesma cor em todos os gráficos da página.

### 11.4 Escolha de Tipo de Gráfico

| Objetivo | Tipo recomendado | Tipo a evitar |
|----------|-----------------|---------------|
| Comparar categorias | `clusteredBarChart` (horizontal) | Pie chart, donut |
| Tendência temporal | `lineChart` | Barras para séries temporais longas |
| Ranking (top N) | `clusteredBarChart` (horizontal, sort desc) | Tabela, column chart |
| Parte do todo | Stacked bar 100% | Pie chart |
| Comparar 2 períodos | `lineChart` com 2 séries (atual + anterior) | Tabela lado a lado |
| Valor único (KPI) | `cardVisual` ou texto simples | Gauge, donut com 1 valor |
| Desvio/variação | Barra positiva/negativa | Linhas para desvios |

**Regras de ouro para tipo de gráfico:**
- Se há **1 ou 2 números isolados**, use `cardVisual` ou texto simples — não gaste um gráfico.
- **Barras horizontais** são preferíveis a colunas quando os nomes das categorias são longos.
- **Barras devem ser mais largas que o espaço entre elas** — isso facilita a comparação.
- **Nunca use rótulos de eixo X na diagonal** — se não cabem, use barras horizontais ou abrevie.
- **Pie charts são desencorajados** — o olho humano é ruim em comparar ângulos/áreas.

### 11.5 Títulos que Contam a História

Em vez de títulos descritivos ("Vendas por Mês"), use títulos que comuniquem o insight:

| ❌ Título descritivo | ✅ Título narrativo |
|---------------------|---------------------|
| Receita por Estado | SP lidera com 26% da receita total |
| Vendas Mensais | Receita cresceu 12% vs ano anterior |
| Cancelamentos por Mês | Taxa de cancelamento estável em ~8% |

**Implementação em PBIR:** Use o campo `text` em `visualContainerObjects.title` para comunicar o insight principal. Se o dado é dinâmico, use o título descritivo como fallback — mas sempre que possível, inclua o "e daí?" ("so what?").

### 11.6 Hierarquia Visual e Princípios de Gestalt

Use estes princípios para organizar a informação na página:

- **Proximidade**: Agrupe visualmente elementos relacionados (cards de KPI em linha, gráficos relacionados lado a lado)
- **Similaridade**: Use mesma cor/estilo para dados da mesma natureza
- **Enclosure**: Use fundo/borda para agrupar (header bar = grupo de navegação)
- **Continuidade**: Alinhe gráficos em grid — o olhar segue linhas naturais
- **Leitura em Z**: Coloque o KPI mais importante no canto superior esquerdo (Card 1)

**Posição = importância:**
- Topo-esquerda → Informação mais importante
- Cards → Resumo executivo (visão em 3 segundos)
- Gráficos superiores → Análise principal
- Gráficos inferiores → Detalhamento / drill-down

### 11.7 Atributos Pré-Atentivos

Atributos visuais processados pelo cérebro em menos de 250ms. Use UM atributo por gráfico:

| Atributo | Como usar em PBIR |
|----------|-------------------|
| **Cor** | dataPoint fill para destacar uma barra/série |
| **Tamanho** | fontSize maior no card principal (22L vs 18L) |
| **Posição** | Card 1 no canto superior esquerdo |
| **Orientação** | Barras horizontais para ranking, verticais para temporal |

**Regra: use no máximo 1 atributo de destaque por gráfico.** Se tudo está destacado, nada está destacado.

### 11.8 Framework Narrativo

Toda página de dashboard deve seguir o framework "O quê → E daí → E agora":

1. **O quê?** → Cards de KPI mostram os números-chave
2. **E daí?** → Gráficos mostram o contexto (tendência, comparação, composição)
3. **E agora?** → Título narrativo ou callout indica a ação necessária

---

## 12. Regras SWD Aplicadas ao JSON PBIR

Tradução direta das regras de Data Storytelling para propriedades JSON dos visuais:

### 12.1 Gráfico de Barras/Colunas com DataLabels (sem eixo de valores)

```json
"objects": {
  "dataLabels": [{"properties": {
    "show": {"expr": {"Literal": {"Value": "true"}}},
    "fontSize": {"expr": {"Literal": {"Value": "9D"}}},
    "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#757575'"}}}}}
  }}],
  "categoryAxis": [{"properties": {
    "show": {"expr": {"Literal": {"Value": "true"}}},
    "showAxisTitle": {"expr": {"Literal": {"Value": "false"}}},
    "fontSize": {"expr": {"Literal": {"Value": "9D"}}}
  }}],
  "valueAxis": [{"properties": {
    "show": {"expr": {"Literal": {"Value": "false"}}}
  }}]
}
```

### 12.2 Gráfico de Linha sem DataLabels (com eixo de valores sutil)

```json
"objects": {
  "categoryAxis": [{"properties": {
    "show": {"expr": {"Literal": {"Value": "true"}}},
    "showAxisTitle": {"expr": {"Literal": {"Value": "false"}}},
    "fontSize": {"expr": {"Literal": {"Value": "9D"}}}
  }}],
  "valueAxis": [{"properties": {
    "show": {"expr": {"Literal": {"Value": "true"}}},
    "showAxisTitle": {"expr": {"Literal": {"Value": "false"}}},
    "fontSize": {"expr": {"Literal": {"Value": "9D"}}},
    "gridlineShow": {"expr": {"Literal": {"Value": "true"}}},
    "gridlineColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#EEEEEE'"}}}}}
  }}],
  "lineStyles": [{"properties": {
    "showMarker": {"expr": {"Literal": {"Value": "false"}}}
  }}],
  "legend": [{"properties": {
    "show": {"expr": {"Literal": {"Value": "true"}}},
    "position": {"expr": {"Literal": {"Value": "'Top'"}}},
    "fontSize": {"expr": {"Literal": {"Value": "9D"}}}
  }}]
}
```

### 12.3 Destaque com Cor Estratégica (1 série destaque + 1 cinza)

```json
"dataPoint": [
  {"properties": {"fill": {"solid": {"color": {"expr": {"Literal": {"Value": "'#2E7D32'"}}}}}},
   "selector": {"metadata": "Medidas.Receita Concluída"}},
  {"properties": {"fill": {"solid": {"color": {"expr": {"Literal": {"Value": "'#999999'"}}}}}},
   "selector": {"metadata": "Medidas.Receita Ano Anterior"}}
]
```

### 12.4 Container Limpo (sem borda, sem sombra desnecessária)

Para gráficos com dataLabels onde o visual já é auto-explicativo:

```json
"visualContainerObjects": {
  "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}],
  "dropShadow": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}],
  "background": [{"properties": {
    "show": {"expr": {"Literal": {"Value": "true"}}},
    "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}},
    "transparency": {"expr": {"Literal": {"Value": "0D"}}}
  }}]
}
```

---

## 13. Checklist de Criação de Página

Ao criar uma nova página, siga esta ordem:

0. **Perguntar ANTES de gerar (§0)**: tem tema? (se sim, usar as cores do tema) · página 1280×720 ou 1920×1080?
1. **Gerar hex IDs únicos** para a página e cada visual
2. **Criar page.json** com fundo `#F4F6F5` e `displayOption: FitToPage` (720/1280 ou 1080/1920 conforme resposta)
3. **Header bar** (shape) — z:0, verde escuro, full width
4. **TextBox** — z:11000, título branco sobre o header
5. **Slicers** — z:9000–10000, dropdown, canto direito do header, **em 1280×720: y=3 e height máx. 57** (1920×1080: y=14, h=78), com `syncGroup`
6. **Cards** — z:5000–8000, **UM único cardVisual multi-tile com todas as medidas (§8)** — nunca vários cards separados; **SEM título (show: false)**
7. **Gráficos** — z:1000–4000, grid 2×2 abaixo dos cards (3 visuais → 1 em largura total na linha de baixo, §4), **query well "Y" para medidas**
8. **Atualizar pages.json** — adicionar ao `pageOrder`
9. **OBRIGATÓRIO: subTitle show: false** em TODOS os visuais
10. **Nunca usar** títulos de eixo (`showAxisTitle: false`)
11. **Gridlines**: remover se há dataLabels; manter sutil se não há
12. **Sempre usar** sort explícito
13. **Sempre usar** `drillFilterOtherVisuals: true`
14. **Schema** — copie o `$schema` de um visual existente do mesmo report; NUNCA rebaixe para `visualContainer/2.8.0` se o projeto usa versão maior. Em report novo sem visuais existentes, o default dos templates deste arquivo (`visualContainer/2.8.0`) permanece válido
15. **Query wells**: `"Y"` para gráficos, `"Values"` para slicers, `"Data"` para cards
16. **Títulos de gráfico**: incluir `titleWrap: true` e `fontFamily` no visualContainerObjects.title
17. **Spacing/Padding**: incluir `spacing` e `padding` no visualContainerObjects dos gráficos
18. **SWD — DataLabels vs Eixo**: se dataLabels ON → valueAxis OFF + gridlines OFF
19. **SWD — Cor estratégica**: cinza para contexto, cor forte apenas para destaque
20. **SWD — Sem marcadores**: lineChart com `showMarker: false` (exceto ponto de destaque)
21. **SWD — Barras > espaço**: barras mais largas que o gap entre elas
22. **SWD — Sem 3D/gradientes/sombras desnecessárias**: simplicidade sempre
23. **SWD — Hierarquia visual**: KPI mais importante no Card 1 (topo-esquerda)
24. **SWD — Título narrativo**: quando possível, título comunica o insight, não apenas o tema
25. **Slicer com título**: height mínimo de 55px quando `header.show: true` (40px corta o título); em 1280×720 o máximo é 57px com y=3
26. **Fill do tile do card**: `fillCustom.fillColor` via `ThemeDataColor` (herda o tema) — nunca hardcode hex no tile
27. **Página 1920×1080**: usar posições e fontes da §4B (título 14D, tabelas 10D, slicers 11D, card 26D/14D)
