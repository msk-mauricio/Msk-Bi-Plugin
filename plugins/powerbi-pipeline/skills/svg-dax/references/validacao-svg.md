# Validação de medidas SVG — receita executável (gates 4b, 6 e 7)

> Nenhum passo abaixo escreve no modelo (D-15 preservado): `DEFINE MEASURE` é query-scoped e o
> desktop-bridge é somente leitura/reload. QA permanece read-only.

## 1. Extrair a string em runtime

**Medida de modelo** (canal padrão do kit: `dax_query_operations` do MCP `powerbi-modeling-mcp` com o
Desktop aberto; alternativas: `pbi dax execute --file`, DAX query view):

```dax
EVALUATE
ADDCOLUMNS (
    VALUES ( dCliente[NomeCliente] ),
    "SVG", [Receita Tendência SVG],
    "LenSVG", LEN ( [Receita Tendência SVG] )
)
ORDER BY [LenSVG] DESC
```

**Extension measure** — não existe no modelo, então não é avaliável por nome; mas **qualquer canal que
execute query DAX completa avalia a expressão via `DEFINE MEASURE`** (mecanismo oficial: a doc do DAX
query view diz que report measures "must always be converted to DAX query scoped measures in the
DEFINE MEASURE block to run"). Copiar `expression` do `reportExtensions.json` e envolver:

```dax
DEFINE
    MEASURE Medidas[__SVG Teste] = /* expression copiada do reportExtensions.json */
EVALUATE
ADDCOLUMNS ( VALUES ( dCliente[NomeCliente] ), "SVG", [__SVG Teste], "Len", LEN ( [__SVG Teste] ) )
```

Se a extension measure referencia outras extension measures, todas entram no mesmo bloco `DEFINE`.
O que o `DEFINE` **não** reproduz: o efeito do `dataCategory` e a renderização — isso é o passo 4.

**Nuance ALLSELECTED**: em query pura não há "seleção de slicer" — para reproduzir o eixo do visual,
aplicar o filtro como filtro externo: `CALCULATETABLE ( ADDCOLUMNS (...), dX[Grupo] IN { "A", "B" } )`.
Sem isso o teste mascara bugs de normalização.

Queries persistidas: `powerbi/<Nome>.SemanticModel/DAXQueries/qa-svg-*.dax` (pasta oficial do PBIP);
resultados espelhados em `docs/qa/`.

## 2. Validar cada string retornada

Python sem dependências (ou `xmllint --noout` no arquivo .svg sem o prefixo):

```python
import re, xml.etree.ElementTree as ET
PREFIX = "data:image/svg+xml;utf8,"
def valida_svg(valor):
    erros = []
    if valor is None:
        return ["BLANK"]  # legítimo em guarda de total — registrar, não falhar
    if not valor.startswith(PREFIX):
        erros.append("prefixo data-URI ausente/errado")
    svg = valor.removeprefix(PREFIX)
    try:
        root = ET.fromstring(svg)
        if not root.tag.endswith("svg"): erros.append("raiz não é <svg>")
        if "http://www.w3.org/2000/svg" not in root.tag: erros.append("xmlns ausente")
        if "viewBox" not in root.attrib: erros.append("viewBox ausente")
    except ET.ParseError as e:
        erros.append(f"XML inválido: {e}")
    if "%23" in svg: erros.append("cor com %23 (usar # literal)")
    if "NaN" in svg or "Infinity" in svg: erros.append("NaN/Infinity (DIVIDE sem guarda)")
    # locale pt-BR: vírgula entre dígitos dentro de atributo numérico = coordenada corrompida
    if re.search(r"(?:x|y|x1|y1|x2|y2|cx|cy|r|rx|ry|width|height|points|d)='[^']*\d,\d", svg):
        erros.append("vírgula decimal em atributo (FORMAT en-US ou INT ausente)")
    if re.search(r"\dE\+", svg): erros.append("notação científica em coordenada")
    return erros
```

**Orçamento de comprimento**: 32.766 caracteres é o teto do texto que chega ao visual (truncamento
**silencioso**; a string DAX em si suporta ~2,1 mi — o estouro só aparece na renderização). Gate falha
se `LenMax > 32766`; alerta se `> 29000` (margem p/ crescimento de dados). Mitigações: polyline em vez
de círculos por ponto, coordenadas inteiras, amostragem no CONCATENATEX, ou migrar para Deneb.

## 3. Matriz de casos (por medida SVG)

| # | Caso | Como | Esperado |
|---|---|---|---|
| T1 | Linha normal | `ADDCOLUMNS ( VALUES ( dX[Grupo] ), "SVG", [m] )` | SVG válido por linha |
| T2 | Total/subtotal | `ROW ( "SVG", [m] )` e `SUMMARIZECOLUMNS + ROLLUPADDISSUBTOTAL` | BLANK (guarda) ou variante de total deliberada — nunca gráfico de agregado |
| T3 | Seleção de slicer | `CALCULATETABLE ( …, dX[Grupo] IN {…} )` | eixo renormalizado ao subconjunto |
| T4 | Sem dados | filtro em período vazio | BLANK limpo; nunca NaN/Infinity |
| T5 | 1 ponto na série | filtro em 1 período | fallback (círculo único) ou BLANK — polyline de 1 par não desenha |
| T6 | Negativos e zero | grupo com medida ≤ 0 | width/height nunca negativos; baseline correta |
| T7 | Pior caso de tamanho | contexto mais denso + `ORDER BY [Len] DESC` | LenMax ≤ 32.766 (alerta > 29.000) |
| T8 | Locale pt-BR | qualquer caso com fração | sem `\d,\d` em atributo, sem `E+` |
| T9 | Rótulos longos | categoria de nome máximo em `<text>` | XML ok (`&` → `&amp;` via SUBSTITUTE) |

Mínimo obrigatório no gate 4b: **T1 + T2 + T7 + T8**. Gate 7 (QA): matriz completa + passo 4, saída
em `docs/qa/validacao-svg.md` (tabela medida × caso × resultado + pendências).

## 4. Renderização real — loop desktop-bridge

Extension measures moram no `.Report`, então `reload` basta (mudança TMDL exige reabrir o PBIP):

```text
1. editar reportExtensions.json / visual.json
2. powerbi-report-author validate "powerbi/<Nome>.Report"
3. powerbi-desktop status            → PID conectado, hasUnsavedChanges: false
4. powerbi-desktop reload --pid <pid>
5. powerbi-desktop screenshot <pageId-PBIR> --pid <pid>   (scale 2.0+ para micro-visuais)
```

Checklist SVG no screenshot:

1. Célula vazia/quebrada onde deveria haver gráfico → binding não-Measure, dataCategory ausente ou
   SVG inválido que passou batido (vírgula decimal).
2. Corte abrupto à direita → estouro de 32.766 (o corte costuma quebrar o XML no meio).
3. Esticado/espremido → `grid.imageHeight/imageWidth` vs proporção do `viewBox`.
4. Linha de total: em branco (guarda) ou variante deliberada — nunca gráfico "gigante" de agregado.
5. Ordenar pela coluna SVG → ordem numérica correta (chave `<desc>`)?
6. Barras comparáveis entre linhas (mesma normalização `__EixoMax`)? Barra 100% em toda linha
   denuncia normalização por linha.
7. Cores conferem com o tema/mockup da Fase 5; nada renderizado em preto (cor inválida vira default).
8. Capturar com e sem seleção de slicer (comportamento `ALLSELECTED`).

Sem Desktop/bridge: validação offline (passos 1–3) + pendência runtime manual no `TODO.md` — a
indisponibilidade não bloqueia gate (D-14).

## 5. Preview rápido durante a autoria (antes do DAX)

Montar o SVG estático com valores reais do modelo, salvar como `.svg` no scratchpad, abrir no browser
e colher feedback **antes** de converter em DAX (workflow do plugin `reports:svg-visuals`). Para
render sintético automatizado: navegador headless (Playwright) sobre o arquivo — valida o documento,
não substitui o passo 4 (que valida o pipeline dataCategory → visual).
