---
name: figma-mockup
description: Traduz PRD + matriz de KPIs aprovados em mockup de dashboard, fiel aos recursos nativos do Power BI e ao grid PBIR. O renderizador padrao e HTML + SVG; Figma so quando o usuario pedir explicitamente. Use quando o agente figma-mockup-designer precisa gerar visual a partir de requisitos.
---

# Skill: Mockup de Dashboard (HTML + SVG)

## Quando usar
Após o Gate 4a (matriz de viabilidade aprovada) — o despacho pode ser antecipado em background, em paralelo à criação de medidas do 4b (o Gate 5 só abre após o 4b). Sempre antes da construção do relatório PBIR.

## Princípio: mapa primeiro, desenho depois
O mockup é um **preview fiel** do relatório que a Fase 6 vai construir — mesmo canvas (a **resolução vem no handoff de despacho**: 1280×720 → grid §4 do design system; 1920×1080 → grid §4B), mesmo grid e apenas visuais nativos do Power BI. Antes de desenhar qualquer frame, monte `docs/mockups/mapa-construcao.md` com a resolução e o tema declarados no cabeçalho; o mockup é a renderização do mapa, não uma criação livre.

## Renderizador: HTML + SVG e o padrao (D-07)
**Sempre gere o mockup em HTML + SVG.** Nao faca pre-check de Figma, nao peca autenticacao e nao
aborte a fase por indisponibilidade de Figma - o Figma deixou de ser o caminho padrao.

- **Layout da pagina:** HTML com elementos posicionados em coordenadas absolutas, identicas as do
  mapa de construcao (`left/top/width/height` em px dentro de um conteiner do tamanho exato da
  resolucao). Isso torna o mockup conferivel linha a linha contra o mapa.
- **Todo grafico e SVG inline** - barras, linhas, areas, combinados. Com eixo, gridlines em escala
  arredondada e rotulo de valor. Nunca use `<canvas>`, biblioteca de grafico externa, imagem
  rasterizada ou barra simulada com `div`.
- **Cartoes, tabelas, slicers e cabecalho** sao HTML/CSS; SVG e para a area de plotagem.
- Sem dependencia de rede: nada de CDN, fonte remota ou script externo. O arquivo tem de abrir
  offline com duplo clique.
- Fonte: pilha `"Segoe UI", system-ui, sans-serif` (e a fonte real do Power BI Desktop).

### Entregavel do renderizador
`docs/mockups/mockup.html` - **arquivo unico, autocontido**, com todas as paginas empilhadas em
rolagem vertical, cada uma no tamanho exato da resolucao, com legenda abaixo explicando as
decisoes de design daquela pagina.

Inclua o ajuste a janela: um pequeno script que escala cada pagina por
`transform: scale(larguraDisponivel / larguraDaResolucao)` e um botao que alterna para 100%.
Sem isso o mockup fica ilegivel em monitor menor que a resolucao alvo - e requisito, nao enfeite.

### Figma - apenas sob pedido explicito
So use Figma se o usuario pedir com todas as letras nesta execucao. Nesse caso, verifique o MCP
(tool `whoami`, tipicamente `mcp__plugin_figma_figma__whoami`; carregue via ToolSearch se deferred)
e **gere o HTML+SVG assim mesmo** - o HTML e o entregavel canonico; o Figma e adicional.
Atencao a cota: planos Starter esgotam em poucas chamadas de escrita. Se a cota estourar no meio,
termine o HTML e registre o Figma como parcial, sem trocar de renderizador no meio do caminho.

## Referências obrigatórias (ler antes de desenhar)
1. `.claude/skills/pbir/references/visual-design-system.md` §§1–4 — paleta, tipografia, configuração de página e grid com posições exatas (fonte canônica; não duplicada aqui).
2. `references/catalogo-visuais-pbi.md` (desta skill) — visuais permitidos (Bloco A), tabela de decisão pergunta → visual (Bloco B), visuais proibidos (Bloco C) e template do mapa de construção (Bloco D).

