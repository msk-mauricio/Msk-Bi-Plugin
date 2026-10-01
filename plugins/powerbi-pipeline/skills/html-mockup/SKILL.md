---
name: html-mockup
description: Traduz PRD + matriz de KPIs aprovados em mockup de dashboard em HTML/SVG autocontido (docs/mockups/), fiel aos recursos nativos do Power BI e ao grid PBIR, junto com o mapa-construcao.md que a Fase 6 consome. Padrao da Fase 5 (D-24); Figma so sob pedido explicito do usuario. Use quando o agente html-mockup-designer precisa gerar o mockup a partir dos requisitos.
---

# Skill: Mockup de Dashboard em HTML/SVG (Fase 5)

## Quando usar
Após o Gate 4a (matriz de viabilidade aprovada). O despacho pode ser antecipado em background, em paralelo à criação de medidas do 4b; o Gate 5 só abre depois do 4b. Sempre antes da construção do relatório PBIR (Fase 6).

## Princípio: mapa primeiro, desenho depois (D-16)
O mockup é um **preview fiel** do relatório que a Fase 6 vai construir: mesmo canvas, mesmo grid e apenas visuais nativos do Power BI. A **resolução vem no handoff de despacho**: 1280×720 → grid §4 do design system; 1920×1080 → grid §4B. Antes de desenhar qualquer página, monte `docs/mockups/mapa-construcao.md` com a resolução e o tema no cabeçalho. O HTML é a renderização do mapa, não uma criação livre.

## Padrão: HTML/SVG autocontido (D-24)
**Sempre gere o mockup em HTML/SVG.** Não há pré-check de Figma, autenticação nem fallback: o renderizador só depende de escrita de arquivo. Indisponibilidade de Figma nunca é motivo para abortar a fase.

### Estrutura de arquivos (tudo em `docs/mockups/`)
- **Modo A (padrão, até ~6 páginas):** `index.html` único, com uma `<section>` por página do relatório, empilhadas em rolagem vertical.
- **Modo B (muitas páginas ou páginas pesadas):** um arquivo por página (`pagina-01-<slug>.html`, `pagina-02-<slug>.html`, …) mais um `index.html` com a navegação e a lista de páginas. Os arquivos de página seguem as mesmas regras do Modo A.
- `index.html` é sempre o ponto de entrada e o **entregável canônico** do Gate 5.

### Fidelidade ao canvas PBIR
- Cada página é um contêiner com o tamanho **exato** da resolução em px (`width:1280px;height:720px` ou `1920px × 1080px`), `position:relative; overflow:hidden`, com o fundo da página do tema.
- Cada visual é um elemento `position:absolute` com `left/top/width/height` **idênticos** aos x/y/w/h da linha correspondente no mapa. Anote os valores em atributos de dados, para a conferência ser mecânica:
  ```html
  <div class="visual" data-id="P1-03" data-tipo="lineChart"
       data-x="30" data-y="178" data-w="600" data-h="240"
       style="left:30px;top:178px;width:600px;height:240px">…</div>
  ```
- Botão **"Mostrar grid"**: sobrepõe o grid do design system e exibe em cada visual uma etiqueta `P1-03 · lineChart · 30,178,600,240`. Desligado por padrão.
- Só tipos de visual do **Bloco A** do catálogo (`references/catalogo-visuais-pbi.md`), cada um desenhado como o Power BI o renderiza (container com título, padding, cantos e sombra do tema; cartão com rótulo e valor; slicer dropdown com rótulo de negócio; tabela com cabeçalho do tema). Nada que o PBIR não consiga construir.
- **Tema/paleta do cliente:** tokens do handoff (theme.json ou identidade visual) viram variáveis CSS em `:root` (`--cor-primaria`, `--cor-texto`, `--fundo-pagina`, `--serie-1…n`). Sem tema definido, use a paleta do design system da skill `pbir` e registre isso no cabeçalho do mapa.
- Fonte: `"Segoe UI", system-ui, sans-serif` (a fonte real do Power BI), com os tamanhos da tabela de tipografia do design system para a resolução escolhida.

