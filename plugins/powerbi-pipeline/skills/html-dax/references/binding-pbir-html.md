# Binding PBIR do visual HTML Content — registro, JSONs por cenário e navegação

> Complementa `pbip:pbir-format` com o fluxo específico do HTML Content: registro do custom visual
> no `report.json` + `visual.json` por cenário, objects próprios do visual e a receita de navegação
> por botões nativos transparentes. GUIDs e regras de edição (lite vs standard): ver SKILL.md §
> "Decisão de edição". Schema de referência do repo: `visualContainer/2.11.0`. Relatório PBIR de
> referência do próprio autor do visual: pasta `test-uat` em `github.com/dm-p/powerbi-visuals-html-content`
> (demonstra binding de Column; o suporte a Measure vem do schema `semanticQuery` 1.4.0).

## 1. Passo 1 — registrar o visual no `definition/report.json`

```json
{
  "publicCustomVisuals": [
    "htmlContent443BE3AD55E043BF878BED274D3A6865"
  ]
}
```

- Array no nível raiz do `report.json`; se já existir, **acrescentar** o GUID (um por edição usada).
- Sem o registro, toda instância falha com "Can't display this visual. To see this custom visual,
  add it to this report first".
- Visual **organizacional** usa campo próprio `organizationCustomVisuals` (`{name, path, disabled}`);
  visual **privado** (.pbiviz) fica versionado em `CustomVisuals/`/`RegisteredResources/` — únicos
  caminhos com pinning de versão. Visual do AppSource **não** fica no repo: o Desktop baixa na 1ª
  abertura (internet + AppSource liberado no tenant → pendência runtime no `TODO.md`).

## 2. Regra do SourceRef (idêntica à do svg-dax)

```json
// Medida do MODELO (default do kit): SEM Schema
{ "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "Medidas" } },
    "Property": "Home Página HTML" } },
  "queryRef": "Medidas.Home Página HTML", "nativeQueryRef": "Home Página HTML" }

// Extension measure (reportExtensions.json): COM Schema (o queryRef NÃO carrega o schema)
{ "field": { "Measure": { "Expression": { "SourceRef": { "Schema": "extension", "Entity": "Medidas" } },
    "Property": "Home Página HTML" } },
  "queryRef": "Medidas.Home Página HTML" }
```

## 3. Cenário A — página única (só a medida HTML)

`visual.json` completo e mínimo — a medida no role `content`, CSS no object `stylesheet`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.11.0/schema.json",
  "name": "a1b2c3d4e5f6a7b8c9d0",
  "position": { "x": 0, "y": 0, "z": 0, "height": 720, "width": 1280 },
  "visual": {
    "visualType": "htmlContent443BE3AD55E043BF878BED274D3A6865",
    "query": {
      "queryState": {
        "content": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "Medidas" } },
                  "Property": "Home Página HTML"
                }
              },
              "queryRef": "Medidas.Home Página HTML",
              "nativeQueryRef": "Home Página HTML"
            }
          ]
        }
      }
    },
    "objects": {
      "contentFormatting": [
        {
          "properties": {
            "format": { "expr": { "Literal": { "Value": "'html'" } } },
            "showRawHtml": { "expr": { "Literal": { "Value": "false" } } },
            "noDataMessage": { "expr": { "Literal": { "Value": "'Sem dados para o contexto atual'" } } }
          }
        }
      ],
      "stylesheet": [
        {
          "properties": {
            "stylesheet": { "expr": { "Literal": { "Value": "'.kpiGrid { display: flex; gap: 16px; } .kpiCard { border-radius: 12px; font-family: ''Segoe UI'', sans-serif; }'" } } }
          }
        }
      ]
    }
  }
}
```

- **Escaping de `expr.Literal`**: string envolvida em aspas simples; aspas simples internas do CSS
  **duplicadas** (`''Segoe UI''`). Booleans e números vão sem aspas (número com sufixo `D`).
- `contentFormatting` — propriedades documentadas: `format` (`'html'`|`'markdown'`), `showRawHtml`,
  `fontFamily`, `fontSize`, `fontColour` (grafia britânica), `align`, `overrideInlineStyling`,
  `hyperlinks` ("Allow opening URLs"), `userSelect`, `noDataMessage`.
- `stylesheet` — CSS separado do DAX (diff limpo); aceita **formatação condicional** (binding a
  medida/coluna via expressão de agregação) quando o CSS precisa reagir a dados sem reescrever a
  medida. Seletores-alvo do visual: `#htmlContent` (container) e `.htmlViewerEntry` (cada linha).
- Nomes de propriedade vêm do `capabilities.json` do visual — na dúvida, conferir no repo dm-p antes
  de inventar chave nova.

