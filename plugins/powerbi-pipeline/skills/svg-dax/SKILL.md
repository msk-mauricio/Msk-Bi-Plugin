---
name: svg-dax
description: >
  Use SEMPRE que o projeto pedir gráfico embutido em célula, cartão ou botão via medida DAX que
  retorna SVG — frases-gatilho: "sparkline na tabela", "barra de progresso na célula", "bullet chart
  inline", "status pill", "medida SVG", "gráfico dentro da matriz", "imagem por medida",
  "dataCategory ImageUrl", "extension measure", "reportExtensions.json", "SVG no button slicer",
  "ícone dinâmico no cartão", "waterfall na célula", "heatmap de célula". Também quando aparecer o
  sintoma "a célula mostra o texto data:image/svg+xml em vez da imagem" ou "o SVG renderiza em
  branco/preto". Aplica-se às Fases 4 (medida) e 6 (binding) do pipeline e ao QA (Fase 7).
---

# Skill: Visuais SVG via DAX

> **Preferência de plugin:** templates DAX prontos (12 exemplos), referência de elementos SVG e árvore
> de decisão estão na skill de plugin `reports:svg-visuals`; schemas PBIR em `pbip:pbir-format`; revisão
> final com o agente `reports:svg-reviewer`. **Esta skill define as convenções e o processo DESTE kit
> por cima delas** — em conflito, esta skill vence (ex.: o plugin recomenda extension measures por
> padrão; neste kit o padrão é medida no modelo — ver D-22).

> **Catálogo visual:** `docs/catalogo-svg.html` — 22 espécimes renderizados em tamanho real (barras,
> sparklines, bullet, waterfall, boxplot, gauge, waffle…), cada um com o DAX que o gera, mais a seção
> "Em produção" com as 5 medidas vivas do ValeVerdeBI e o defeito que cada uma escondia até a validação
> em runtime. Abrir no navegador antes de desenhar do zero — o exemplo mais próximo costuma existir.

## Mecânica em uma linha

Medida DAX retorna `"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='…'>…</svg>"`
+ `dataCategory: ImageUrl` → o visual renderiza a string como imagem (tabela, matriz, cartão novo,
image, button slicer). Sem a dataCategory, aparece a string crua — é o defeito nº 1.

## Quando usar / quando não usar

| Necessidade | Solução |
|---|---|
| Micro-gráfico estático em célula/cartão (barra, pill, bullet, tendência) | **SVG via DAX** (esta skill) |
| Linha/coluna simples de tendência em tabela, ≤5 por visual, ≤52 pontos | Sparkline nativo (menos manutenção) |
| Interatividade (tooltip próprio, cross-filter, hover, drill) | Deneb/Vega-Lite (`reports:deneb-visuals`) — SVG é imagem estática, zero interação |
| Estatística pesada (violin, regressão) | Python/R visuals |
| Gráfico standalone de página | Visual nativo sempre (`dataviz-powerbi`) — SVG-DAX não substitui visuais nativos |

## Regra de ouro pt-BR (falha silenciosa nº 1)

Modelos deste kit nascem com `culture: pt-BR` (`model.tmdl`) — a conversão implícita número→texto do
`&` gera **vírgula decimal** (`1.5 & ""` → `"1,5"`), que corrompe atributos e `points` do SVG **sem
erro visível** (testado ao vivo no ValeVerdeBI).

- **Coordenadas**: só inteiros (`INT()`/`ROUND(x, 0)`) ou `FORMAT ( x, "0.0#", "en-US" )` — o 3º
  argumento de locale é obrigatório. `ROUND(x, 1)` **NÃO** protege; `#,0` em coordenada **nunca**.
- **Rótulos**: `FORMAT ( v, "#,0,,.0 "" mi""", "pt-BR" )` → `12,3 mi`. As vírgulas de escala vêm
  **imediatamente antes** do ponto (`#,0,,.0`); a forma `#,0.0,,` não escala na função FORMAT.
  Rótulo pt-BR e coordenada en-US coexistem na mesma medida sem conflito.
