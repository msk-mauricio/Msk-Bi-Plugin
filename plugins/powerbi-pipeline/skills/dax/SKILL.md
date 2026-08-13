---
name: dax
description: Skill para criação, revisão, documentação e otimização de medidas DAX em Power BI.
---

# Skill: DAX

## Quando usar
Use para criar ou revisar medidas, expressões DAX, KPIs, cálculos de tempo, metas, variações, ranking e medidas auxiliares. A orquestração da Fase 4 (matriz de viabilidade, Gates 4a/4b) está no agente `04-dax-specialist` — esta skill cobre o **como** escrever as medidas.

> **Preferência de plugin:** para autoria via CLI, prefira a skill `power-bi-dax` quando disponível. Regra crítica: DAX multi-linha (VAR/RETURN) não pode ser passado via `-e`; use `--file` ou stdin.

## Princípios de criação

0. **Tabela dedicada de medidas** — nunca crie medidas soltas em tabelas de fato/dimensão. Ao criar a primeira medida do modelo, crie uma tabela calculada vazia chamada `Medidas` (uma única vez) e insira todas as medidas do modelo nela, independente de qual tabela fornece as colunas usadas na fórmula. Ver § "Tabela dedicada de medidas" abaixo para a sintaxe TMDL exata.
1. **Medidas base antes de derivadas** — `[Receita Líquida]` antes de `[Ticket Médio]`; derivadas referenciam medidas, nunca repetem lógica.
2. **`DIVIDE()` em toda divisão** — nunca `/` direto; evita erro de divisão por zero.
3. **Variáveis (`VAR`) para legibilidade e performance** — armazene expressões repetidas ou caras em variáveis com nomes descritivos, sempre com prefixo `__` (D-18): `__PascalCase` para escalares (`VAR __ValorAnterior`), `__camelCase` para tabelas/listas (`VAR __windowTresMeses`).
4. **Nome orientado ao negócio** — sem prefixos técnicos (`med_`, `calc_`); ver `AGENTS.md` § Convenções.
5. **Sempre com `formatString`** — moeda `"R$\ #,0.00"`, percentual `"0.0%"`, inteiro `"#,0"`.
6. **Sempre em display folder** — organização sugerida na skill `tmdl` § 9.4.
7. **Descrição (`///`) em toda medida relevante** — a fórmula de negócio em uma frase.
8. **Rastreabilidade** — nenhuma medida sem requisito aprovado, pergunta de negócio e linha na matriz de rastreabilidade.

## Sintaxe TMDL de medida (formato do kit)

```tmdl
/// Receita líquida total considerando devoluções e descontos comerciais.
measure 'Receita Líquida' =
    SUM ( fVendas[ValorLiquido] )
    formatString: "R$\ #,0.00"
    displayFolder: "01. Vendas"
```

Medida derivada com variáveis:

```tmdl
/// Ticket médio por pedido: receita líquida dividida pela quantidade de pedidos.
measure 'Ticket Médio' =
    DIVIDE ( [Receita Líquida], [Quantidade de Pedidos] )
    formatString: "R$\ #,0.00"
    displayFolder: "04. Ticket Médio"
```

Antes de escrever a expressão, **leia o `.tmdl` da tabela de origem** para confirmar os nomes exatos das colunas (`sourceColumn:` pode divergir do que se assume) — nome errado = erro DAX no Desktop.

## Tabela dedicada de medidas (`Medidas`)

Todo modelo deve ter uma única tabela calculada, vazia, chamada `Medidas`, que serve só de "casa" organizacional para todas as medidas do projeto — nenhuma medida deve ficar solta em tabelas de fato/dimensão. Isso separa cálculos de dados no painel de campos e facilita a navegação em modelos com muitas medidas.

Criar **uma vez só**, na primeira medida do projeto (não recriar por fase/tabela):

```tmdl
table Medidas
	lineageTag: <gerar-guid>

	measure 'Receita Líquida' =
			SUM ( fVendas[ValorLiquido] )
		formatString: "R$\ #,0.00"
		displayFolder: "01. Vendas"

	/* demais medidas do modelo entram aqui, organizadas por displayFolder */

	column Medidas
		isHidden
		lineageTag: <gerar-guid>
		summarizeBy: sum
		isNameInferred
		sourceColumn: [Medidas]

		annotation SummarizationSetBy = Automatic

	partition Medidas = calculated
		source =
				SELECTCOLUMNS ( { 1 }, "Medidas", ''[Value] )
```

Pontos de atenção (sintaxe de tabela calculada — ver skill `tmdl`/`pbip:tmdl` para o padrão geral):
- A coluna dummy (`column Medidas`) usa `sourceColumn: [Medidas]` **com colchetes** (sintaxe de referência DAX, obrigatória em colunas de tabela calculada — `sourceColumn` sem colchetes falha ao carregar no Power BI Desktop) e fica `isHidden` — ela nunca aparece para o usuário final, existe só para a tabela ter uma coluna válida.
- `SELECTCOLUMNS ( { 1 }, "Medidas", ''[Value] )` produz uma tabela de 1 linha/1 coluna descartável — o conteúdo não importa, só a existência da tabela para hospedar medidas.
- Todas as medidas do modelo (de qualquer fato/dimensão referenciada na fórmula) entram em `table Medidas`, nunca na tabela de origem dos dados.

## Padrões comuns da Fase 4

- **Inteligência de tempo:** exige `dCalendario` marcada como tabela de datas (D-19 — `dataCategory: Time` + `isKey`, ver skill `tmdl` § 5.2); padrões `TOTALYTD`, `DATEADD(-1, YEAR)` para ano anterior, `DATESINPERIOD` para médias móveis.
- **Variação %:** `DIVIDE ( [Atual] - [Anterior], [Anterior] )` com formatString `"+0.0%;-0.0%"`.
- **Atingimento de meta:** `DIVIDE ( [Realizado], [Meta] )` — meta normalmente em `fMetas` com granularidade documentada.
- **Ranking:** `RANKX ( ALL ( dTabela[Coluna] ), [Medida] )` — atenção ao contexto de filtro.

## Checklist de revisão de medida

- [ ] Deriva de requisito aprovado (KPI 🟢/🟡 na matriz de viabilidade)?
- [ ] Reaproveita medidas base (sem lógica duplicada)?
- [ ] Usa `DIVIDE` e variáveis onde cabe?
- [ ] `formatString` e `displayFolder` definidos?
- [ ] Descrição `///` presente (se medida relevante)?
- [ ] Colunas referenciadas existem no TMDL (conferido, não assumido)?
- [ ] Linha da matriz de rastreabilidade atualizada?

## Otimização de DAX (uso secundário)

Ao revisar medidas existentes com problema de performance:

1. **Análise:** identifique transições de contexto em iteradores, expressões repetidas sem `VAR`, filtros complexos que poderiam ser expressões de tabela, funções subótimas (`COUNT` → `COUNTROWS`, `VALUES` → `SELECTEDVALUE` para valor único).
2. **Estratégia:** mova cálculos repetidos para variáveis; minimize `CALCULATE` aninhado; prefira filtrar colunas a filtrar tabelas inteiras.
3. **Entrega:** apresente a fórmula original, a otimizada, e a justificativa de cada mudança com impacto esperado; preserve o comportamento de `BLANK()`.
4. **Validação:** recomende teste comparativo (mesmos filtros, mesmos totais) no Power BI Desktop antes de substituir.
