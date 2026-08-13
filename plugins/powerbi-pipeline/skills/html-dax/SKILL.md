---
name: html-dax
description: >
  Use SEMPRE que o projeto pedir página HTML completa dentro do relatório Power BI — frases-gatilho:
  "página HTML", "landing page no Power BI", "welcome screen", "header rico", "cards HTML",
  "grade de KPI cards em HTML", "HTML Content", "medida HTML", "CSS no Power BI", "Markdown no
  relatório", "publicCustomVisuals". Também quando aparecer o sintoma "Can't display this visual.
  To see this custom visual, add it to this report first" ou HTML aparecendo como texto cru.
  Aplica-se às Fases 4 (medida), 6 (registro do visual + binding + stylesheet) e 7 (QA).
---

# Skill: Páginas HTML via DAX (visual HTML Content)

> **Preferência de plugin:** schemas PBIR em `pbip:pbir-format`; autoria DAX em `power-bi-dax`/`dax`.
> **Esta skill define as convenções e o processo DESTE kit por cima delas** — em conflito, esta skill
> vence. Fundamentação completa (fontes, divergências, verificação adversarial):
> `docs/pesquisa-html-power-bi.md` (D-23). Skill irmã para micro-gráficos em célula: `svg-dax` (D-22).

## Mecânica em uma linha

Medida DAX retorna a **string HTML completa** (texto puro, **sem `dataCategory`**) → data role
`content` do custom visual **HTML Content** → render em iframe sandbox (Chromium). Diferença central
vs. `svg-dax`: lá a string é data-URI + `dataCategory: ImageUrl` em visual nativo; aqui é HTML cru
num custom visual que precisa estar **registrado no `report.json`** (`publicCustomVisuals`).

## Quando usar / quando não usar — hierarquia obrigatória (D-23)

| # | Necessidade | Solução |
|---|---|---|
| 1 | KPI cards simples, hero image, reference labels | Card novo nativo (`cardVisual`, GA nov/2025) |
| 2 | Navegação/menu, botões com estados | Button slicer + bookmarks (nativo) |
| 3 | Micro-gráfico em célula/cartão/botão | `svg-dax` |
| 4 | Gráfico custom com interatividade própria | Deneb (`reports:deneb-visuals`) |
| 5 | Landing page/welcome screen, header rico, grade de cards com CSS moderno — layout que 1–4 não cobrem | **HTML Content (esta skill)** |

HTML por hábito é falha de revisão: só desça à linha 5 quando 1–4 não atendem, e registre o porquê
no handoff.

## Decisão de edição — por projeto, ANTES de desenhar (D-23)

| | **lite (padrão do kit)** | standard (exceção justificada) |
|---|---|---|
| GUID (`visualType` e `publicCustomVisuals`) | `htmlContent443BE3AD55E043BF878BED274D3A6865` | `htmlContent443BE3AD55E043BF878BED274D3A6855` |
| AppSource | `coacervolimited1596856650797.htmlcontent_certified` | WA200001930 |
| Certificado / export PDF-PPT / subscriptions | **Sim** | Não ("The visual does not support exporting") |
| Recursos externos (imagem URL, web fonts, `@import`, vídeo) | Não — sanitizados | Sim |
| Sanitização | Agressiva: elemento **inteiro** descartado se tiver atributo `on*`; `<use>`/`<foreignObject>`/`<script>` removidos de SVG; imagem só data URI (`image/svg+xml` aceito desde 1.6.1) | HTML/CSS/SVG plenos |

Standard só com justificativa registrada no `DECISIONS.md` do projeto + pendência "sem export
PDF/PPT" no `TODO.md`. Registrar também a **origem** do visual (AppSource vs. release standalone do
GitHub — GUIDs **diferentes**, standalone tem prefixo STANDALONE). Trocar de edição depois de
desenhar custa retrabalho: a sanitização da lite muda o que sobrevive no markup.

## Checklist de tenant (antes de prometer a página ao cliente)

Fase 1/proposta: confirmar (a) tenant setting "Add and use certified visuals only" — se ligado, só a
lite entra; (b) bloqueio de visuais AppSource/SDK ("Allow visuals created using the Power BI SDK",
Group Policy `EnableUncertifiedVisuals` no Desktop); (c) organizational store disponível (única via
de pinning de versão). Sem essas respostas, prometa layout nativo, não HTML.

## Regra "sem JavaScript" (nenhuma edição executa JS autoral)

