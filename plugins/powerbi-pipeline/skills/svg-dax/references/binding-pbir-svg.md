# Binding PBIR de medidas SVG — JSONs por tipo de visual

> Complementa `reports:svg-visuals` (que assume extension measures) com: binding de **medida de
> modelo** (default D-22 deste kit), especificidades de matriz e o binding por item/estado do button
> slicer extraído do PBIX de demonstração oficial do PowerofBI.IBCS (`avatorl/dax-udf-svg-ibcs`).

## 1. Regra do SourceRef (vale para todos os visuais)

```json
// Medida do MODELO (default do kit — D-22): SEM Schema
{ "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Medidas" } },
    "Property": "Receita Tendência SVG" } },
  "queryRef": "Medidas.Receita Tendência SVG", "nativeQueryRef": "Receita Tendência SVG" }

// Extension measure (reportExtensions.json): COM Schema
{ "field": { "Measure": { "Expression": { "SourceRef": { "Schema": "extension", "Entity": "Medidas" } },
    "Property": "Receita Tendência SVG" } },
  "queryRef": "Medidas.Receita Tendência SVG" }
```

- O `queryRef` **não** carrega o schema — e é a chave que os seletores de formatação
  (`selector.metadata` de `columnWidth` etc.) precisam casar caractere a caractere, acentos incluídos.
- Trocar um pelo outro é a causa nº 1 de "campo não encontrado" ao abrir o relatório.

## 2. Tabela (`tableEx`) e Matriz (`pivotTable`)

Tamanho da imagem — global ao visual (não há configuração por coluna), UI "Image size", faixa
documentada **8–512 px**:

```json
"objects": {
  "grid": [ { "properties": {
    "imageHeight": { "expr": { "Literal": { "Value": "28D" } } },
    "imageWidth":  { "expr": { "Literal": { "Value": "160D" } } },
    "rowPadding":  { "expr": { "Literal": { "Value": "3D" } } } } } ],
  "columnHeaders": [ { "properties": {
    "autoSizeColumnWidth": { "expr": { "Literal": { "Value": "false" } } } } } ],
  "columnWidth": [ { "properties": { "value": { "expr": { "Literal": { "Value": "180D" } } } },
    "selector": { "metadata": "Medidas.Receita Tendência SVG" } } ]
}
```

- Sufixo `D` (Double) obrigatório nos literais numéricos; `L` para inteiros como `z`/`tabOrder`.
- Defaults sem `grid`: 25×100 px — quase sempre pequeno demais.
- Altura efetiva da linha = maior entre imageHeight e a fonte das demais colunas + rowPadding —
  ajustar os três juntos.
- `columnWidth` da coluna SVG ≥ imageWidth + ~20 px de folga; `autoSizeColumnWidth: false`, senão o
  auto-ajuste corta a imagem ao filtrar.
- **Proporção**: `viewBox` com a mesma razão de imageWidth×imageHeight (ex.: `0 0 160 28` para
  160×28) deixa 1 unidade SVG = 1 px. `preserveAspectRatio='none'` força esticar (só para
  barras/retângulos — distorce círculos e texto).
- Alternativa via tema (padroniza o relatório inteiro): `visualStyles.pivotTable.*.grid: [{ "imageHeight": 28, "imageWidth": 160 }]`
  — no tema os valores são números JSON simples, sem `expr/Literal` e sem sufixo.

### Especificidades da matriz

- Papéis: `Rows` / `Columns` / `Values` (a tabela `tableEx` usa só `Values`).
- `sortDefinition` é irmão de `queryState` dentro de `query` — ordenar pela própria medida SVG
  funciona (`{"sort": [{"field": {Measure…}, "direction": "Descending"}], "isDefaultSort": true}`),
  desde que a string tenha chave ordenável no primeiro trecho variável.
- Duas chaves de ordenação equivalentes (mesmo princípio — prefixo constante + chave de largura fixa):
  - `<desc>` + `FORMAT ( v, "000000000000" )` como **primeiro** elemento após `<svg>`;
  - comentário `/*SortBy:` & rank & `*/` dentro de `<style>` (padrão PowerofBI.IBCS:
    `1000000000000 + ROUND(v, 0)`). Negativos quebram a ordem alfabética — somar offset antes.
- Subtotais — duas estratégias legítimas:
  1. `IF ( HASONEVALUE ( dX[Col] ), <svg> )` → subtotal em branco (default do kit);
  2. Padrão IBCS: `VAR __EhTotal = NOT ISINSCOPE ( dX[Col] )` e renderizar variante de total
     (negrito/barra total) — preserva a chave de ordenação nos níveis pai de hierarquias.
- Seletores de formatação por alvo: `dataViewWildcard.matchingOption` `1` = só instâncias,
  `2` = só totais; `hierarchyMatching: 1` = todos os níveis.
- Stepped layout: `rowHeaders.stepped` + `steppedLayoutIndentation`; expansão persistida em
  `visual.expansionStates`.
- Sort trick em hierarquia multi-nível não tem evidência pública testada — validar no Desktop e
  registrar pendência.

## 3. Visual Image (`image`) — standalone

