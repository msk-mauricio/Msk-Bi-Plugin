---
name: figma-mockup
description: Traduz PRD + matriz de KPIs aprovados em mockup de dashboard no Figma, fiel aos recursos nativos do Power BI e ao grid PBIR. Use quando o agente figma-mockup-designer precisa gerar visual a partir de requisitos.
---

# Skill: Figma Mockup

## Quando usar
Após o Gate 4a (matriz de viabilidade aprovada) — o despacho pode ser antecipado em background, em paralelo à criação de medidas do 4b (o Gate 5 só abre após o 4b). Sempre antes da construção do relatório PBIR.

## Princípio: mapa primeiro, desenho depois
O mockup é um **preview fiel** do relatório que a Fase 6 vai construir — mesmo canvas (a **resolução vem no handoff de despacho**: 1280×720 → grid §4 do design system; 1920×1080 → grid §4B), mesmo grid e apenas visuais nativos do Power BI. Antes de desenhar qualquer frame, monte `docs/mockups/mapa-construcao.md` com a resolução e o tema declarados no cabeçalho; o mockup é a renderização do mapa, não uma criação livre.

## Pré-condição — verificação do Figma MCP (D-07)
Os nomes das tools MCP do Figma variam por instalação (prefixo `mcp__plugin_figma_figma__*` quando via plugin, ou outro prefixo se conectado como servidor MCP). Verificar de forma agnóstica ao prefixo:

1. Localizar a tool `whoami` do servidor MCP do Figma disponível na sessão (tipicamente `mcp__plugin_figma_figma__whoami`). Se as tools estiverem deferred, carregá-las via ToolSearch primeiro.
2. Chamar a `whoami` — se responder com usuário autenticado, ok.
3. Se não houver servidor Figma ou a `whoami` falhar por falta de autenticação, **abortar a fase** com instruções claras (rodar `/mcp` e autenticar o Figma) e recomendar o fallback textual via agente `client-presentation`.

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
5. Criar o arquivo no Figma com a tool `create_new_file` do servidor Figma (tipicamente `mcp__plugin_figma_figma__create_new_file`) ou, se preferir geração assistida, invocar a skill `figma:figma-generate-design` (nome de skill, não de tool) com prompt detalhado por página — sempre **1 frame por página na resolução do despacho** (1280×720 ou 1920×1080), elementos nas posições do mapa, paleta e tipografia do design system aplicável.
6. Capturar URL do arquivo Figma criado.
7. Exportar thumbnails de cada página via a tool `get_screenshot` do servidor Figma.
8. Gravar `docs/mockups/figma-url.md` com URL, paleta e lista de páginas.
9. Gravar thumbnails em `docs/mockups/screenshots/`.

## Checklist de fidelidade (antes de encerrar a fase)
- [ ] Todo elemento do mockup tem linha correspondente no mapa de construção.
- [ ] Toda linha do mapa referencia medida com status 🟢/🟡 na matriz de viabilidade.
- [ ] Todos os frames têm exatamente a resolução definida no despacho (1280×720 ou 1920×1080), declarada no cabeçalho do mapa.
- [ ] Nenhum visual fora do Bloco A do catálogo.

## Saída
- `docs/mockups/mapa-construcao.md` (contrato Fase 5 → Fase 6)
- `docs/mockups/figma-url.md` (estrutura: URL + paleta + lista de páginas + KPIs por página)
- `docs/mockups/screenshots/*.png`

## Anti-padrões
- Desenhar antes de montar o mapa de construção.
- Visual fora do Bloco A do catálogo ou presente na lista de proibidos (Bloco C): gauge, pie/donut, radar, sankey, word cloud, 3D, infográfico livre.
- Frame com dimensão diferente da resolução definida no despacho.
- Elemento fora das posições do grid sem justificativa registrada no mapa.
- Gerar mockup com KPI que ainda não tem medida DAX aprovada.
- Mockup que sugere interação inexistente no Power BI (busca livre, hover states elaborados, animações).
- Usar paleta/tipografia divergente do design system do cliente (se houver `docs/padroes-design/`).
- Assumir nomes de tool hardcoded sem verificar o prefixo real do servidor MCP na sessão.
