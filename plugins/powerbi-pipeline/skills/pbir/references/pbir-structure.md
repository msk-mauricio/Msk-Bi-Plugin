# PBIP/PBIR Complete Structure Reference

This document contains the full file hierarchy, JSON schemas, and TMDL syntax for Power BI projects in the modern PBIP/PBIR format.

## Table of Contents

1. [Project Hierarchy](#1-project-hierarchy)
2. [PBIP Project File](#2-pbip-project-file)
3. [Report Structure (PBIR)](#3-report-structure-pbir)
4. [Semantic Model Structure](#4-semantic-model-structure)
5. [TMDL Syntax](#5-tmdl-syntax)
6. [Expression Patterns](#6-expression-patterns)
7. [Visual Types Reference](#7-visual-types-reference)
8. [Modern Tables: tableEx and pivotTable](#8-modern-tables-tableex-and-pivottable)
9. [Filters (filterConfig)](#9-filters-filterconfig)
10. [Page, Interactivity and Accessibility Properties](#10-page-interactivity-and-accessibility-properties)
11. [Schema URLs](#11-schema-urls)

---

## 1. Project Hierarchy

```
project-name/
├── project-name.pbip                           # Project manifest
├── .gitignore                                  # Auto-generated ignore rules
│
├── project-name.Report/                        # Report artifact
│   ├── definition.pbir                         # Report metadata + semantic model reference
│   ├── .platform                               # Fabric integration metadata
│   ├── .pbi/
│   │   ├── localSettings.json                  # Personal settings (GITIGNORED)
│   │   └── cache.abf                           # Local cache (GITIGNORED)
│   ├── definition/
│   │   ├── version.json                        # Report format version
│   │   ├── report.json                         # Global report settings, themes, resources
│   │   ├── pages/
│   │   │   ├── pages.json                      # Page order and active page
│   │   │   └── <PageSection>/
│   │   │       ├── page.json                   # Page dimensions, background, display options
│   │   │       └── visuals/
│   │   │           └── <VisualHexId>/
│   │   │               └── visual.json         # Individual visual definition
│   │   └── bookmarks/
│   │       ├── bookmarks.json                  # Bookmark list
│   │       └── <BookmarkId>.bookmark.json      # Individual bookmark state
│   ├── CustomVisuals/
│   │   └── <VisualId>/
│   │       ├── package.json
│   │       └── resources/
│   │           ├── .pbiviz.json
│   │           ├── *.js
│   │           ├── *.css
│   │           └── icon.png
│   └── StaticResources/
│       ├── RegisteredResources/                # User images, custom themes
│       └── SharedResources/                    # Base themes
│
└── project-name.SemanticModel/                 # Semantic model artifact
    ├── definition.pbism                        # Semantic model metadata
    ├── .platform                               # Fabric integration metadata
    ├── diagramLayout.json                      # Model diagram view layout
    ├── .pbi/
    │   ├── localSettings.json                  # GITIGNORED
    │   └── cache.abf                           # GITIGNORED
    └── definition/
        ├── database.tmdl                       # Compatibility level
        ├── model.tmdl                          # Model config, culture, table refs
        ├── relationships.tmdl                  # All relationships
        ├── tables/
        │   ├── Table1.tmdl                     # Table schema + M query
        │   ├── Table2.tmdl
        │   └── MeasureTable.tmdl               # Dedicated measure table
        └── cultures/
            └── pt-BR.tmdl                      # Linguistic metadata
```

---

## 2. PBIP Project File

**File:** `project-name.pbip`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
  "version": "1.0",
  "artifacts": [
    {
      "report": {
        "path": "project-name.Report"
      }
    }
  ],
  "settings": {
    "enableAutoRecovery": true
  }
}
```

---

## 3. Report Structure (PBIR)

### 3.1 definition.pbir

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byPath": {
      "path": "../project-name.SemanticModel"
    }
  }
}
```

### 3.2 .platform

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "Report",
    "displayName": "Display Name"
  },
  "config": {
    "version": "2.0",
    "logicalId": "uuid-string"
  }
}
```

`type` can be: `"Report"`, `"SemanticModel"`, `"Dashboard"`

### 3.3 report.json

Global report settings, themes, custom visuals, and resource packages.

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.2.0/schema.json",
  "themeCollection": {
    "baseTheme": {
      "name": "CY24SU06",
      "reportVersionAtImport": {
        "visual": "2.8.0",
        "report": "3.2.0",
        "page": "2.3.1"
      },
      "type": "SharedResources"
    },
    "customTheme": {
      "name": "theme-name",
      "reportVersionAtImport": { ... },
      "type": "RegisteredResources"
    }
  },
  "publicCustomVisuals": ["VisualId1", "VisualId2"],
  "resourcePackages": [
    {
      "name": "SharedResources",
      "type": "SharedResources",
      "items": [
        {"name": "base-theme.json", "path": "BaseThemes/base-theme.json", "type": "BaseTheme"}
      ]
    },
    {
      "name": "RegisteredResources",
      "type": "RegisteredResources",
      "items": [
        {"name": "image.svg", "path": "RegisteredResources/image.svg", "type": "Image"},
        {"name": "custom-theme.json", "path": "RegisteredResources/custom-theme.json", "type": "CustomTheme"}
      ]
    }
  ],
  "settings": {
    "useStylableVisualContainerHeader": true,
    "defaultFilterActionIsDataFilter": true,
    "defaultDrillFilterOtherVisuals": true,
    "allowChangeFilterTypes": true,
    "useEnhancedTooltips": true,
    "filterPaneHiddenInEditMode": false
  }
}
```

### Theme cascade boundary — what theme JSON cannot deliver

A custom theme cascades defaults, but the following frequently require per-visual PBIR properties because they may not inherit from `visualStyles`:

- Container rounded corners, explicit container backgrounds and internal padding
- Card accent bars and the other cardVisual objects configured via `selector` (`accentBar`, `outline`, `padding` — see the cardVisual template in `references/visual-design-system.md`)
- Sort order (`query.sortDefinition` — always per-visual; see section 3.6)
- dataColor gradients / conditional-formatting `FillRule` stops — colors depend on the specific measure/category, so they are defined per visual with Literal hex
- On any palette or light↔dark theme swap, gradient stops, card accent bars and state-aware buttons need per-visual updates

**Theme-swap side effects (dependency check before editing any theme JSON):**
- Conditional-formatting rules that reference palette slots may stop resolving after a palette change — re-verify thresholds and color expressions after any swap.
- On light↔dark swaps, every text/background contrast pair must be revalidated per visual.
- Power BI Desktop caches theme files by file name — after editing a theme JSON, rename the file (e.g., add a suffix) and update the corresponding entry in `report.json` (`themeCollection` + `resourcePackages`), or fully close and reopen Desktop; a simple reload may not pick up the edits.

### 3.4 pages.json

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
  "pageOrder": ["PageSection1", "PageSection2", "PageSection3"],
  "activePageName": "PageSection1"
}
```

### 3.5 page.json

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
  "name": "PageSection1",
  "displayName": "Visão Geral",
  "displayOption": "FitToPage",
  "height": 720.00,
  "width": 1280.00,
  "objects": {
    "background": [{
      "properties": {
        "color": {
          "solid": {
            "color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}
          }
        },
        "transparency": {"expr": {"Literal": {"Value": "0D"}}},
        "image": {
          "image": {
            "name": {"expr": {"Literal": {"Value": "'bg.png'"}}},
            "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageItem": {"ItemName": "bg.png"}}}},
            "scaling": {"expr": {"Literal": {"Value": "'Fit'"}}}
          }
        }
      }
    }]
  }
}
```

**displayOption values:** `"FitToPage"`, `"FitToWidth"`, `"ActualSize"`, custom dimensions via height/width

### 3.6 visual.json

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.8.0/schema.json",
  "name": "abc123def456",
  "position": {
    "x": 100.0,
    "y": 50.0,
    "z": 5000,
    "height": 300.0,
    "width": 400.0,
    "tabOrder": 1000
  },
  "visual": {
    "visualType": "clusteredColumnChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [{
            "field": {
              "Column": {
                "Expression": {"SourceRef": {"Entity": "Products"}},
                "Property": "CategoryName"
              }
            },
            "queryRef": "Products.CategoryName",
            "active": true
          }]
        },
        "Y": {
          "projections": [{
            "field": {
              "Measure": {
                "Expression": {"SourceRef": {"Entity": "Sales"}},
                "Property": "TotalRevenue"
              }
            },
            "queryRef": "Sales.TotalRevenue"
          }]
        }
      },
      "sortDefinition": {
        "sort": [{
          "field": {
            "Measure": {
              "Expression": {"SourceRef": {"Entity": "Sales"}},
              "Property": "TotalRevenue"
            }
          },
          "direction": "Descending"
        }],
        "isDefaultSort": true
      }
    },
    "objects": {
      "dataLabels": [{
        "properties": {
          "show": {"expr": {"Literal": {"Value": "true"}}},
          "fontSize": {"expr": {"Literal": {"Value": "12D"}}},
          "color": {"solid": {"color": {"expr": {"ThemeDataColor": {"ColorId": 1, "Percent": 0}}}}}
        }
      }],
      "categoryAxis": [{
        "properties": {
          "show": {"expr": {"Literal": {"Value": "true"}}}
        }
      }],
      "valueAxis": [{
        "properties": {
          "show": {"expr": {"Literal": {"Value": "true"}}}
        }
      }]
    }
  }
}
```

**Query well slots** (depend on visual type — a wrong role name is silently ignored and the visual renders blank):
- `Category` — dimension/axis field for cartesian charts
- `Y` — measure well for `lineChart`, `clusteredBarChart`, `clusteredColumnChart` and other cartesian charts (**NOT** `Values`)
- `Values` — slicers (`slicer`, `listSlicer`, `advancedSlicerVisual`) and `tableEx` columns
- `Data` — `cardVisual` (never `Fields`, which is the legacy `card` role name)
- `Rows` / `Columns` / `Values` — `pivotTable` (row/column-grouping dimensions in Rows/Columns, measures in Values)
- `Series` / `Legend` — legend/series fields; `Tooltips` — tooltip fields
- When unsure, inspect an existing visual of the same type in the project instead of assuming role names.

### 3.7 bookmarks.json

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmarksMetadata/1.0.0/schema.json",
  "items": [
    {"name": "Bookmark1"},
    {"name": "Bookmark2"}
  ]
}
```

### 3.8 Individual bookmark

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.0.0/schema.json",
  "displayName": "Show Product View",
  "name": "Bookmark1",
  "options": {
    "targetVisualNames": ["visual-hex-id-1", "visual-hex-id-2"]
  },
  "explorationState": {
    "version": "1.0",
    "activeSection": "PageSection1",
    "sections": {
      "PageSection1": {
        "visualContainers": {
          "visual-hex-id-1": {
            "isVisible": true
          }
        }
      }
    }
  }
}
```

---

## 4. Semantic Model Structure

### 4.1 definition.pbism

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
  "version": "4.2",
  "settings": {}
}
```