## Entrada
- `docs/levantamento-requisitos/requisitos-aprovados.md`
- `docs/dax/matriz-viabilidade.md`
- (opcional) `docs/apresentacoes-cliente/*.md` para narrativa
- (opcional) `docs/padroes-design/` — design system do cliente; quando existir, seus tokens substituem a paleta/tipografia de exemplo do design system

## Processo
1. Ler as referências obrigatórias acima.
2. Extrair lista de KPIs aprovados (status 🟢 e 🟡) da matriz de viabilidade.
3. Agrupar KPIs em 3 a 6 páginas lógicas (visão executiva, vendas detalhadas, geográfico, etc.), cada uma respondendo uma pergunta de negócio central.
4. **Montar `docs/mockups/mapa-construcao.md`** (template no Bloco D do catálogo): para cada página, escolher visuais pela tabela de decisão (Bloco B) e posições pela tabela "Posições exatas" do design system (§4). Desvios de posição exigem nota de justificativa no mapa.
5. **Renderizar `docs/mockups/mockup.html`** - uma pagina por bloco do mapa, posicoes absolutas
   identicas as do mapa, graficos em SVG inline, na resolucao do despacho (1280x720 ou 1920x1080).
   Para mais de 2 graficos, gere o HTML por script (Python) em vez de escrever a mao: as
   coordenadas saem consistentes entre as paginas e a manutencao fica barata.
6. Conferir o HTML contra o mapa, linha a linha (checklist de fidelidade abaixo).
7. Gravar `docs/mockups/mockup.md` com a paleta, os tokens propostos e a lista de paginas com os
   KPIs de cada uma.
8. (Somente se o usuario pediu Figma) criar o arquivo, capturar URL e screenshots, e gravar
   `docs/mockups/figma-url.md` e `docs/mockups/screenshots/`.

## Checklist de fidelidade (antes de encerrar a fase)
- [ ] Todo elemento do mockup tem linha correspondente no mapa de construção.
- [ ] Toda linha do mapa referencia medida com status 🟢/🟡 na matriz de viabilidade.
- [ ] Todos os frames têm exatamente a resolução definida no despacho (1280×720 ou 1920×1080), declarada no cabeçalho do mapa.
- [ ] Nenhum visual fora do Bloco A do catálogo.
- [ ] Todo gráfico é SVG inline, com eixo, gridlines e rótulo de valor.
- [ ] O HTML abre offline, sem requisição de rede.
- [ ] O ajuste à janela funciona: a página cabe em monitor menor que a resolução alvo.
- [ ] Dados fictícios estão declarados como tais; valores reais medidos no modelo vêm marcados.

## Saída
- `docs/mockups/mapa-construcao.md` (contrato Fase 5 → Fase 6)
- `docs/mockups/mockup.html` (**entregável canônico** - autocontido, HTML + SVG)
- `docs/mockups/mockup.md` (paleta, tokens propostos, páginas e KPIs)
- Somente sob pedido: `docs/mockups/figma-url.md` e `docs/mockups/screenshots/*.png`

## Anti-padrões
- Desenhar antes de montar o mapa de construção.
- Visual fora do Bloco A do catálogo ou presente na lista de proibidos (Bloco C): gauge, pie/donut, radar, sankey, word cloud, 3D, infográfico livre.
- Frame com dimensão diferente da resolução definida no despacho.
- Elemento fora das posições do grid sem justificativa registrada no mapa.
- Gerar mockup com KPI que ainda não tem medida DAX aprovada.
- Mockup que sugere interação inexistente no Power BI (busca livre, hover states elaborados, animações).
- Gráfico como `<canvas>`, imagem rasterizada, biblioteca externa ou barra simulada com `div` - todo gráfico é SVG inline.
- HTML que depende de CDN, fonte remota ou script externo: o mockup tem de abrir offline.
- Mockup em tamanho fixo sem ajuste à janela.
- Abortar a fase por Figma indisponível: o Figma não é mais pré-requisito de nada.
- Apresentar número fictício sem dizer que é fictício.
- Usar paleta/tipografia divergente do design system do cliente (se houver `docs/padroes-design/`).
- Assumir nomes de tool hardcoded sem verificar o prefixo real do servidor MCP na sessão.