- **Animação**: CSS `@keyframes`/`transition` (funcionam até na lite) + SMIL em SVG inline (1.6.1+).
- **Navegação**: botões nativos **transparentes** do Power BI sobrepostos aos botões desenhados no
  HTML + bookmarks/pageNavigation — receita em `references/binding-pbir-html.md`.
- **Interatividade de dados**: coluna no role `sampling` (UI "Sampling"; as docs do visual chamam de
  "Granularity") → cross-filter, drillthrough e context menu; classes `hover`/`unselected`; tooltips
  via `data-tooltip-title-*`/`data-tooltip-value-*`.
- **Hyperlinks**: só http/https, delegados ao Power BI ("Allow opening URLs", com prompt).
- **Proibidos por padrão**: iframes (não renderizam no Desktop; no Service dependem de CORS de
  origem `null`), cookies/localStorage, `<object>`, popups/modais.

## Onde a medida mora (D-23)

Default: tabela `Medidas` (D-17), nome de negócio + sufixo ` HTML` (ex.: `Home Página HTML`),
`displayFolder: 92. Páginas HTML`, descrição `///`, **sem `dataCategory`** — o visual recebe texto
puro; `dataCategory: ImageUrl` aqui é defeito. Cores **sempre** via medidas de token (pasta
`91. Cores`, compartilhada com o SVG) — hex literal em medida HTML é falha de revisão. Extension
measure segue o caminho secundário delimitado da D-22 (mesmas regras, sem o campo `dataCategory`).
HTML **nunca** por coluna importada via Power Query — teto de 32.766 caracteres com truncamento
silencioso; medida DAX vai a ~2,1 milhões (empírico); conteúdo grande vindo de dados → chunking em
linhas < 32.766 + remontagem com `CONCATENATEX`.

## Esqueleto TMDL (Fase 4)

````tmdl
	/// Página HTML de cards de KPI (Home). Renderiza no visual HTML Content (lite). Texto puro — sem dataCategory.
	measure 'Home Página HTML' = ```
			VAR __Css =
			    "<style>" &
			    ".kpiGrid { display: flex; gap: 16px; flex-wrap: wrap; font-family: 'Segoe UI', sans-serif; } " &
			    ".kpiCard { flex: 1 1 200px; border-radius: 12px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); } " &
			    ".kpiCard:hover { transform: translateY(-4px); transition: transform 0.2s; } " &
			    ".kpiTitulo { font-size: 12px; color: " & [Cor Texto Suave] & "; } " &
			    ".kpiValor { font-size: 24px; font-weight: 600; }" &
			    "</style>"
			VAR __Cards =
			    CONCATENATEX (
			        dCardsConfig,
			        "<div class='kpiCard' style='background: " & [Cor Fundo Card] & "'>" &
			            "<div class='kpiTitulo'>" & SUBSTITUTE ( SUBSTITUTE ( SUBSTITUTE ( dCardsConfig[Titulo], "&", "&amp;" ), "<", "&lt;" ), ">", "&gt;" ) & "</div>" &
			            "<div class='kpiValor' style='color: " & [Cor Positiva] & "'>" &
			                SWITCH (
			                    dCardsConfig[Medida],
			                    "Receita", FORMAT ( [Receita Bruta], "R$ #,0,,.0 "" mi""", "pt-BR" ),
			                    "Margem", FORMAT ( [Margem Bruta %], "0.0%", "pt-BR" )
			                ) &
			            "</div>" &
			        "</div>",
			        "",
			        dCardsConfig[Ordem], ASC
			    )
			RETURN
			    __Css & "<div class='kpiGrid'>" & __Cards & "</div>"
			```
		formatString: "General"
		displayFolder: 92. Páginas HTML
		lineageTag: <GUID-novo>
````

Convenções fixas (não improvisar): **aspas simples nos atributos** (`style='...'` — evita escapar as
aspas duplas do DAX); texto vindo do modelo escapado com `SUBSTITUTE` na ordem `&` → `<` → `>`
(primeiro o `&`!); números interpolados em CSS/atributos via `INT()` ou
`FORMAT ( x, "0.0#", "en-US" )` e rótulos via `FORMAT ( v, fmt, "pt-BR" )` — mesma regra de locale
da D-22 (vírgula decimal pt-BR quebra valor CSS sem erro visível); dados repetidos via
`CONCATENATEX` sobre tabela de configuração + `SWITCH` para resolver medidas por nome (card novo =
linha nova, sem editar layout); `UNICHAR()`/SVG inline para ícones; medida HTML **embrulha medidas
base aprovadas** (D-04) — nunca esconde lógica de negócio nova; CSS estrutural preferencialmente no
object `stylesheet` do visual (diff limpo, aceita formatação condicional) e `<style>` na medida só
quando o CSS depende de dados; estrutura VAR nas regiões CONFIG → DADOS → ELEMENTOS → MONTAGEM.

