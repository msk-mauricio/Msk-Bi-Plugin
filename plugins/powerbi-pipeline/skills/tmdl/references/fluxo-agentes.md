# TMDL — Fluxo de trabalho dos agentes, checklists e critérios de qualidade

> Referência da skill `tmdl`. Carregar ao planejar uma alteração completa (diagnóstico → validação)
> ou ao revisar o trabalho antes de devolver o handoff.

## 1. Agentes que usam TMDL

| Agente | Usa TMDL? | Motivo |
|---|---:|---|
| Power Query Reviewer | Sim | Pode alterar partições, expressões M e consultas dentro de TMDL. |
| Data Modeler | Sim | Cria e revisa tabelas, colunas, relacionamentos, cardinalidade e direções de filtro. |
| DAX Specialist | Sim | Cria medidas, formatos, descrições e display folders. |
| PBIR Report Builder | Sim | Precisa ler medidas, tabelas e campos disponíveis para criar visuais corretos. Só deve alterar TMDL se for autorizado. |
| BI QA Validator | Sim | Valida consistência entre requisito, modelo, DAX e relatório. |
| Documentador | Sim | Lê TMDL para documentar modelo, medidas e regras. |

## 2. Fluxo obrigatório para agentes modificadores

### 2.1 Antes da alteração

O agente deve gerar:

```md
## Diagnóstico TMDL

### Arquivos analisados

### Objetos impactados

### Dependências encontradas

### Riscos

### Plano de alteração
```

### 2.2 Durante a alteração

O agente deve:

```text
- Editar apenas arquivos necessários.
- Preservar propriedades existentes.
- Não reformatar tudo.
- Não misturar responsabilidades de outros agentes.
```

### 2.3 Depois da alteração

O agente deve gerar:

```md
## Validação pós-alteração

### Arquivos alterados

### Objetos criados/alterados

### Dependências validadas

### Riscos remanescentes

### Próximos passos
```

E garantir os registros:

```text
CHANGELOG.md (no pipeline guiado: via handoff → o orquestrador grava no encerramento do gate)
DECISIONS.md, se houver decisão técnica
TODO.md, se houver pendência
```

## 3. Checklist para revisão TMDL

Use esta lista antes de finalizar qualquer tarefa:

```text
[ ] O arquivo TMDL continua com indentação válida.
[ ] O objeto alterado existe no escopo correto.
[ ] Não houve renomeação sem busca de dependências.
[ ] Medidas DAX referenciam objetos existentes.
[ ] Relacionamentos usam colunas com tipos compatíveis.
[ ] Colunas técnicas desnecessárias foram ocultadas, não expostas.
[ ] Medidas possuem formato adequado.
[ ] Medidas relevantes possuem descrição.
[ ] Display folders foram aplicados quando necessário.
[ ] Alterações em Power Query consideraram unappliedChanges.json.
[ ] Alterações que afetam PBIR foram sinalizadas.
[ ] Mudança registrada para o CHANGELOG.md (via handoff no pipeline guiado).
[ ] DECISIONS.md foi atualizado se houve decisão arquitetural.
```

## 4. Critérios de qualidade

Uma alteração TMDL é considerada boa quando:

```text
- Resolve um requisito claro.
- É pequena e rastreável.
- Mantém o modelo semanticamente consistente.
- Preserva propriedades existentes.
- Não quebra PBIR.
- Não cria ambiguidade de relacionamento.
- Não duplica lógica DAX.
- Está documentada.
```

Uma alteração TMDL é considerada ruim quando:

```text
- Renomeia objetos sem rastrear dependências.
- Remove propriedades desconhecidas.
- Reescreve arquivos inteiros sem necessidade.
- Cria medida sem requisito.
- Cria relacionamento bidirecional sem justificativa.
- Usa muitos-para-muitos para resolver problema de modelagem mal definido.
- Altera Power Query sem validar impacto no modelo.
```

## 5. Integração com outras skills

Combinar esta skill com:

- `power-query-m` — ao alterar partições ou expressões M.
- `dimensional-modeling` — ao alterar tabelas, chaves, cardinalidade ou relacionamentos.
- `dax` — ao criar ou revisar medidas.
- `pbir` — quando a alteração impactar visuais, filtros, páginas, bookmarks ou tooltips.
- `qa-validation` — ao concluir alteração e validar consistência do fluxo completo.

## 6. Prompt interno recomendado

Sempre que um agente for modificar TMDL, seguir este prompt mental:

```text
Estou alterando o modelo semântico. Antes de editar, preciso:

1. Identificar objeto e arquivo.
2. Verificar dependências no repositório.
3. Verificar impacto em PBIR.
4. Verificar se há unappliedChanges.json.
5. Aplicar alteração mínima.
6. Preservar propriedades existentes.
7. Documentar mudança.
8. Listar riscos remanescentes.
```

## 7. Exemplo de saída esperada do agente

```md
## Diagnóstico

Identifiquei que a medida `Receita` está sem descrição, sem display folder e com nome pouco
específico para o requisito aprovado de Receita Líquida.

## Plano

- Criar nova medida `Receita Líquida`.
- Manter `Receita` temporariamente para evitar quebra de visuais.
- Adicionar descrição e formatString.
- Sinalizar ao PBIR Report Builder para substituir o uso da medida antiga nos visuais.

## Alterações realizadas

- `tables/Medidas.tmdl`: criada medida `Receita Líquida`.
- `TODO.md`: criada pendência para revisar visuais que ainda usam `Receita`.
- Handoff: mudança listada para o orquestrador registrar no CHANGELOG.md.

## Riscos

- A medida antiga ainda pode estar em uso no PBIR.
```
