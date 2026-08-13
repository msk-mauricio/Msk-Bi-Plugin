# TMDL — referência

A fonte canônica de sintaxe, regras de segurança e boas práticas TMDL deste kit é a skill local **`tmdl`**:

```
.claude/skills/tmdl/SKILL.md
```

Leia aquele arquivo diretamente — este ponteiro existe para evitar duas cópias divergentes do mesmo conteúdo (a cópia integral que vivia aqui foi consolidada lá).

Complementos rápidos no contexto PBIR:

- Antes de escrever DAX numa medida, leia o `.tmdl` da tabela de origem para confirmar os nomes exatos das colunas (`sourceColumn:`).
- Preserve `lineageTag` de objetos existentes; gere novos UUIDs apenas para objetos genuinamente novos.
- Indentação TMDL é tab-based; edite blocos mínimos, nunca reformate o arquivo inteiro.
- Para o layout de pastas canônico do projeto, use `powerbi/<NomeDoProjeto>.SemanticModel/definition/` (ver CLAUDE.md § Power BI artifact layout).