## 4. Cenário B — grade repetida por linha (`sampling` + cross-filter)

A coluna no role `sampling` (rótulo de UI "Sampling" no capabilities 1.6.x; as docs do visual usam
"Granularity") faz o visual repetir a medida **por linha** do contexto e habilita
cross-filtering, drillthrough e context menu (sem `sampling`, design de medida única perde quase
toda a interatividade):

```json
"query": {
  "queryState": {
    "sampling": {
      "projections": [
        {
          "field": {
            "Column": {
              "Expression": { "SourceRef": { "Entity": "dCliente" } },
              "Property": "NomeCliente"
            }
          },
          "queryRef": "dCliente.NomeCliente",
          "nativeQueryRef": "NomeCliente"
        }
      ]
    },
    "content": {
      "projections": [
        {
          "field": {
            "Measure": {
              "Expression": { "SourceRef": { "Entity": "Medidas" } },
              "Property": "Card Cliente HTML"
            }
          },
          "queryRef": "Medidas.Card Cliente HTML",
          "nativeQueryRef": "Card Cliente HTML"
        }
      ]
    }
  }
}
```

Com cross-filter, adicionar o object de feedback visual de seleção (classes `hover`/`unselected`
entram no HTML; a transparência dos não selecionados é do visual):

```json
"crossFilter": [
  {
    "properties": {
      "enabled": { "expr": { "Literal": { "Value": "true" } } },
      "useTransparency": { "expr": { "Literal": { "Value": "true" } } },
      "transparencyPercent": { "expr": { "Literal": { "Value": "60D" } } }
    }
  }
]
```

## 5. Cenário C — tooltip

Medidas adicionais no role `tooltips` ficam disponíveis para o tooltip padrão do Power BI; dentro
do HTML, os atributos `data-tooltip-title-*`/`data-tooltip-value-*` montam tooltip por elemento
(classe `tooltipEnabled`):

```json
"tooltips": {
  "projections": [
    {
      "field": {
        "Measure": {
          "Expression": { "SourceRef": { "Entity": "Medidas" } },
          "Property": "Receita Bruta"
        }
      },
      "queryRef": "Medidas.Receita Bruta",
      "nativeQueryRef": "Receita Bruta"
    }
  ]
}
```

## 6. Navegação — botões nativos transparentes sobrepostos (receita canônica)

O HTML desenha o botão (visual); um `actionButton` nativo **100% transparente** por cima executa a
ação (bookmark ou navegação de página). Um `actionButton` por botão desenhado, alinhado à área
clicável e com `z` maior que o do visual HTML:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.11.0/schema.json",
  "name": "b2c3d4e5f6a7b8c9d0e1",
  "position": { "x": 96, "y": 480, "z": 100, "height": 48, "width": 220 },
  "visual": {
    "visualType": "actionButton",
    "objects": {
      "fill": [ { "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } },
        "selector": { "id": "default" } } ],
      "outline": [ { "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } } } ],
      "text": [ { "properties": { "show": { "expr": { "Literal": { "Value": "false" } } } },
        "selector": { "id": "default" } } ]
    },
    "visualContainerObjects": {
      "visualLink": [
        {
          "properties": {
            "show": { "expr": { "Literal": { "Value": "true" } } },
            "type": { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
            "navigationSection": { "expr": { "Literal": { "Value": "'7de7362217796b52823f'" } } }
          }
        }
      ]
    }
  }
}
```

- `type` alternativos do `visualLink` (catálogo confirmado em `reports:pbir-cli` §property-catalogue):
  `'Bookmark'` (+ propriedade `bookmark`), `'Drillthrough'` (`drillthroughSection`), `'WebUrl'`
  (`webUrl`), `'Back'`.
- Manter o mapeamento botão HTML ↔ actionButton documentado no handoff da Fase 6 (posições mudam
  juntas).
- Alternativa quando os alvos são itens de dados: button slicer (`advancedSlicerVisual`) ao lado do
  HTML, não sobreposto.

## 7. Armadilhas específicas do binding

- GUID do `visualType` ≠ GUID registrado em `publicCustomVisuals` → "Can't display this visual".
- Trocar de edição (lite ↔ standard) exige trocar **os dois** lugares — e revalidar a sanitização.
- `queryRef` precisa casar caractere a caractere (acentos incluídos) com `Entity.Property` — é a
  chave que seletores de formatação usam.
- O visual **precisa** de pelo menos uma projeção em `content` — sem query, não renderiza nada
  (diferente do visual `image` do svg-dax, que usa `sourceField` sem query).
- Sem `sampling`, o cross-filter não tem grão — `crossFilter.enabled` sozinho não faz nada.