## Binding PBIR (Fase 6) — 2 passos

| Passo | Arquivo | O quê |
|---|---|---|
| 1 | `definition/report.json` | GUID da edição no array `publicCustomVisuals` — sem ele: "Can't display this visual…" |
| 2 | `pages/<pg>/visuals/<id>/visual.json` | `visualType` = GUID; medida em `queryState.content.projections`; coluna em `sampling` para grade por linha; objects `contentFormatting` / `stylesheet` / `crossFilter` |

Medida do modelo: `SourceRef` **sem** `Schema`; extension measure: `"Schema": "extension"` (o
`queryRef` continua `Medidas.Nome`). JSONs completos por cenário (página única, grade por
Granularity, tooltip) + receita dos botões transparentes: `references/binding-pbir-html.md`.
Pendências runtime: a 1ª abertura no Desktop **baixa o visual do AppSource** (exige internet +
AppSource liberado); **sem pinning de versão** (auto-update → drift) — registrar ambas no `TODO.md`.

## Erros comuns (sintoma → causa)

| Sintoma | Causa |
|---|---|
| "Can't display this visual. To see this custom visual, add it to this report first" | GUID ausente do `publicCustomVisuals` — ou edição trocada (lite vs standard) |
| HTML aparece como texto cru | Medida ligada a visual nativo em vez do HTML Content — ou "Show Raw HTML" ligado |
| Render estranho de tags | `contentFormatting.format` = `markdown` com conteúdo HTML (ou vice-versa) |
| Imagem some só na lite | URL externa sanitizada — converter para base64/SVG inline |
| Elemento inteiro some na lite | Atributo `on*` presente — a sanitização descarta o elemento todo |
| Fonte/estilo diverge entre Desktop e Service | Web font externa (só standard renderiza) ou fallback — fixar pilha `'Segoe UI', sans-serif` |
| Valor CSS ignorado, layout torto | Vírgula decimal pt-BR em número interpolado — `INT()`/`FORMAT` en-US |
| Visual em branco no export PDF/PPT | Edição standard não exporta — trocar para lite ou aceitar pendência |
| Iframe em branco no Desktop | Iframe nunca renderiza no Desktop (e é proibido por padrão — D-23) |
| Página quebra com dado contendo `&`/`<` | Escaping ausente (`SUBSTITUTE` na ordem `&` → `<` → `>`) |

## Validação (obrigatória antes de fechar gate)

Mínimo no gate 4b: **H1** render em contexto real, **H2** escaping, **H3** contexto vazio/total,
**H4** locale (regex `: *\d+,\d+` no CSS gerado = zero), **H5** comprimento. Fases 6/7: **H6**
sanitização lite, **H7** export, **H8** mobile (obrigatório — comportamento sem documentação
oficial), **H9** performance/interatividade + loop `desktop-bridge` (validate → reload →
screenshot). Medida testável sem tocar o modelo via `DEFINE MEASURE` (D-15). Matriz completa e
receitas: `references/validacao-html.md`.

## Checklist de encerramento

- [ ] Hierarquia de escolha (1–4 antes do HTML) percorrida e justificada no handoff
- [ ] Edição decidida ANTES do design e registrada no `DECISIONS.md` do projeto (GUID + origem);
      standard → pendência de export no `TODO.md`
- [ ] Medida na tabela `Medidas` com sufixo ` HTML`, `displayFolder: 92. Páginas HTML`,
      **sem `dataCategory`**, descrição `///`
- [ ] Cores só via tokens (`91. Cores`); escaping; locale en-US em números CSS; guarda de contexto
      vazio ou `noDataMessage`
- [ ] Rastreabilidade: medida HTML entra na coluna Visual/Página das **mesmas linhas** dos KPIs que
      exibe (embrulha só medidas base aprovadas, D-04); página puramente estrutural não cria KPI
- [ ] Validação H1–H5 anexada ao gate 4b; H6–H9 nas Fases 6/7; screenshot via `desktop-bridge`
      quando disponível
- [ ] Pendências runtime no `TODO.md` (download do visual na 1ª abertura, teste mobile, drift de
      versão do AppSource); CHANGELOG conforme o modo (pipeline: orquestrador grava; avulso/manual:
      você grava)
