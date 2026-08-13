---
name: desktop-bridge
description: "Verificação viva no Power BI Desktop sem fechar/reabrir o programa: reload de PBIR, screenshots das páginas renderizadas e validação runtime do modelo (refresh/EVALUATE). Use nas Fases 6 e 7 e nos gates 2b/3b/4b quando o Desktop estiver aberto com o PBIP do projeto."
---

# Skill: Desktop Bridge — verificação viva no Power BI Desktop

Baseada no plugin `powerbi-authoring` (microsoft/skills-for-fabric). Permite **editar arquivos PBIR e ver o resultado renderizado no Desktop aberto**, sem fechar/reabrir o programa, e **validar o modelo em runtime** (refresh, queries DAX) — substituindo a antiga pendência manual "refresh test no Power BI Desktop".

> **Sempre opcional:** se os CLIs ou o bridge não estiverem disponíveis, siga o fluxo file-only atual (validação offline + pendência runtime manual no TODO.md). Indisponibilidade do bridge nunca bloqueia gate (D-14).

## Fonte da verdade (D-14/D-15 — regra dura)

- Os **arquivos versionados** (PBIR JSON e TMDL) continuam sendo a única fonte da verdade. O modelo vivo no Desktop nunca é.
- O MCP `powerbi-modeling-mcp` é usado **somente para leitura/runtime**: refresh, query DAX (`EVALUATE`), inventário de objetos. **Nunca** usar as operações de escrita do MCP — toda escrita no modelo é feita nos arquivos TMDL (lanes dos agentes 02/03/04), e toda escrita de relatório nos arquivos PBIR (lane do agente 06).

## Pré-requisitos (setup completo em `docs/setup-desktop-bridge.md`)

1. Node.js 20+ (`node --version`).
2. `npm install -g @microsoft/powerbi-report-authoring-cli@latest @microsoft/powerbi-desktop-bridge-cli@latest` → comandos `powerbi-report-author` e `powerbi-desktop`.
3. Power BI Desktop com a preview feature **"Enable external tool access to Power BI Desktop through secure local APIs"** habilitada (File > Options > Preview features) e Desktop **reiniciado**.
4. O projeto aberto no Desktop como **PBIP** (não `.pbix` — reload retorna `REPORT_DIR_REQUIRED`).
5. MCP `powerbi-modeling-mcp` registrado no `.mcp.json` da raiz do kit (carregado sob demanda via `npx`).

## Loop da Fase 6 — Edit → Validate → Reload → Screenshot

```text
1. Editar arquivos PBIR (powerbi/<Nome>.Report/definition/)
2. powerbi-report-author validate "powerbi/<Nome>.Report"   → erros? corrigir e voltar a 1
3. powerbi-desktop status                                   → escolher o PID correto
4. powerbi-desktop reload --pid <pid>                       → erro? corrigir PBIR e voltar a 1
5. powerbi-desktop screenshot-all --pid <pid> --output-dir docs/qa/screenshots-gate6
6. Revisar os PNGs; problema? voltar a 1. Limpo? → handoff com screenshots anexados
```

## Regras operacionais (herdadas do plugin — não negociar)

- **PID sempre via `status`**: o mesmo PBIP pode estar aberto em mais de um processo; omitir `--pid` com múltiplas instâncias → `AMBIGUOUS_DESKTOP_INSTANCE`. Preferir instância com `bridgeStatus: connected` e `currentFilePath` do projeto.
- **`hasUnsavedChanges: true` no `status`** → NÃO fazer reload: peça ao usuário salvar/descartar as mudanças da UI do Desktop, rode `status` de novo e só siga com `false` (evita sobrescrever edições de qualquer um dos lados).
- **`reload` e `screenshot` sempre em série por PID** (em paralelo → `Cancelled`). `status`/`manifest` podem rodar concorrentes.
- **`screenshot <page-id>` usa o ID PBIR da página** (ex.: `ReportSection1a2b3c`, de `definition/pages/pages.json`), nunca o display name.
- **`reload` cobre apenas PBIR.** Mudanças de modelo/TMDL não aparecem no reload — reabrir o PBIP no Desktop (pedir ao usuário) antes de validar em runtime.
- **Tema JSON é cacheado por nome de arquivo**: edição de tema pode não aparecer no reload. Renomear o arquivo de tema com sufixo novo + atualizar a referência em `report.json`, ou fechar/reabrir o Desktop. O QA deve conferir o tema explicitamente nos screenshots.
- **Validar offline antes de todo reload** (`powerbi-report-author validate` e, no Gate 6, também `pbip:pbip-validator` — D-06). Recarregar PBIR inválido pode deixar o relatório visivelmente quebrado no Desktop até o fix.

## Validação runtime do modelo (gates 2b/3b/4b)

Quando o Desktop estiver aberto com o PBIP do projeto:

1. Após edições TMDL, pedir ao usuário para **reabrir o PBIP** no Desktop (reload não cobre modelo).
2. Executar **refresh** via MCP `powerbi-modeling-mcp` (operação Refresh) ou via `pbi-desktop:connect-pbid` (TOM) — nunca os dois na mesma instância — e anexar o resultado ao gate. Refresh falhou = gate não abre até corrigir (tipicamente `sourceColumn` errado ou M inválido).
3. No Gate 4b, validar cada medida nova com uma query real: `EVALUATE {[Nome da Medida]}` — resultado anexado ao gate.
4. Erro de credencial no refresh → parar e instruir o usuário a configurar as credenciais no Desktop; não tentar contornar.

Sem Desktop/bridge disponível: registrar a pendência runtime manual no TODO.md, como no fluxo original.

## Erros comuns → ação

| Saída | Significado | Ação |
|---|---|---|
| `not_connected` / `NO_BRIDGE` / `connect ENOENT \\.\pipe\pbi-desktop-bridge-<pid>` | Bridge indisponível | Abrir com `powerbi-desktop open "<caminho>.pbip"`; se persistir, habilitar a preview feature e reiniciar o Desktop |
| `AMBIGUOUS_DESKTOP_INSTANCE` | Mais de uma instância | `status` → escolher PID → repetir com `--pid` |
| `METHOD_NOT_AVAILABLE` | Build do Desktop antigo | Atualizar o Power BI Desktop |
| `REPORT_DIR_REQUIRED` | PID com `.pbix` (não PBIP) | Abrir o PBIP correto ou escolher outro PID |
| `ReportDefinitionValidationFailed` | Desktop rejeitou o PBIR | Corrigir PBIR → `validate` → reload de novo (mesmo PID) |
| `Timeout` | Operação estourou o budget | Confirmar `connected` no `status`, repetir 1x; persistindo, `--wait-seconds 120`; se travar, perguntar ao usuário se há diálogo modal aberto no Desktop |
| `Cancelled` | reload/screenshot concorrentes no mesmo PID | Serializar as operações e repetir uma por vez |
| `HostNotReady` | Host ainda assentando pós-reload | O CLI já re-tenta; repetir 1x se aparecer — sem sleeps manuais |

## Revisão de screenshots (Fase 6 e QA)

Checar em cada PNG: banners de erro ou visuais em branco ("Requires X fields"); valores/labels truncados ou sobrepostos; cores/tema divergentes do mockup aprovado; contraste insuficiente entre séries; slicers sem valores; nulos/brancos inesperados; aderência ao layout do mockup da Fase 5.