### 4.2 diagramLayout.json

```json
{
  "version": "1.1.0",
  "diagrams": [{
    "ordinal": 0,
    "scrollPosition": {"x": -200, "y": 100},
    "nodes": [
      {
        "location": {"x": 50, "y": 100},
        "nodeIndex": "TableName",
        "size": {"height": 300, "width": 250},
        "zIndex": 0
      }
    ]
  }]
}
```

---

## 5. TMDL Syntax

### 5.1 database.tmdl

```tmdl
database
	compatibilityLevel: 1600
```

### 5.2 model.tmdl

```tmdl
model Model
	culture: pt-BR
	defaultPowerBIDataSourceVersion: powerBI_V3
	sourceQueryCulture: pt-BR
	dataAccessOptions
		legacyRedirects
		returnErrorValuesAsNull

	annotation __PBI_TimeIntelligenceEnabled = 0
	annotation PBI_QueryOrder = ["Table1","Table2","Table3"]
	annotation PBI_ProTooling = ["MCP-PBIModeling","DevMode"]

	ref table Table1
	ref table Table2
	ref table MeasureTable

	ref cultureInfo pt-BR
```

### 5.3 Table with columns and partitions

```tmdl
/// Description of the table
table Products
	lineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567890

	/// Product unique identifier
	column ProductID
		dataType: int64
		lineageTag: 11111111-2222-3333-4444-555555555555
		summarizeBy: none
		sourceColumn: ProductID

		annotation SummarizationSetBy = Automatic

	column ProductName
		dataType: string
		lineageTag: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
		summarizeBy: none
		sourceColumn: ProductName

		annotation SummarizationSetBy = Automatic

	column Price
		dataType: double
		lineageTag: 12345678-abcd-ef01-2345-678901234567
		summarizeBy: sum
		sourceColumn: Price

		annotation SummarizationSetBy = Automatic
		annotation PBI_FormatHint = {"isGeneralNumber":true}

	column DateAdded
		dataType: dateTime
		formatString: dd/MM/yyyy
		lineageTag: fedcba98-7654-3210-fedc-ba9876543210
		summarizeBy: none
		sourceColumn: DateAdded

		annotation SummarizationSetBy = Automatic

	partition Products = m
		mode: import
		source =
			let
			    Fonte = Sql.Database("server.database.windows.net", "MyDB"),
			    dbo_Products = Fonte{[Schema="dbo",Item="Products"]}[Data]
			in
			    dbo_Products

		annotation PBI_ResultType = Table
```