- **DaxLib.SVG é vulnerável** em modelo pt-BR (concatena decimais crus): testar antes de adotar;
  preferir passar valores já formatados (parâmetros são STRING).

## Onde a medida mora (D-22)

**Default: no modelo**, na tabela `Medidas` (D-17), arquivo `tables/Medidas.tmdl` — reuso entre
relatórios, rastreabilidade, validação runtime e catálogo de medidas funcionam. Caminho secundário:
**extension measure** em `.Report/definition/reportExtensions.json`, apenas para (a) thin report sobre
modelo que o projeto não pode editar ou (b) iteração estética na Fase 6, com promoção ao TMDL ao
estabilizar. Regras do caminho secundário: o `pbir-report-builder` edita o arquivo (é camada report),
mas o corpo DAX vem do `dax-specialist` via handoff; a entidade `name` deve ser tabela existente do
modelo (`Medidas`); nome único no espaço combinado; **nunca** deixar o arquivo com `entities: []`
(quebra a abertura do PBIP — apagar o arquivo inteiro); binding usa `"Schema": "extension"`.

## Esqueleto TMDL (Fase 4)

```tmdl
	/// Barra de progresso SVG de [Receita Bruta] vs [Meta Receita]. Renderiza via dataCategory ImageUrl.
	measure 'Atingimento Meta Barra SVG' = ```
			VAR __Atingimento = DIVIDE ( [Receita Bruta], [Meta Receita] )
			VAR __CorBarra = IF ( __Atingimento >= 1, [Cor Positiva], [Cor Alerta] )
			VAR __Largura = INT ( 100 * MIN ( __Atingimento, 1 ) )
			VAR __Sort = "<desc>" & FORMAT ( __Atingimento * 1000000, "000000000000" ) & "</desc>"
			RETURN
			    IF (
			        HASONEVALUE ( dCliente[NomeCliente] ),
			        "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 148 20'>"
			            & __Sort
			            & "<rect x='0' y='4' width='100' height='12' rx='6' fill='" & [Cor Trilho] & "'/>"
			            & "<rect x='0' y='4' width='" & __Largura & "' height='12' rx='6' fill='" & __CorBarra & "'/>"
			            & "<text x='106' y='14' font-family='Segoe UI, sans-serif' font-size='11' fill='"
			            & __CorBarra & "'>" & FORMAT ( __Atingimento, "0%", "pt-BR" ) & "</text></svg>"
			    )
			```
		dataCategory: ImageUrl
		formatString: "General"
		displayFolder: 90. Visuais SVG
		lineageTag: <GUID-novo>
```

Convenções fixas (não improvisar): nome de negócio + sufixo ` SVG` (ex.: `Receita Tendência SVG`);
`displayFolder: 90. Visuais SVG`; cores **sempre** via medidas de token (`[Cor Positiva]` etc., pasta
`91. Cores`) — hex literal dentro de medida SVG é falha de revisão (ver
`references/cores-e-tema.md`); atributos com aspas simples; hex com `#` literal (nunca `%23`);
`xmlns` + `viewBox` obrigatórios; fundo transparente (sem rect de fundo — o tema é dono do fundo);
guarda `HASONEVALUE` (ou variante deliberada de total via `NOT ISINSCOPE`); estrutura VAR nas regiões
CONFIG → NORMALIZAÇÃO → ELEMENTOS → MONTAGEM; texto vindo do modelo passa por `SUBSTITUTE` de `&`
(primeiro!), `<` e `>`; série temporal exige `dCalendario` marcada (D-19); medida SVG **embrulha
medidas base aprovadas** (D-04) — nunca esconde lógica de negócio nova.

## Binding PBIR (Fase 6) — referência rápida

