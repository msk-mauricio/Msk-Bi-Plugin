# TMDL — Boas práticas de modelo (nomenclatura, medidas, relacionamentos, descrições)

> Referência da skill `tmdl`. Carregar quando a tarefa envolver nomear objetos, criar/revisar
> medidas, alterar relacionamentos ou documentar o modelo com descrições.

## 1. Nomenclatura

### 1.1 Tabelas

Padrão adotado (Dashmaker, D-18 — camelCase, ver `AGENTS.md` § Convenções):

```text
dCliente
dProduto
dCalendario
dVendedor
fVendas
fEstoque
fMetas
stgVendasTratado
Medidas
```

Regras:

- `d` para dimensões, `f` para fatos, `fx` para funções, `src`/`stg` para staging — tudo camelCase, sem acentos/espaços.
- `Medidas` é o nome fixo da tabela dedicada de medidas (D-17 — exceção deliberada ao camelCase).
- Evitar nomes genéricos como `Tabela1`, `Consulta1`, `Base`, `Planilha1`.
- Convenção anterior (`fato_Vendas`/`dim_Cliente`) substituída em 2026-07-20 — permanece só em projetos já entregues nela.

### 1.2 Colunas

Padrão do kit (ver `AGENTS.md` § Convenções — PascalCase, sem acentos e sem underscores):

```text
IdCliente
IdProduto
DataEmissao
ValorBruto
ValorLiquido
Quantidade
StatusPedido
```

Regras:

- Seguir a convenção oficial do repositório (`AGENTS.md`): PascalCase, sem acentos, sem underscores.
- Nomes amigáveis para o usuário final ficam no relatório/visuais, não no nome físico da coluna.
- Ocultar colunas técnicas.
- Não expor chaves substitutas sem necessidade.
- Evitar prefixos técnicos em campos que aparecem no painel de dados do usuário final.

### 1.3 Medidas

Padrão recomendado:

```text
Receita Bruta
Receita Líquida
Quantidade Vendida
Ticket Médio
Margem Bruta
Margem Bruta %
Atingimento Meta %
Variação Receita %
```

Regras:

- Medidas devem ser orientadas ao negócio.
- Evitar prefixos como `med_`, `calc_`, `m_` no nome exibido ao usuário.
- Usar display folders para organização.
- Toda medida importante deve ter descrição.

### 1.4 Display folders sugeridos

```text
01. Vendas
02. Quantidade
03. Margem
04. Ticket Médio
05. Metas
06. Tempo
07. Rankings
08. Clientes
09. Produtos
99. Técnicas
```

## 2. Boas práticas para medidas DAX em TMDL

Ao criar medidas:

- Usar medidas base antes de medidas derivadas.
- Usar `DIVIDE()` para divisões.
- Usar variáveis para legibilidade.
- Evitar duplicação de lógica.
- Adicionar `formatString` coerente.
- Adicionar descrição funcional com `///` quando aplicável.
- Colocar a medida em display folder.

Medida derivada (exemplo):

```tmdl
/// Ticket médio por pedido, calculado pela divisão entre receita líquida e quantidade de pedidos.
measure 'Ticket Médio' =
    DIVIDE (
        [Receita Líquida],
        [Quantidade de Pedidos]
    )
    formatString: "R$ #,0.00"
    displayFolder: "04. Ticket Médio"
```

Regra:

```text
Nunca criar medida se ela não estiver ligada a:
- Um requisito aprovado;
- Uma pergunta de negócio;
- Um visual planejado;
- Uma necessidade técnica documentada.
```

## 3. Boas práticas para relacionamentos

O agente de modelagem deve priorizar:

```text
- Modelo estrela.
- Fatos no centro.
- Dimensões nas bordas.
- Relacionamentos 1:* entre dimensão e fato.
- Filtro single-direction sempre que possível.
- Muitos-para-muitos apenas com justificativa.
- Bidirecional apenas quando necessário e documentado.
```

Checklist antes de alterar relacionamento:

```text
1. Identificar tabela fato.
2. Identificar tabela dimensão.
3. Confirmar granularidade das tabelas.
4. Confirmar unicidade da chave na dimensão.
5. Validar tipo de dados das chaves.
6. Validar direção de filtro.
7. Avaliar impacto em medidas existentes.
8. Documentar decisão.
```

Toda alteração em relacionamento deve atualizar:

```text
docs/dicionario-dados/relacionamentos.md
DECISIONS.md
CHANGELOG.md (no pipeline guiado: via handoff → orquestrador grava no encerramento do gate)
```

## 4. Descrições com `///`

Use descrições para objetos importantes:

```tmdl
/// Tabela fato com pedidos faturados, devoluções e valores comerciais.
table fVendas
```

```tmdl
/// Receita bruta antes de descontos e devoluções.
measure 'Receita Bruta' =
    SUM ( fVendas[ValorBruto] )
```

Regras:

- Toda medida final voltada ao usuário deve ter descrição.
- Tabelas fato e dimensão devem ter descrição.
- Colunas técnicas podem ter descrição quando houver regra relevante.
