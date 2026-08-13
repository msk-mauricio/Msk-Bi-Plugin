# Publicação da Documentação no Notion

Processo para levar a documentação técnica de um projeto Power BI para o workspace Notion da MSK Code (workspace "Mskcode", `mauricio@mskcode.com.br`), replicando a estrutura mantida pela skill `documentacao-tecnica-powerbi` (não instalada em todo ambiente — quando ausente, siga este documento com as ferramentas MCP do Notion diretamente).

Use esta etapa quando o usuário pedir para "levar para o Notion", "publicar no Notion", "sincronizar documentação no Notion", ou mencionar a skill `documentacao-tecnica-powerbi`.

## 0. Pré-requisito

O conector MCP `claude.ai Notion` precisa estar autorizado na sessão. As ferramentas relevantes (podem estar deferidas — carregar via `ToolSearch` antes de chamar):

- `mcp__claude_ai_Notion__notion-fetch` (ler página/database/data source; `id: "self"` identifica workspace/usuário conectado)
- `mcp__claude_ai_Notion__notion-search`
- `mcp__claude_ai_Notion__notion-create-database`
- `mcp__claude_ai_Notion__notion-create-pages`
- `mcp__claude_ai_Notion__notion-update-page`

Sempre ler o recurso `notion://docs/enhanced-markdown-spec` (via `notion-fetch`) antes de escrever conteúdo, se ainda não tiver sido lido na sessão — a sintaxe Notion-flavored Markdown diverge de Markdown padrão em pontos importantes (ver Seção 5).

## 1. Descobrir a estrutura existente

Antes de criar qualquer coisa, localizar o hub central. Ele fica em:

```
MSK Code — Visão Geral Institucional
  └── 📁 Projetos & Documentação Técnica — Power BI
        ├── 📐 Templates & Padrões DAX          (estrutura padrão + padrões de DAX consolidados)
        ├── Database "<Cliente A>"               (uma por cliente)
        ├── Database "<Cliente B>"
        └── ...
```

Buscar com `notion-search` (query = nome do cliente, ex. "Baldo") e, se vazio, buscar a página "Projetos & Documentação Técnica — Power BI" para listar as databases de cliente existentes (ela lista todas no corpo). **Nunca presumir que a database do cliente já existe** — muitos clientes locais (pasta do repositório) ainda não têm database no Notion.

## 2. Database por cliente (criar se não existir)