### 5.4 Measure table

```tmdl
table Measures
	lineageTag: 99999999-8888-7777-6666-555555555555

	measure 'Total Revenue' = SUM(Sales[Amount])
		formatString: #,0.00
		displayFolder: Revenue
		lineageTag: aaaa1111-bbbb-2222-cccc-3333dddd4444

	measure 'Profit Margin %' = DIVIDE([Total Revenue] - [Total Cost], [Total Revenue], 0)
		formatString: 0.00%;-0.00%;0.00%
		displayFolder: Profitability
		lineageTag: eeee5555-ffff-6666-0000-111122223333

	measure 'YTD Revenue' = TOTALYTD([Total Revenue], Calendar[Date])
		formatString: R$\ #,0.00;-R$\ #,0.00;R$\ #,0.00
		displayFolder: Time Intelligence
		lineageTag: 44445555-6666-7777-8888-999900001111

		annotation PBI_FormatHint = {"currencyCulture":"pt-BR"}
```

### 5.5 relationships.tmdl

```tmdl
relationship 12345678-abcd-ef01-2345-678901234567
	fromColumn: Sales.ProductID
	toColumn: Products.ProductID

relationship 87654321-dcba-10fe-5432-109876543210
	fromColumn: Sales.DateKey
	toColumn: Calendar.DateKey
```