### Gráficos em SVG inline
- Todo gráfico (barras, colunas, linha, área, combinado, dispersão) é **SVG inline** dentro do visual, com `viewBox` igual à área de plotagem. Nunca `<canvas>`, imagem rasterizada, biblioteca de gráfico ou barra simulada com `div`.
- Siga as regras SWD da skill `dataviz-powerbi`: rótulos de dados ligados (e então sem eixo de valores nem gridlines), escala arredondada, cinza para contexto e uma cor forte para o foco, títulos narrativos.
- **Dados:** use valores reais quando houver fonte disponível (por exemplo, `EVALUATE` via MCP com o Desktop aberto) e marque-os como reais. Caso contrário, use dados fictícios **plausíveis** (ordem de grandeza, sazonalidade e categorias coerentes com o negócio) e declare no rodapé de cada página: "Dados fictícios para validação de layout".
- Para mais de 2 gráficos, gere o HTML por script (Python ou Node, a partir do mapa) em vez de escrever à mão: as coordenadas ficam consistentes entre as páginas e a manutenção fica barata. O script é auxiliar; o entregável é o HTML.

### Autocontido
- Sem dependências externas: CSS e JS inline, SVG inline, nenhuma fonte remota, nenhuma requisição de rede. O arquivo abre offline, com duplo clique.
- Exceção só se for imprescindível: bibliotecas via `cdnjs.cloudflare.com` ou `cdn.jsdelivr.net`, registradas como risco no handoff. **Nunca** para desenhar gráficos: gráfico é sempre SVG inline.
- JS mínimo, só para: ajuste à janela, botão "Mostrar grid" e navegação entre páginas.
- **Ajuste à janela (obrigatório):** cada página escala por `transform: scale(larguraDisponivel / larguraDaResolucao)` com `transform-origin: top left`, mais um botão que alterna para 100%. Sem isso o mockup fica ilegível em monitor menor que a resolução alvo.
- **Página única para screenshot:** `index.html#p2` mostra só a página 2, em 100%, sem barra de controles. Isso permite capturar uma imagem por página em modo headless.
- Não sugira interações que o Power BI não tem: busca livre, hover elaborado, animações, drill customizado.

### Legenda por página
Abaixo de cada página (fora do canvas), um bloco curto: pergunta de negócio central, KPIs cobertos (medidas 🟢/🟡) e decisões de design da página.

## Referências obrigatórias (ler antes de desenhar)
1. Skill `pbir`, `references/visual-design-system.md` §§1–4 e §4B: paleta, tipografia, configuração de página e grid com posições exatas. É a fonte canônica; não duplique aqui.
2. `references/catalogo-visuais-pbi.md` (desta skill): visuais permitidos (Bloco A), tabela de decisão pergunta → visual (Bloco B), visuais proibidos (Bloco C) e template do mapa de construção (Bloco D).

## Entrada
- `docs/levantamento-requisitos/requisitos-aprovados.md`
- `docs/dax/matriz-viabilidade.md` (apenas KPIs 🟢/🟡)
- Handoff de despacho com **resolução** (1280×720 ou 1920×1080) e **tema/paleta**
- (opcional) `docs/apresentacoes-cliente/*.md`, para a narrativa
- (opcional) `docs/padroes-design/`: design system do cliente; quando existir, seus tokens substituem a paleta e a tipografia de exemplo