Schema padrão (idêntico em todas as databases de cliente existentes — Ganzerla, Ceat, Parks, Pão d'Gula etc.):

```sql
CREATE TABLE (
  "Projeto" TITLE,
  "Cliente" RICH_TEXT,
  "Consultor" RICH_TEXT,
  "Status" SELECT('Em desenvolvimento':yellow, 'Concluído':green, 'Manutenção':blue),
  "Versão Atual" RICH_TEXT,
  "Última Atualização" DATE
)
```

Criar com `notion-create-database`, `parent: {type: "page_id", page_id: "<id da página 'Projetos & Documentação Técnica — Power BI'>"}`, `title` = nome do cliente (ex. "Baldo"). Guardar o `data_source_id` (`collection://...`) retornado — é o parent usado no próximo passo.

## 3. Página do projeto (uma linha da database)

Criar com `notion-create-pages`, `parent: {type: "data_source_id", data_source_id: "<...>"}`:

- `icon`: `📊`
- `properties`: `Projeto` (título do projeto, ex. "Comercial Soja"), `Cliente`, `Consultor` (nome do consultor responsável, ex. "Maurício"), `Status` (`"Concluído"` para uma primeira documentação completa recém-gerada; `"Em desenvolvimento"` se o projeto ainda está em andamento; `"Manutenção"` para projetos já entregues em ciclo de evolução), `Versão Atual` (ex. `"v1.0"`), `date:Última Atualização:start` (ISO `YYYY-MM-DD`, com `date:Última Atualização:is_datetime: 0`).
- `content`: 1-2 parágrafos curtos descrevendo o projeto (mesmo teor da Visão Geral, resumido) + a linha fixa **"A documentação técnica de cada versão fica nas sub-páginas abaixo (nunca no corpo desta página)."** — o corpo desta página nunca deve conter o detalhamento técnico.

## 4. Sub-página(s) de documentação técnica

Criar com `notion-create-pages`, `parent: {type: "page_id", page_id: "<id da página do projeto criada acima>"}`, `icon: "📄"`, título `"Documentação Técnica v{X.Y}"`.

Estrutura de conteúdo — **sempre estas 6 seções, nesta ordem** (mesma usada em todos os projetos existentes; ver `📐 Templates & Padrões DAX`):

1. **Visão Geral do Projeto** — contexto de negócio, objetivo, escopo, público-alvo.
2. **Modelo de Dados** — tabelas fato/dimensão, relacionamentos-chave, padrões de modelagem não óbvios.
3. **Medidas DAX Documentadas** — organizadas por pasta de exibição/tabela. Medidas com lógica de negócio relevante trazem a fórmula real (lida do `.tmdl`, nunca inventada) dentro de um bloco `<details><summary>...</summary>...```javascript ... ```...</details>`; medidas triviais (constantes, contagens simples) são só listadas por nome em uma linha "Demais: ...".
4. **Problemas Identificados e Correções** — cada item como `<details>` com Problema/Causa/Escopo do impacto/Status (`sinalizado, não corrigido` | `corrigido` | `mantido a pedido`). Preferir apontar bugs reais encontrados na leitura do DAX (ex. medida cujo nome não bate com o que o `RETURN` calcula) além das pendências já levantadas na Fase 8 local.
5. **Decisões Técnicas e Padrões Aplicados** — lista com bullets dos padrões de modelagem/DAX não óbvios (parameter tables + SWITCH, USERELATIONSHIP, guardas DIVIDE(...,0), etc.).
6. **Changelog de Versão** — tabela Notion (`<table header-row="true">`) com colunas Versão/Data/O que mudou.

Use `{color="blue"}` nos headings H1 (mesmo padrão visual dos projetos existentes) e um quote-block (`>`) no topo com `**Cliente:** ... · **Projeto:** ... · **Versão:** ... · **Consultor:** ... · **Data:** ...`.

### Se o projeto já tiver versões anteriores documentadas

Quando a "Versão Atual" mudar (v1.0 → v1.1 etc.) em um projeto que já existe no Notion, **não sobrescrever** a página "Documentação Técnica" anterior de forma destrutiva:
- Renomear/transformar em **"📄 Documentação Técnica — Modelo Completo"** (página viva, sempre atualizada com o estado atual do modelo), e
- Criar uma sub-página **🏷️ vX.Y** por versão, com só "o que mudou nesta versão" (medida nova, análise feita, pendência sinalizada) — não repetir o modelo inteiro.

## 5. Guia de Uso (opcional, sob pedido)

Se o usuário pedir para levar também o guia de uso / manual do usuário final (`docs/documentacao/guia-uso.md` local), criar como sub-página irmã da Documentação Técnica, `icon: "📘"`, título **"Guia de Uso"**, `parent` = mesma página do projeto (não da doc técnica). Conteúdo: navegação, filtros/slicers, interpretação de visuais, drill-through, boas práticas — linguagem para usuário de negócio, não para manutenção do modelo. Vale destacar ali, com `⚠️`, qualquer bug de medida já registrado na doc técnica que possa induzir o usuário final a erro de leitura.

## 5.1 Espelhar todos os arquivos `.md` de `docs/documentacao/` (sob pedido)

Se o usuário pedir para subir/espelhar **todos** os arquivos `.md` da pasta de documentação local (não só a versão condensada de 6 seções), tratar como um entregável de referência **complementar** à `Documentação Técnica v{X.Y}` — não substitui a versão condensada, que continua sendo a leitura executiva/curada.

Processo:

1. Listar os arquivos com `Glob` em `docs/documentacao/*.md` (ou `DOCS/documentacao/*.md`, conforme a convenção de pasta do projeto — nem todo projeto usa `docs/` minúsculo).
2. Criar uma sub-página guarda-chuva, `icon: "📚"`, título **"Documentação Completa (arquivos .md)"**, `parent` = página do projeto (irmã de "Documentação Técnica" e "Guia de Uso"). Corpo: 1 parágrafo explicando que é espelho fiel dos arquivos locais, com tabelas convertidas para o formato Notion.
3. Para cada arquivo (exceto `guia-uso.md`, que já tem página própria — ver Seção 5), criar uma sub-página filha dessa guarda-chuva, `parent: {type: "page_id", page_id: "<id da guarda-chuva>"}`, com título derivado do nome do arquivo (ex. `documentacao-tecnica.md` → "Documentação Técnica — Completa"; `catalogo-medidas-dax.md` → "Catálogo de Medidas DAX — Completo"; `pendencias-conhecidas.md` → "Pendências Conhecidas — Completo"; `release-notes.md` → "Release Notes"; `documentacao-funcional.md` → "Documentação Funcional"). Pode criar as várias páginas filhas em uma única chamada de `notion-create-pages` (até 100 páginas por chamada, mesmo `parent` para todas).
4. **Converter toda tabela Markdown (`| col | col |`) para o formato nativo `<table header-row="true"><tr><td>...</td></tr>...</table>`** — o Notion-flavored Markdown não tem um parser de tabela estilo GFM; tabelas em pipe viram texto solto/paragráfos quebrados se enviadas como estão. Preservar o conteúdo literal de cada célula (não resumir/cortar linhas) — o objetivo desta cópia é ser completa, ao contrário da versão condensada da Seção 4.
5. Dentro de cada célula, envolver nomes técnicos com colchetes/chaves (`tabela[coluna]`, `SWITCH(...)`) em backticks em vez de escapar manualmente — ver Seção 8.
6. Depois de criar as páginas filhas, atualizar (via `replace_content`) o corpo da página guarda-chuva para linkar cada uma (`<page url="...">Título</page>`, sem emoji — ver Seção 7), e atualizar o corpo da página do projeto para linkar a guarda-chuva.
7. Reler todas as páginas criadas com `notion-fetch` para confirmar que as tabelas grandes (pode haver 70+ linhas em algumas) não foram truncadas e que não sobrou lixo de parsing.

## 6. Linkar sub-páginas no corpo da página do projeto

Depois de criar cada sub-página, atualizar o corpo da página do projeto (passo 3) para incluir um link de navegação:

```
<page url="https://app.notion.com/p/<id-sem-tracos>">Documentação Técnica v1.0</page>
```

**Usar sempre `notion-update-page` com `command: "replace_content"`** (reescrever o corpo inteiro), não `insert_content`/`update_content` incremental — evita o bug abaixo.

## 7. Armadilha conhecida: emoji dentro do texto do `<page>` quebra o parser

Incluir um emoji **imediatamente após o texto do link** dentro de uma tag `<page url="...">📄 Título</page>` passada via `insert_content`/`update_content` já causou, em produção, a duplicação do bloco: o parser cria o `<page>` corretamente (mas sem o emoji) e ainda deixa um parágrafo extra com o texto malformado (`\<page url="[...\>📄](...">📄) Título\</page\>`) — sujeira visível na página.

**Mitigação:**
- Não incluir emoji no texto do link `<page>` (o emoji do ícone da sub-página já aparece sozinho quando a página é aberta/expandida — não precisa duplicar no texto do link).
- Preferir `replace_content` (reescreve o corpo inteiro de forma limpa) a `insert_content`/`update_content` ao adicionar um link de sub-página no corpo de uma página já existente.
- Depois de qualquer `insert_content`/`update_content`, sempre reler a página com `notion-fetch` para confirmar que não sobrou lixo — se sobrar, corrigir com `replace_content`.

## 8. Escaping do Notion-flavored Markdown

Fora de blocos de código, escapar `\ * ~ \` $ [ ] < > { } | ^` com barra invertida quando usados literalmente (ex. valores em reais: `R\$ 353.241,20`). Dentro de code spans (`` `texto` ``) e code fences (```` ```javascript ... ``` ````) o conteúdo é literal — **não escapar** nada ali. Por isso, ao mencionar nomes técnicos com colchetes/chaves em prosa (`fFaturamento[coluna]`, `SWITCH(...)`), sempre envolver em backticks em vez de escapar manualmente cada caractere.
