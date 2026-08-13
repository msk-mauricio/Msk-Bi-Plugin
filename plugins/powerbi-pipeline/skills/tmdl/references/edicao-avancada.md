# TMDL — Edição avançada e segura

> Referência da skill `tmdl`. Carregar quando a tarefa envolver renomear/excluir objetos,
> alterar partições M, gerar scripts TMDL ou avaliar impacto em PBIR.

## 1. Atenção especial ao `unappliedChanges.json`

Antes de alterar Power Query, partições ou expressões M via TMDL, verificar se existe:

```text
.pbi/unappliedChanges.json
```

Risco:

- O Power BI Desktop pode sobrescrever consultas do modelo se houver alterações pendentes no Power Query.
- Se o agente editar TMDL fora do Desktop enquanto existir `unappliedChanges.json`, as alterações podem ser perdidas ao aplicar mudanças pendentes.

Regra:

```text
Se existir unappliedChanges.json:
1. Avisar o usuário.
2. Não modificar expressões M sem confirmação.
3. Sugerir abrir o PBIP no Power BI Desktop e aplicar ou descartar alterações pendentes.
```

## 2. Não renomear objetos sem rastrear dependências

Renomear tabela, coluna ou medida pode quebrar:

- Medidas DAX.
- Relacionamentos.
- Visuais PBIR.
- Tooltips.
- Bookmarks.
- Filtros de página.
- RLS.
- Perspectivas.
- Traduções.

Checklist obrigatório antes de renomear:

```text
1. Buscar o nome antigo no repositório inteiro.
2. Verificar arquivos TMDL.
3. Verificar arquivos PBIR.
4. Verificar medidas DAX.
5. Verificar relacionamentos.
6. Verificar roles/RLS.
7. Documentar substituições.
```

## 3. Não excluir objetos sem análise de uso

Antes de excluir tabela, coluna, medida ou relacionamento:

```text
- Procurar referências no repositório.
- Verificar uso em DAX.
- Verificar uso no PBIR.
- Verificar uso em relações.
- Verificar uso em roles.
- Verificar se o objeto é técnico, oculto ou usado como chave.
```

Se houver dúvida, marcar como `isHidden: true` em vez de excluir, quando fizer sentido.

## 4. Power Query dentro de TMDL (partições M)

Quando TMDL contiver partições com expressão M:

```tmdl
partition 'Tabela-Partition' = m
    mode: import
    source =
        let
            Source = ...
        in
            ...
```

Regras:

- Não alterar M sem usar também a skill `power-query-m`.
- Verificar query folding quando fonte permitir.
- Não remover coluna usada em relacionamento, DAX ou PBIR.
- Padronizar etapas M sem quebrar dependências.
- Evitar transformar tipos no final se isso comprometer performance.
- Registrar qualquer mudança em fonte, filtro, merge, append ou tipo de dado.

## 5. Propriedades importantes a preservar

Ao editar TMDL, preservar quando existirem:

```text
lineageTag
summarizeBy
formatString
isHidden
isAvailableInMdx
sourceColumn
dataType
sortByColumn
displayFolder
description
annotations
changedProperties
```

Não remover propriedades desconhecidas. Se o agente não souber o impacto, deve preservar.

## 6. Compatibilidade com PBIR

Alterações em TMDL podem impactar diretamente o relatório PBIR.

Antes de alterar nomes, remover campos ou mudar medidas, buscar referências em:

```text
*.Report/definition/
*.Report/report.json
*.Report/pages/
*.Report/visuals/
powerbi/*.Report/definition/
```

Riscos comuns:

```text
- Visual quebrado por medida renomeada.
- Filtro quebrado por coluna removida.
- Tooltip quebrado por campo ocultado ou excluído.
- Bookmark inconsistente.
- Página usando medida antiga.
```

Regra:

```text
Se uma alteração TMDL afetar PBIR, chamar o agente pbir-report-builder ou bi-qa-validator.
```

## 7. Scripts TMDL

TMDL scripts possuem comando no topo, seguido de um ou mais objetos.

Comandos comuns:

```text
createOrReplace
alter
create
replace
delete
```

Regra de segurança:

- Preferir `createOrReplace` apenas quando o objeto inteiro for conhecido.
- Evitar `delete` sem validação explícita.
- Para alterações pequenas, preferir modificar o arquivo específico no projeto PBIP em vez de gerar script amplo.

Exemplo conceitual:

```tmdl
createOrReplace
    table dCalendario
        column Data
            dataType: dateTime
```