```json
"objects": { "image": [ { "properties": {
  "sourceType":   { "expr": { "Literal": { "Value": "'imageData'" } } },
  "sourceField":  { "expr": { "Measure": { "Expression": { "SourceRef": { "Entity": "Medidas" } },
                    "Property": "KPI Header SVG" } } },
  "transparency": { "expr": { "Literal": { "Value": "0D" } } },
  "effects":      { "expr": { "Literal": { "Value": "false" } } } } } ] }
```

- **`sourceType` = `'imageData'`** para data URI. `'imageUrl'` (HTTP) causa
  `VisualDataProxyExecutionUnknownError` e renderiza **preto**.
- **Sem bloco `query`** — a medida é avaliada via `sourceField`; adicionar query duplica a avaliação.
- viewBox maiores (300×60 KPI, 300×50 sparkline) e fontes maiores (~28px) que em célula.

## 4. Cartão novo (`cardVisual`)

```json
"objects": { "callout": [ { "properties": {
  "imageFX":     { "expr": { "Literal": { "Value": "true" } } },
  "imageHeight": { "expr": { "Literal": { "Value": "40D" } } },
  "imageWidth":  { "expr": { "Literal": { "Value": "100D" } } } } } ] }
```

- Três slots de imagem no cartão (UI "Select from data" → medida ImageUrl): **Image** (hero — a doc
  oficial recomenda para SVGs de tendência), **Callout image** (ícone junto ao valor) e **Category
  header background**; estados Default/Hover trocam a imagem (medidas diferentes por estado).
- Card **clássico** (`card`) não suporta — se renderizar texto/blank, conferir o visualType.
- GA nov/2025; o walkthrough oficial da Microsoft usa uma UDF `TrendSVG` com `dataCategory: ImageUrl`
  (learn.microsoft.com/power-bi/visuals/power-bi-visualization-card).

## 5. Button slicer (`advancedSlicerVisual`) — imagem por item e por estado

A medida SVG **não entra em field well** — só em `objects.image`, avaliada por botão:

```json
"objects": { "image": [
  { "properties": { "image": { "expr": { "Measure": {
        "Expression": { "SourceRef": { "Entity": "Medidas" } },
        "Property": "Coluna Mensal SVG" } } } },
    "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ],
                  "id": "default", "hierarchyMatching": 1 } },
  { "properties": { "enhancedFit": { "expr": { "Literal": { "Value": "'Fit'" } } },
                    "height":      { "expr": { "Literal": { "Value": "300L" } } } },
    "selector": { "id": "default" } }
] }
```

- Binding **por item** = selector com `dataViewWildcard.matchingOption: 1` + `hierarchyMatching: 1`;
  a entrada só com `id` configura propriedades estáticas do estado.
- Estados (`selector.id`): `default`, `interaction:rest`, `interaction:hover`, `selection:selected`,
  `selection:unselected`, `selection:selected-interaction:hover`, `series:selectall`. Troca de SVG por
  estado = repetir a entrada com outra medida (ex.: `… Hover SVG`); `"image": "''"` suprime no
  Select all.
- Objetos acompanhantes usuais: `layout` (rowCount×columnCount, `cellPadding: 0L`),
  `value.show=false` (esconde o texto, fica só o SVG), `fillCustom` por estado,
  `visualContainerObjects.title.text` aceita medida (título dinâmico).
- Ordenação de botões limitada a "Value" (doc oficial).
- Campo dos itens em `queryState.Values`; medidas de tooltip em `Tooltips`.

## 6. actionButton — **não suportado**

Imagem de botão é sempre recurso estático (`ResourcePackageItem` em
`StaticResources/RegisteredResources`); a formatação condicional de botões cobre cores/texto/efeitos,
não imagem. Um `Measure` expr em `icon.image.url` valida no schema (que é aberto), mas não há
evidência de funcionar em runtime — tratar como não suportado. **Workaround canônico**: button slicer
com um único item (tem estados + binding por medida nativos), ou camadas + bookmarks.

## 7. reportExtensions.json (caminho secundário — D-22)

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/reportExtension/1.0.0/schema.json",
  "name": "extension",
  "entities": [ { "name": "Medidas", "measures": [ {
    "name": "Receita Tendência SVG",
    "dataType": "Text",
    "dataCategory": "ImageUrl",
    "displayFolder": "90. Visuais SVG",
    "expression": "<DAX com \\n e \\\" escapados — atributos SVG em aspas simples evitam escape duplo>"
  } ] } ]
}
```

- `entities[].name` deve ser tabela **existente** do modelo (o arquivo não cria tabelas); nome da
  medida único no espaço combinado modelo+extensões; `dataCategory` é opcional no schema — esquecê-lo
  degrada para string crua sem aviso.
- Arquivo **opcional que não pode ficar vazio**: ao remover a última medida, apagar o arquivo inteiro
  (com `entities: []` o Desktop falha ao abrir o PBIP).
- Extension measures moram no `.Report` → `powerbi-desktop reload` as recarrega (diferente de TMDL,
  que exige reabrir o PBIP) — bom para iteração estética na Fase 6.
