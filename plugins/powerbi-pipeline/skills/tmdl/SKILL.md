---
name: tmdl
version: 2026-07-20
summary: Skill para agentes que leem, analisam ou modificam arquivos TMDL em projetos Power BI PBIP/PBIR.
description: Use esta skill sempre que um agente precisar alterar objetos do modelo semântico Power BI em TMDL, incluindo tabelas, colunas, medidas, relacionamentos, partições, expressões M, roles, calculation groups, perspectivas, descrições, display folders e propriedades avançadas do Tabular Object Model.
allowed_agents:
  - orquestrador-bi
  - power-query-reviewer
  - data-modeler
  - dax-specialist
  - pbir-report-builder
  - bi-qa-validator
  - documentador-bi
last_reviewed: 2026-07-20
sources:
  - Microsoft Learn: Tabular Model Definition Language
  - Microsoft Learn: TMDL View in Power BI Desktop
  - Microsoft Learn: Power BI Desktop project semantic model folder
  - Microsoft Power BI Blog: TMDL View on the Web Preview
---

# Skill: TMDL para Power BI PBIP/PBIR

> **Leitura progressiva:** este arquivo traz só o essencial (segurança, estrutura, sintaxe de alta
> frequência). O conteúdo aprofundado fica em `references/` — carregue **somente** o arquivo
> relevante à tarefa em mãos:
>
> | Arquivo | Quando ler |
> |---|---|
> | `references/boas-praticas-modelo.md` | Nomenclatura (tabelas/colunas/medidas), boas práticas de medidas DAX, relacionamentos, descrições `///`, display folders |
> | `references/edicao-avancada.md` | `unappliedChanges.json`, renomear/excluir com rastreio de dependências, partições M, propriedades a preservar, impacto em PBIR, scripts TMDL |
> | `references/fluxo-agentes.md` | Fluxo diagnóstico→validação, checklist de revisão, critérios de qualidade, integração com outras skills |

## 1. Objetivo e quando usar

TMDL (Tabular Model Definition Language) é a representação textual do modelo tabular — otimizada
para leitura humana, versionamento e edição como código, com hierarquia por indentação (estilo YAML).

Use esta skill sempre que for ler ou modificar qualquer item dentro de:

```text
*.SemanticModel/definition/     (model.tmdl, relationships.tmdl, expressions.tmdl,
powerbi/*.SemanticModel/definition/    tables/*.tmdl, roles/, perspectives/, cultures/)
TMDLScripts/
```

## 2. Regra central de segurança

Nenhum agente modifica TMDL sem executar este ciclo:

```text
1. Diagnosticar
2. Mapear dependências
3. Propor plano de alteração
4. Alterar o menor escopo possível
5. Validar impacto
6. Atualizar documentação
7. Registrar a mudança (no pipeline guiado: via handoff → o orquestrador grava o CHANGELOG.md)
```

Antes de qualquer alteração, responder:

```text
- Qual objeto será alterado?
- Por que será alterado?
- Quais objetos dependem dele?
- Existe impacto em medidas, relacionamentos, visuais PBIR ou Power Query?
- A alteração exige aprovação humana?
```

## 3. Estrutura típica em PBIP

```text
Projeto.SemanticModel/
├── definition.pbism            # obrigatório
├── .pbi/                       # localSettings.json e cache.abf não versionar;
│                               # unappliedChanges.json = alterações PQ pendentes (ver referência)
├── definition/
│   ├── model.tmdl
│   ├── expressions.tmdl
│   ├── relationships.tmdl
│   ├── tables/                 # fVendas.tmdl, dCliente.tmdl, dCalendario.tmdl, Medidas.tmdl
│   ├── roles/  perspectives/  cultures/
└── TMDLScripts/
```

## 4. Regras mínimas de edição (valem sempre)

- **`unappliedChanges.json` existe?** Avisar o usuário e não alterar M sem confirmação
  (detalhes em `references/edicao-avancada.md` § 1).
- **Preservar indentação** (não misturar tabs e espaços no mesmo bloco); alterar apenas os blocos
  necessários; nunca reformatar o arquivo inteiro.
- **Nunca renomear ou excluir** sem buscar dependências no repositório inteiro (TMDL + PBIR + DAX +
  roles) — checklists em `references/edicao-avancada.md` §§ 2–3. Em dúvida, `isHidden: true` em vez
  de excluir.
