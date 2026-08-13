# Padrões HTML/CSS para o visual HTML Content — o que funciona no sandbox e biblioteca de padrões

> Todos os snippets seguem as convenções do SKILL.md: aspas simples nos atributos, cores por medida
> de token (`" & [Cor …] & "`), zero JavaScript, autossuficiência (base64/SVG inline). Números
> interpolados em CSS passam por `INT()`/`FORMAT en-US` (locale, D-22/D-23).

## 1. Matriz de sanitização — lite (certificada) × standard

| Recurso | lite | standard |
|---|---|---|
| `<style>` embutido / CSS inline | ✔ | ✔ |
| Flexbox, grid, `linear-gradient`, `border-radius`, `box-shadow`, `::after` | ✔ | ✔ |
| `@keyframes`, `transition`, `:hover` + `transform` | ✔ | ✔ |
| SMIL (SVG animado inline) | ✔ (desde 1.6.1) | ✔ |
| Imagem por data URI base64 (`image/png`, `image/svg+xml` desde 1.6.1) | ✔ | ✔ |
| Imagem por URL externa | ✖ (removida) | ✔ |
| Web fonts (`<link>` Google Fonts, `@import`, `@font-face`, `url()` externo) | ✖ | ✔ |
| `<video autoplay muted loop>` externo | ✖ | ✔ |
| Atributo `on*` (onclick etc.) | ✖ — **elemento inteiro descartado** | inerte (JS não roda) |
| `<script>`, `<use>`, `<foreignObject>` em SVG | ✖ removidos | inertes/não suportados |
| `expression()`, `attr()` em CSS | ✖ | — |
| Iframe | ✖ | só no Service, se o destino aceitar origem `null` (CORS); nunca no Desktop |
| Export PDF/PPT/subscription | ✔ | ✖ |

Regra de bolso: desenhe para a **lite**; cada linha "só standard" usada é uma justificativa a
registrar (SKILL.md § Decisão de edição).

## 2. Grade de KPI cards (flex-wrap)

Estrutura HTML gerada pela medida (esqueleto DAX completo no SKILL.md):

```html
<style>
  .kpiGrid { display: flex; gap: 16px; flex-wrap: wrap; font-family: 'Segoe UI', sans-serif; }
  .kpiCard { flex: 1 1 200px; border-radius: 12px; padding: 16px;
             box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .kpiCard:hover { transform: translateY(-4px); transition: transform 0.2s; }
</style>
<div class='kpiGrid'>
  <div class='kpiCard' style='background: {{CorFundoCard}}'>
    <div class='kpiTitulo'>Receita</div>
    <div class='kpiValor' style='color: {{CorPositiva}}'>R$ 12,3 mi</div>
  </div>
  <!-- 1 card por linha da dCardsConfig, via CONCATENATEX -->
</div>
```

Notas DAX: `{{…}}` é ilustrativo — na medida os pontos variáveis são concatenação com tokens
(`" & [Cor Positiva] & "`) e valores (`FORMAT(…, "pt-BR")`); o loop é `CONCATENATEX(dCardsConfig, …,
"", dCardsConfig[Ordem], ASC)`.

## 3. Landing page / welcome screen (hero + CTA falso)

```html
<style>
  .hero { height: 100%; display: flex; flex-direction: column; justify-content: center;
          align-items: center; text-align: center;
          background: linear-gradient(135deg, {{CorFundoPagina}}, {{CorDestaqueSuave}}); }
  .heroTitulo { font-size: 44px; font-weight: 700; letter-spacing: -1px; }
  .heroSub { font-size: 16px; color: {{CorTextoSuave}}; margin-top: 8px; }
  .cta { margin-top: 32px; padding: 14px 36px; border-radius: 999px;
         background: {{CorPositiva}}; color: {{CorTextoSobreDestaque}}; font-weight: 600; }
  .cta:hover { filter: brightness(1.08); transition: filter 0.15s; }
</style>
<div class='hero'>
  <div class='heroTitulo'>Painel Comercial</div>
  <div class='heroSub'>Atualizado em {{DataAtualizacao}}</div>
  <div class='cta'>Explorar indicadores</div>
</div>
```

O `.cta` é **desenho**: quem executa a navegação é o `actionButton` transparente sobreposto
(`references/binding-pbir-html.md` §6). `{{DataAtualizacao}}` vem de medida
(`FORMAT ( MAX ( dCalendario[Data] ), "dd/mm/yyyy", "pt-BR" )`).

## 4. Header de página (título + contexto de filtros)

```html
<style>
  .hdr { display: flex; justify-content: space-between; align-items: center;
         padding: 12px 20px; border-bottom: 2px solid {{CorTrilho}};
         font-family: 'Segoe UI', sans-serif; }
  .hdrTitulo { font-size: 20px; font-weight: 600; }
  .hdrPill { padding: 4px 12px; border-radius: 999px; font-size: 12px;
             background: {{CorFundoCard}}; color: {{CorTextoSuave}}; }
</style>
<div class='hdr'>
  <div class='hdrTitulo'>Vendas — Visão Mensal</div>
  <div class='hdrPill'>{{ContextoFiltro}}</div>
</div>
```

`{{ContextoFiltro}}` = medida com `SELECTEDVALUE`/`CONCATENATEX ( VALUES (…) )` descrevendo o filtro
ativo — padrão útil para dar feedback de slicers sem tooltip.

## 5. Flip-card (hover 3D, sem JS)

