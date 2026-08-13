---
description: Mostra o status do projeto BI (somente leitura, sem abrir gates).
---

# Status do Projeto BI

Comando **somente leitura** — não edite nenhum arquivo, não abra `AskUserQuestion`, não invoque subagentes.

1. Leia `TODO.md`: identifique o último gate `[x]` aprovado (com data e artefatos, se preenchidos) e o primeiro gate `[ ]` pendente; leia também a seção `## Ponto de retomada`.
2. Leia as 2 últimas entradas do `CHANGELOG.md`.
3. Leia a tabela "Decisões do projeto atual" de `DECISIONS.md`.
4. Apresente um resumo de uma tela: fase atual, último gate aprovado (data/usuário), próximo passo concreto, riscos e pendências em aberto.
5. Encerre sugerindo `/retomar-projeto-bi` para continuar, `/iniciar-projeto-bi` para um projeto novo, ou o comando de fase avulsa correspondente (`/fase-1-requisitos` … `/fase-8-documentacao`, D-21) se o usuário quiser rodar só uma etapa.