Relationships are many-to-one by default (from = many side, to = one side).

### 5.6 cultures (linguistic metadata)

```tmdl
cultureInfo pt-BR

	linguisticMetadata =
		{
		  "Version": "2.0.0",
		  "Language": "pt-BR"
		}
```

---

## 6. Expression Patterns

Used in visual.json and page.json property values:

| Pattern | Syntax | Example |
|---------|--------|---------|
| String literal | `{"expr":{"Literal":{"Value":"'text'"}}}` | `'#FF0000'`, `'Fit'` |
| Number literal | `{"expr":{"Literal":{"Value":"13D"}}}` | `0D`, `100D` |
| Boolean | `{"expr":{"Literal":{"Value":"true"}}}` | `true`, `false` |
| Theme color | `{"expr":{"ThemeDataColor":{"ColorId":0,"Percent":0}}}` | ColorId 0-12, Percent -100 to 100 |
| Column ref | `{"Column":{"Expression":{"SourceRef":{"Entity":"Table"}},"Property":"Col"}}` | |
| Measure ref | `{"Measure":{"Expression":{"SourceRef":{"Entity":"Table"}},"Property":"Meas"}}` | |
| Resource ref | `{"expr":{"ResourcePackageItem":{"PackageName":"RegisteredResources","PackageItem":{"ItemName":"file.png"}}}}` | |

### FillRule gradients — Literal hex only

Value-driven gradients use `dataPoint.fill` with a `FillRule` (`linearGradient2` with min/max stops) and the selector `{"dataViewWildcard": {"matchingOption": 0}}`.

⚠️ **Rendering trap:** inside a `FillRule`, `ThemeDataColor` references DO NOT resolve — the gradient silently renders black/default. Color stops MUST be `Literal` hex values: resolve the theme color to its hex before writing the JSON.

**Where each color mechanism lives** (theme defines cascading defaults; these are the per-visual anchor points):