| Visual | visualType | Onde liga | Armadilha |
|---|---|---|---|
| Tabela | `tableEx` | projeção em `Values` + `objects.grid.imageHeight/imageWidth` (`"28D"` — sufixo D; faixa 8–512 px) | `autoSizeColumnWidth: false` + `columnWidth` ≥ imageWidth, senão corta |
| Matriz | `pivotTable` | idem; linhas em `Rows` | subtotais/hierarquia: ver referência |
| Image | `image` | `objects.image.sourceType = 'imageData'` + `sourceField` | `'imageUrl'` renderiza **preto**; sem bloco `query` |
| Cartão novo | `cardVisual` | `callout.imageFX` + imagem por estado | card clássico **não** suporta |
| Button slicer | `advancedSlicerVisual` | `objects.image` por item/estado | ver referência (estados `selection:selected` etc.) |
| actionButton | — | **não suportado** (só recurso estático) | usar button slicer de 1 item |

Medida do modelo: `SourceRef` **sem** `Schema`. Extension measure: `"Schema": "extension"` (e o
`queryRef` continua `Medidas.Nome` sem o schema). Proporção do `viewBox` deve casar com
`imageHeight`×`imageWidth`, senão o SVG encolhe com faixas vazias (`preserveAspectRatio` default é
`xMidYMid meet`). JSONs completos por visual: `references/binding-pbir-svg.md`.

## Validação (obrigatória antes de fechar gate)

Mínimo no gate 4b: avaliar a medida em contexto real (T1), no total (T2 — deve dar BLANK), pior caso
de comprimento (T7 — `LEN` ≤ 32.766, alerta > 29.000) e locale (T8 — regex `\d,\d` em atributo).
Extension measures **são testáveis** sem tocar no modelo: envolver a expressão em `DEFINE MEASURE` na
query (doc oficial do DAX query view). Na Fase 6/7: loop `desktop-bridge`
(validate → reload → screenshot) com o checklist SVG. Receita completa, script de validação XML e
matriz de casos T1–T9: `references/validacao-svg.md`.

## Erros comuns (sintoma → causa)

| Sintoma | Causa |
|---|---|
| Célula mostra `data:image/svg+xml…` como texto | `dataCategory: ImageUrl` ausente (ou se perdeu num round-trip) |
| Imagem preta no visual image | `sourceType: 'imageUrl'` em vez de `'imageData'` |
| Imagem em branco, sem erro | Vírgula decimal pt-BR em atributo/points, ou cor `%23`/nomeada |
| Barra gigante na linha de total | Guarda `HASONEVALUE` ausente |
| Imagem pequena com sobras laterais | Proporção do `viewBox` ≠ proporção imageHeight×imageWidth |
| Imagem cortada à direita ao filtrar | `autoSizeColumnWidth` ligado ou `columnWidth` < `imageWidth` |
| Ordenação da coluna SVG errada | `<desc>` ausente/depois de elemento variável, prefixo não constante, valor sem zero-padding ou negativo |
| Gráfico some após ~30 pontos | Estouro dos 32.766 caracteres (truncamento silencioso) |
| PBIP não abre após remover extension measures | `reportExtensions.json` ficou com `entities: []` — apagar o arquivo |

## Checklist de encerramento

- [ ] KPI 🟢/🟡 na matriz de viabilidade (D-04) e medida SVG registrada na **mesma linha** do KPI base
      na matriz de rastreabilidade (não é KPI novo)
- [ ] Medida na tabela `Medidas` com sufixo ` SVG`, displayFolder `90. Visuais SVG`, descrição `///`
- [ ] Cores só via medidas de token; coordenadas INT/en-US; guarda de total; `<desc>` de ordenação
- [ ] Validação T1/T2/T7/T8 anexada ao gate; screenshot via `desktop-bridge` quando disponível
- [ ] Revisão pelo agente `reports:svg-reviewer` antes de apresentar
- [ ] Pendência runtime no `TODO.md` se o Desktop não estava aberto; CHANGELOG conforme o modo
      (pipeline: orquestrador grava; avulso/manual: você grava)
