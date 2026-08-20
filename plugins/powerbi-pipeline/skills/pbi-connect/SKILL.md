---
name: pbi-connect
description: "Conecta ao arquivo Power BI Desktop aberto no computador via powerbi-modeling-mcp. Use SEMPRE que o usuário pedir \"conecta ao power bi\", \"conecta ao arquivo aberto\", \"conecta no pbix\", \"abre o modelo\", \"faz a conexão\", \"conecta no projeto\", ou qualquer variação de conexão com Power BI Desktop. Também usar quando o usuário pedir qualquer operação DAX, edição de medida, análise de modelo ou manutenção de projeto Power BI sem conexão ativa. Executar imediatamente sem fazer perguntas."
---

# pbi-connect — Conexão ao Power BI Desktop

Conecta ao arquivo Power BI Desktop aberto no computador via `powerbi-modeling-mcp` e confirma o modelo disponível. Executa direto, sem perguntas.

## Pré-requisito

- `powerbi-modeling-mcp` disponível (tool_search se necessário)
- Power BI Desktop aberto com pelo menos um arquivo

---

## Fluxo padrão (executar sempre nessa ordem)

### Passo 1 — Garantir acesso às ferramentas

Se `powerbi-modeling-mcp:connection_operations` não estiver carregada, rodar:

```
tool_search("powerbi connection")
```

### Passo 2 — Listar instâncias abertas

```json
{
  "operation": "ListLocalInstances"
}
```

**Cenários:**

| Resultado | Ação |
|---|---|
| 1 instância | Conectar direto (passo 3) |
| 2+ instâncias | Listar todas com nome do arquivo e porta → perguntar ao usuário qual |
| 0 instâncias | Informar que nenhum Power BI Desktop está aberto e encerrar |

### Passo 3 — Conectar

Usar a porta retornada no ListLocalInstances:

```json
{
  "operation": "Connect",
  "connectionString": "Data Source=localhost:{PORTA};Application Name=MCP-PBIModeling"
}
```

### Passo 4 — Confirmar modelo

```json
{
  "operation": "List"
}
```

(`database_operations`)

### Passo 5 — Responder ao usuário

Confirmar conexão com resumo curto:

```
✅ Conectado — {NOME_DO_ARQUIVO} (porta {PORTA}, ~{TAMANHO} MB)
```

Se o usuário já tinha uma tarefa em mente (ex: "conecta e lista as medidas"), executar já na sequência sem esperar nova mensagem.

---

## Reconexão (porta mudou)

Quando o Power BI Desktop é fechado e reaberto, a porta muda. Se uma operação falhar com erro de conexão:

1. Rodar `ListLocalInstances` novamente
2. Conectar na nova porta
3. Confirmar e retomar a operação que falhou

Não perguntar ao usuário — reconectar silenciosamente e informar só o resultado.

---

## Múltiplos arquivos abertos

Se houver 2+ instâncias, listar assim:

```
Encontrei {N} arquivos Power BI abertos:
1. {NOME} — porta {PORTA}
2. {NOME} — porta {PORTA}

Qual você quer usar?
```

Aguardar resposta e conectar na instância escolhida.

---

## Tom

- Direto: sem introduções longas
- Confirmar conexão em 1 linha
- Se já havia tarefa, ir pra ela imediatamente após conectar