| Goal | Property path |
|------|---------------|
| Base color of a single-series chart | `dataPoint.defaultColor` |
| Per-series color | `dataPoint.fill` + `selector.metadata` (queryRef of the measure/series) |
| Per-category color | `dataPoint.fill` + scope-identity selector |
| Value-driven gradient | `dataPoint.fill` + `FillRule` (**Literal hex stops only**) |
| Card accent bar — accepts measure-driven conditional formatting | `accentBar.color` |
| Data label / title text color | `labels.color`, `title.fontColor` |
| In-cell data bars / icon sets / cell gradient (tables & matrix) | `dataBar`, `iconRule`, `fillRule` (conditional formatting objects) |

Note: single-measure bar charts render all bars in one color because the palette assigns colors **per series, not per category** — to differentiate categories use per-category selectors or a sequential FillRule gradient (never duplicate the same field as category + legend).

---

## 7. Visual Types Reference

**Rule: never create legacy visual types.** The `powerbi-report-author validate` CLI (when available) emits the `PBIR_VISUAL_TYPE_DEPRECATED` warning (code documented for `multiRowCard`, `map`, `filledMap`; the never-create rule applies to all six legacy types below).

| visualType | Status | Notes |
|------------|--------|-------|
| `cardVisual` | modern | replaces `card` and `multiRowCard` (multi-value = 2+ projections in `Data`) |
| `tableEx` | modern | replaces `table` |
| `pivotTable` | modern | replaces `matrix` |
| `azureMap` | modern | replaces `map`/`filledMap`. If Azure Maps doesn't render (tenant policy / region), fall back to `tableEx` with conditional formatting or `clusteredBarChart` per region; `shapeMap` is a specialized shape-based visual, not a general substitute |
| `listSlicer` / `advancedSlicerVisual` | modern | modern list/tile slicers; classic `slicer` remains valid via `data.mode` |
| `aiNarratives` | modern | Smart Narrative — verify formatting/query mechanics for the target report version before use; otherwise prefer a textbox bound to a narrative measure |
| `decompositionTreeVisual` | modern | decomposition/flow analysis |
| `card`, `multiRowCard`, `table`, `matrix`, `map`, `filledMap` | **DEPRECATED — never create** | only read/interpret when found in existing reports |
| `clusteredColumnChart`, `clusteredBarChart`, `stackedColumnChart`, `stackedBarChart`, `hundredPercentStackedBarChart`, `lineChart`, `areaChart`, `lineClusteredColumnComboChart`, `waterfallChart`, `ribbonChart`, `scatterChart`, `treemap`, `pieChart`, `donutChart`, `funnel`, `gauge`, `kpi` | current | `scatterChart` supports a play-axis role for time animation; `waterfallChart` has `increase`/`decrease`/`total` sentiment colors |
| `textbox`, `shape`, `image`, `actionButton`, `pageNavigator`, `bookmarkNavigator`, `slicer` | current | — |

