# Validação de páginas HTML — matriz de casos H1–H9 e receitas

> Uso: gate 4b exige H1–H5; Fases 6/7 acrescentam H6–H9. QA (Fase 7) usa esta referência como
> checklist duro. A medida é testável **sem tocar o modelo** via `DEFINE MEASURE` na query
> (compatível com D-15); com o Desktop aberto, usar o loop `desktop-bridge`
> (validate → reload → screenshot).

## Matriz de casos

| ID | O que testar | Como | Critério de aceite |
|---|---|---|---|
| **H1** | Render em contexto real | Desktop com dados reais, `Show Raw HTML` **off**; screenshot via `desktop-bridge` | Página renderiza completa; nenhum elemento faltante ou desalinhado |
| **H2** | Escaping de texto do modelo | Injetar (ou localizar) registro com `&`, `<`, `>` no campo exibido | Markup íntegro; caracteres aparecem literais no texto |
| **H3** | Contexto vazio / total | Avaliar a medida com filtro que zera o contexto e no total da página | `noDataMessage` do visual ou guarda DAX (`IF ( ISEMPTY (…) )`); nunca HTML quebrado/parcial |
| **H4** | Locale pt-BR em CSS | Regex `: *\d+,\d+` sobre a string gerada (via `DEFINE MEASURE` + `EVALUATE`) | Zero ocorrências — número em CSS/atributo sempre `INT()`/`FORMAT` en-US |
| **H5** | Comprimento no pior caso | `EVALUATE ROW ( "len", LEN ( [Medida HTML] ) )` no contexto de maior cardinalidade real | Medida: sem teto prático (~2,1M empírico), mas > 100k = revisar densidade; **qualquer trecho vindo de coluna PQ**: < 32.766 |
| **H6** | Sanitização da lite | Abrir com a edição lite (GUID `…6865`); comparar com o HTML de origem | Nenhuma imagem/fonte externa esperada; nenhum elemento sumido por atributo `on*`; SVG sem `<use>`/`<foreignObject>` |
| **H7** | Export PDF/PPT | Exportar a página no Service (ou subscription de teste) | lite: visual renderizado no arquivo; standard: registrar pendência "sem export" no `TODO.md` |
| **H8** | Mobile (**obrigatório**) | App Power BI Mobile real (iOS/Android), layout portrait e landscape | Comportamento **sem documentação oficial** — aceite só com evidência (screenshot do app); falha = redesenho ou visual alternativo na visão mobile |
| **H9** | Performance e interatividade | Performance Analyzer (tempo de render do visual); com `sampling`: cross-filter, drillthrough, context menu; tooltips | Render aceitável no padrão da página (comparar com visuais nativos vizinhos); interações do cenário B funcionando; sem re-render perceptível em cross-filter |

## Receita — avaliar a medida sem abrir o Desktop (H2–H5)

```dax
DEFINE
    MEASURE Medidas[__TesteHtml] = [Home Página HTML]
EVALUATE
ROW (
    "len", LEN ( Medidas[__TesteHtml] ),
    "temVirgulaCss", "não confie só nisto — rodar a regex fora do DAX",
    "html", Medidas[__TesteHtml]
)
```

Exportar a coluna `html` e rodar a regex `: *\d+,\d+` (H4) e a inspeção de escaping (H2) fora do
DAX (editor/script). Para extension measures, o mesmo `DEFINE MEASURE` funciona com a expressão
embutida na query.

## Receita — comparação lite × standard (H6)

1. Registrar **temporariamente** os dois GUIDs em `publicCustomVisuals` e duplicar o visual com
   `visualType` de cada edição, lado a lado na página de rascunho.
2. Diferenças visíveis = dependência de recurso que a lite sanitiza → eliminar a dependência
   (base64/SVG inline) ou justificar a standard (SKILL.md § Decisão de edição).
3. Remover o visual e o GUID da edição descartada antes do gate (página de rascunho não vai para
   produção).

## Registro anti-drift (toda execução de QA)

Anotar no relatório de QA: edição + GUID + **versão do visual observada** (change log oficial em
`html-content.com/docs/change-log`; a UI do Desktop mostra a versão no "about" do visual). O
AppSource atualiza sem mudança no Git — a versão anotada é a única evidência para diagnosticar
regressão visual futura ("funcionava na 1.6.2").

## Pendências runtime padronizadas (copiar para o `TODO.md`)

- [ ] Primeira abertura no Desktop baixa o visual do AppSource (exige internet + AppSource liberado
      no tenant) — validar em máquina limpa
- [ ] H8 mobile pendente de teste em app real
- [ ] Drift de versão: sem pinning via AppSource (avaliar organizational store se o cliente exigir)