- **Preservar propriedades existentes** (`lineageTag`, `sourceColumn`, `summarizeBy`,
  `formatString`, `sortByColumn`, `annotations`, …). Propriedade desconhecida = preservar.
- **Menor escopo possível** — relatar "alterei apenas: <arquivo>: <bloco>".
- Nomenclatura: padrão Dashmaker D-18 (`fVendas`, `dCliente`, colunas PascalCase, medidas com
  espaço) — tabela completa em `references/boas-praticas-modelo.md` § 1 e `AGENTS.md` § Convenções.

## 5. Sintaxe de alta frequência

### 5.1 Medida (sempre na tabela dedicada `Medidas` — D-17)

```tmdl
/// Receita líquida total considerando devoluções e descontos comerciais.
measure 'Receita Líquida' =
    SUM ( fVendas[ValorLiquido] )
    formatString: "R$ #,0.00"
    displayFolder: "01. Vendas"
```

- Medidas base antes de derivadas; `DIVIDE()` para divisões; descrição `///` nas medidas relevantes.
- Sintaxe da tabela `Medidas` (tabela calculada vazia): skill `dax` § "Tabela dedicada de medidas".

### 5.2 Tabela de datas — marcação obrigatória (D-19)

Toda tabela calendário (`dCalendario`) deve ser **marcada como tabela de datas** imediatamente
após a criação. Se o modelo já vier com uma tabela calendário (scaffold/herdada), **verificar** se
está marcada e marcar caso não esteja — nunca deixar um calendário sem marcação.

Sintaxe TMDL (duas propriedades, sempre em conjunto):

```tmdl
table dCalendario
	dataCategory: Time

	column Data
		isKey
		dataType: dateTime
		...
```

- `dataCategory: Time` na declaração da `table` (linha própria, indentada por tab, tipicamente após `lineageTag`).
- `isKey` na coluna de data (primeira propriedade da coluna, como no exemplo oficial `Date.tmdl` da skill `pbip:tmdl`).
- Pré-requisito de runtime: a coluna de data deve ser única e contígua (sem lacunas) — o Desktop valida no refresh; se o intervalo do calendário tiver buracos, a marcação falha.
- A marcação é o que habilita as funções de inteligência de tempo (`TOTALYTD`, `DATEADD`, `DATESINPERIOD`, etc.) sem depender do auto date/time do Desktop.
- Gotchas de sintaxe já aprendidos em projeto real (não repetir): comentários `//` soltos são inválidos em TMDL estrutural (só `///` antes de objeto); colunas de **tabela calculada** usam `sourceColumn: [Nome]` com colchetes (+ `isNameInferred` quando o nome TMDL é idêntico ao do DAX).

### 5.2b Roles (RLS/OLS) — sem `///` antes do objeto

```tmdl
role Representante
	modelPermission: read

	tablePermission dRepresentante = FALSE ()

	tablePermission dProduto
		columnPermission CustoUnitario
			metadataPermission: none
```

- **Nunca colocar um comentário `///` imediatamente antes de `role`, `tablePermission` ou `columnPermission`.** Um `///` logo antes de um objeto TMDL vira a propriedade `description` desse objeto — mas, ao contrário de tabela/coluna/medida, os objetos `Role`/`TablePermission` **não suportam** `description` no motor Analysis Services Tabular atual. O Power BI Desktop rejeita a carga do modelo inteiro com `Property 'description' is unknown and is not expected in the situation it appears` (stack trace aponta `ModelRole.TryReadNextMetadataProperty`) — achado real em projeto (Vale Verde, 2026-07-29).
- Documentar o racional de RLS/OLS (regra de negócio, pendência de dado, filtro real esperado) em markdown (`DECISIONS.md`, dicionário de dados) — nunca como comentário `///` dentro do arquivo de role.

### 5.3 Partição com expressão M

```tmdl
partition 'Tabela-Partition' = m
    mode: import
    source =
        let
            Source = ...
        in
            ...
```

- Não alterar M sem usar também a skill `power-query-m`; regras completas em
  `references/edicao-avancada.md` § 4.

## 6. Regra final

TMDL é **código-fonte crítico do modelo semântico**:

```text
Não edite como texto solto.
Edite como contrato de dados, regra de negócio e camada semântica do Power BI.
```