**Native platform gaps** (do not attempt to instantiate — they don't exist as native types): histogram (bin the data and use a column chart), box plot (custom visual only), full Sankey (native option is limited — use `decompositionTreeVisual` or a custom visual), dumbbell/tornado/slope graph (simulate with bar variants or a `lineChart` over a 2-period categorical axis), IBCS-style hatching (needs pattern fills via theme or custom visual).

---

## 8. Modern Tables: tableEx and pivotTable

- **Wells:** `tableEx` takes all fields in `Values`. `pivotTable` uses `Rows` (row-grouping dimensions), `Columns` (column-grouping dimensions) and `Values` (measures). A `tableEx` given dimensions AND measures where a matrix was intended renders **headers with no data rows** — use `pivotTable` with dimensions in `Rows`.
- **Column sizing:** without `columnHeaders.autoSizeColumnWidth: true` + `columnHeaders.columnAdjustment: "growToFit"`, columns render shrunken with trailing whitespace.
- **Custom row colors:** `values.backColorPrimary`/`backColorSecondary` (banded rows) have NO effect unless the visualContainerObjects `stylePreset` is set to `'None'`. And whenever you set backColorPrimary/Secondary you MUST also set `fontColorPrimary`/`fontColorSecondary` — otherwise cell text can become invisible.
- **pivotTable extras:** the default expand/collapse state of hierarchies is persisted in `expansionStates`; cell heatmaps use the conditional-formatting `fillRule`; formatting objects beyond tableEx: `rowHeaders`, `subTotals`, `columnSubtotals`, `columnHeaders`.

---

## 9. Filters (filterConfig)

Filters exist at three levels — report (`report.json`), page (`page.json`) and visual (`visual.json`) — and all use the same `filterConfig.filters` array. Essential mechanics:

- ⚠️ **`"Source"` inside `Where`, `"Entity"` in the top-level `field`.** The filter's `field` (outside the `filter` object) references the table via `SourceRef.Entity`. But inside the `Where` conditions of the `filter` object (Version 2), the `SourceRef` must use `"Source"` with the alias declared in the `From` clause — never `"Entity"`. Using `Entity` inside `Where` keeps the JSON schema-valid and Desktop raises no error, but the filter is **not applied** (silent failure). Do not swap `Entity` for `Source` in the top-level `field` — the mistake only exists inside `Where`.
- **Slicer selections do not live in filterConfig.** A slicer's current selection is persisted exclusively in the slicer's own `visual.json`, in `objects.general.filter` (and, for hierarchy slicers with expanded nodes, also in `expansionStates`) — never in the `filterConfig` of other visuals.
- For higher-level filter operations (TopN, date ranges, categorical), prefer the `power-bi-filters` plugin skill when available in the session; this section is the fallback knowledge.

---

## 10. Page, Interactivity and Accessibility Properties

**Page-level:**
- `background` and wallpaper are distinct objects in `page.json` (the wallpaper is serialized as `outspace` in the JSON; validate against the schema via `pbip:pbir-format` before editing). Set the page background `transparency` explicitly (`0D`).
- `autoPageRefreshInterval` only works with DirectQuery sources (minimum 1s on Premium capacity, 30min on shared capacity); `changeDetection` triggers refresh only when upstream data changes.
- `personalizeVisuals: true` is a page-level setting that lets end users swap measure/axis without edit mode.

**Cross-visual interactions:**
- Three modes per source→target pair: **Highlight** (dims non-selected — default for charts), **Filter** (cards/KPIs must be set to Filter — they must update to show the selected subset), **None** (fixed benchmark/reference visuals). Configure deliberately; don't ship unreviewed defaults.
- **Sync slicers** persist via a named `syncGroup` — synchronization is by field, across pages.
- **Tooltip pages:** small canvas (typically 320×240) + `tooltipType: ReportPage`; never put critical data there (tooltips are not reachable by all input paths).
- **`actionButton`** supports `action` values `PageNavigation`, `Bookmark`, `Drillthrough`; always set `altText`. Drillthrough target pages must include a back button. `bookmarkNavigator` references a bookmark group.
- **Bookmarks** capture composite state — filters + visual visibility + position — referencing visual ids (see SKILL.md: renaming a visual's hex `name` breaks bookmarks). Avoid timer-driven auto-cycling bookmark carousels (accessibility violation) — use static views with manual next/prev buttons.

**Accessibility as verifiable properties:**
- `position.tabOrder` must follow the visual reading order (top-left → bottom-right), not creation order.
- Alt text is a per-visual property and accepts a static value OR a measure-driven (DAX) expression for dynamic alt text — write content-specific text (the insight and value), never just the chart type.
- Interactive targets (slicer items, buttons) should be ≥ 24×24 px.
- Don't disable visual headers indiscriminately — "Show as table" and header actions are accessibility affordances (hide only on decorative visuals).

---

## 11. Schema URLs

All PBIR JSON files declare their schema. Key URLs:

> **Snapshot note:** the versioned suffixes below are example snapshots, NOT required values — Power BI Desktop bumps them with most releases. Always preserve the `$schema` of the real file you are editing; when creating a new file, copy the `$schema` from a sibling of the same type (see SKILL.md § schema version rules).

| File | Schema URL |
|------|-----------|
| .pbip | `https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json` |
| definition.pbir | `https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json` |
| definition.pbism | `https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json` |
| report.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.2.0/schema.json` |
| pages.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json` |
| page.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json` |
| visual.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.8.0/schema.json` |
| bookmarks.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmarksMetadata/1.0.0/schema.json` |
| bookmark.json | `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.0.0/schema.json` |
| .platform | `https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json` |