## Processo
1. Ler as referências obrigatórias.
2. Extrair os KPIs 🟢/🟡 da matriz de viabilidade.
3. Agrupar os KPIs em 3 a 6 páginas lógicas, cada uma respondendo a uma pergunta de negócio central.
4. **Montar `docs/mockups/mapa-construcao.md`** (template no Bloco D do catálogo): cabeçalho com tema e resolução; por página, visual, tipo nativo, medidas, campos e x/y/w/h. Visuais pela tabela de decisão (Bloco B), posições pela tabela "Posições exatas" do design system. Desvio de posição exige nota de justificativa no mapa.
5. **Renderizar `docs/mockups/index.html`** (Modo A ou B), com as posições idênticas às do mapa e os gráficos em SVG inline.
6. Conferir o HTML contra o mapa, linha a linha: cada `data-id` do HTML tem linha no mapa e vice-versa, com o mesmo x/y/w/h.
7. **Screenshots (opcional):** se houver navegador headless disponível, capture uma imagem por página em `docs/mockups/screenshots/pagina-NN.png`, no tamanho exato da resolução. Por exemplo, com Edge ou Chrome: `msedge --headless=new --window-size=1280,720 --screenshot=<png> "file:///<caminho>/index.html#p1"`, ou Playwright se estiver instalado. Sem navegador, pule este passo e registre no handoff; não bloqueia o gate.
8. Gravar `docs/mockups/mockup.md`: paleta e tokens propostos, lista de páginas com os KPIs de cada uma, e indicação de quais dados são fictícios e quais são reais.

## Evidência para o Gate 5
- Caminho do `docs/mockups/index.html` (e dos arquivos de página, no Modo B), para o usuário abrir no navegador.
- Screenshots em `docs/mockups/screenshots/`, quando capturados.
- Resultado da conferência HTML × mapa (quantidade de visuais por página, divergências = 0).

## Checklist de fidelidade (antes de encerrar a fase)
- [ ] Todo visual do HTML tem linha correspondente no mapa, com o mesmo x/y/w/h, e vice-versa.
- [ ] Toda linha do mapa referencia medida 🟢/🟡 na matriz de viabilidade.
- [ ] Toda página tem exatamente a resolução do despacho, declarada no cabeçalho do mapa.
- [ ] Nenhum visual fora do Bloco A do catálogo.
- [ ] Todo gráfico é SVG inline, seguindo as regras SWD (rótulos de dados, escala arredondada).
- [ ] Tema/paleta aplicados via variáveis CSS; nenhuma cor solta fora dos tokens.
- [ ] O HTML abre offline, sem requisição de rede (ou só CDN permitida, registrada como risco).
- [ ] O ajuste à janela, o "Mostrar grid" e o `#pN` funcionam.
- [ ] Dados fictícios declarados como tais; valores reais marcados.

## Saída
- `docs/mockups/mapa-construcao.md`: contrato Fase 5 → Fase 6 (D-16)
- `docs/mockups/index.html`: **entregável canônico** (mais `pagina-NN-<slug>.html` no Modo B)
- `docs/mockups/mockup.md`: paleta, tokens, páginas e KPIs
- `docs/mockups/screenshots/pagina-NN.png`: opcional

## Figma (opcional, sob pedido)
Figma só entra se o usuário pedir explicitamente nesta execução, e **como adicional**: o HTML/SVG e o mapa continuam sendo gerados e continuam canônicos. Nesse caso, quem faz a cópia é a sessão principal (o subagente `html-mockup-designer` não tem MCP do Figma): depois do handoff, ela verifica as tools MCP do Figma disponíveis (carregando via ToolSearch se estiverem deferred), reproduz as páginas a partir do mesmo mapa e grava `docs/mockups/figma-url.md`. Se o MCP estiver indisponível ou a cota estourar, termine o HTML, registre o Figma como pendente no handoff e siga; nunca troque de renderizador no meio da execução.

## Anti-padrões
- Desenhar antes de montar o mapa de construção.
- Visual fora do Bloco A ou presente na lista de proibidos (Bloco C): gauge, pie/donut, radar, sankey, word cloud, 3D, infográfico livre.
- Página com dimensão diferente da resolução do despacho, ou visual sem `data-x/y/w/h`.
- Visual fora das posições do grid sem justificativa registrada no mapa.
- KPI sem medida 🟢/🟡 na matriz de viabilidade.
- Gráfico como `<canvas>`, imagem, biblioteca externa ou barra de `div`.
- Dependência de rede sem necessidade (CDN, fonte remota, script externo).
- Mockup em tamanho fixo, sem ajuste à janela.
- Número fictício apresentado sem aviso.
- Paleta ou tipografia divergentes do tema do cliente (ou de `docs/padroes-design/`, se houver).
- Tratar Figma como pré-requisito ou abortar a fase por falta dele.