```html
<style>
  .flip { perspective: 800px; width: 220px; height: 140px; }
  .flipInner { position: relative; width: 100%; height: 100%;
               transition: transform 0.5s; transform-style: preserve-3d; }
  .flip:hover .flipInner { transform: rotateY(180deg); }
  .flipFace { position: absolute; inset: 0; backface-visibility: hidden;
              border-radius: 12px; display: flex; align-items: center; justify-content: center; }
  .flipVerso { transform: rotateY(180deg); background: {{CorDestaqueSuave}}; }
</style>
<div class='flip'><div class='flipInner'>
  <div class='flipFace' style='background: {{CorFundoCard}}'>R$ 12,3 mi</div>
  <div class='flipFace flipVerso'>Meta: R$ 15,0 mi</div>
</div></div>
```

Frente = valor; verso = detalhe (meta, variação). Funciona na lite (só CSS).

## 6. Lista com barras de progresso embutidas

```html
<div style='display: flex; align-items: center; gap: 8px'>
  <span style='width: 120px'>Regional Sul</span>
  <div style='flex: 1; height: 10px; border-radius: 5px;
              background: linear-gradient(to right,
                {{CorPositiva}} 0%, {{CorPositiva}} {{Pct}}%,
                {{CorTrilho}} {{Pct}}%, {{CorTrilho}} 100%)'></div>
  <span>{{PctRotulo}}</span>
</div>
```

`{{Pct}}` = `INT ( 100 * DIVIDE ( [Realizado], [Meta] ) )` — **inteiro** (locale!);
`{{PctRotulo}}` = `FORMAT ( DIVIDE ( [Realizado], [Meta] ), "0%", "pt-BR" )`. Uma linha por registro
via `CONCATENATEX` — ou o cenário B do binding (`sampling`) para ganhar cross-filter por linha.

## 7. Config table pattern (escala sem editar layout)

Tabela calculada de configuração (camada modelo, Fase 3/4):

```tmdl
	table dCardsConfig
		column Ordem
		column Titulo
		column Medida
		column DetalheRotulo
		partition dCardsConfig = calculated
			source = DATATABLE (
				"Ordem", INTEGER, "Titulo", STRING, "Medida", STRING, "DetalheRotulo", STRING,
				{ { 1, "Receita", "Receita", "vs. meta" }, { 2, "Margem", "Margem", "bruta" } }
			)
```

A medida HTML itera `dCardsConfig` com `CONCATENATEX` e resolve `[Medida]` (texto) via `SWITCH`
para a medida real — card novo = **linha nova na tabela**, zero edição de layout. O `SWITCH` é o
único ponto que cresce (uma linha por medida exposta).

## 8. Assets — imagens, ícones e fontes

- **SVG inline** é o default para ícone/ilustração: menor que base64, temável por token
  (`fill='" & [Cor Positiva] & "'`) e sobrevive à lite. Atenção: `<use>`/`<foreignObject>` são
  removidos na lite — SVG plano (paths diretos).
- **Base64** (`data:image/png;base64,…`) para logo/foto pequena; gerar com
  `[Convert]::ToBase64String([IO.File]::ReadAllBytes('logo.png'))` (PowerShell) e guardar num token
  de medida (`[Logo Cliente B64]`) — nunca colar o blob no meio do layout.
- **Fontes**: pilha segura `'Segoe UI', sans-serif` (fonte do tema PBI). Google Fonts só na
  standard (`<link>`/`@import`) e com justificativa — no Desktop + lite a fonte externa silenciosamente
  não carrega e o fallback assume.
- **Ícones tipográficos**: `UNICHAR(9650)` ▲ / `UNICHAR(9660)` ▼ / `UNICHAR(8226)` • dispensam SVG
  em indicadores simples.

## 9. CSS: object `stylesheet` vs `<style>` na medida

| Critério | `stylesheet` (visual.json) | `<style>` na medida DAX |
|---|---|---|
| Diff/versionamento | ✔ limpo, separado do DAX | mistura layout com dados |
| Formatação condicional | ✔ (binding a medida) | via lógica DAX |
| CSS depende de dados (cores por estado, larguras) | limitado | ✔ natural |
| Reuso entre visuais HTML da mesma página | manual (copiar) | manual |

Default do kit: **estrutura no `stylesheet`, dados no HTML** — a medida emite classes e valores; o
CSS estático mora no visual. `<style>` na medida quando o CSS é função do dado (ex.: keyframe com
`animation-duration` vindo de medida — padrão Workout Wednesday 2024-47).

## 10. Produtividade

1. Desenvolver o HTML num arquivo `.html` local (preview instantâneo no navegador — o render é o
   mesmo Chromium) com valores mockados `{{…}}`.
2. Transpor para DAX ao estabilizar: trocar `{{…}}` por concatenações; converter aspas duplas de
   atributos para simples; quebrar em `VAR` por região (CONFIG → DADOS → ELEMENTOS → MONTAGEM).
3. `SUBSTITUTE` como templating quando o mesmo bloco repete com poucos pontos variáveis:
   `SUBSTITUTE ( SUBSTITUTE ( __Template, "{{valor}}", __Valor ), "{{cor}}", [Cor Positiva] )`.
4. Depuração: propriedade **Show Raw HTML** do visual (mostra a string crua); comparar Desktop ×
   Service antes do gate (fontes/recursos externos divergem por edição).
5. Validar cedo o pior caso de volume (H5): `CONCATENATEX` sobre a maior cardinalidade real.
