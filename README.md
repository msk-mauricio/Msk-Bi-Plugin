# msk-bi — marketplace de plugins Claude Code

Marketplace interno com os plugins de Business Intelligence da MSK Code.

## Instalar

```
/plugin marketplace add C:\Projetos\msk-bi-plugins
```

```
/plugin install powerbi-pipeline@msk-bi
```

Em outra máquina, depois de publicar este repositório no GitHub, troque o caminho local pelo repo:

```
/plugin marketplace add mskcode/msk-bi-plugins
```

## Atualizar

Edite os arquivos em `plugins/powerbi-pipeline/`, faça commit e rode:

```
/plugin marketplace update msk-bi
```

## Plugins

| Plugin | Conteúdo |
|---|---|
| `powerbi-pipeline` | 8 fases com gates, 10 agentes, 12 comandos, 18 skills |

## Estrutura

```
.claude-plugin/marketplace.json     ← catálogo
plugins/powerbi-pipeline/
  .claude-plugin/plugin.json        ← manifesto do plugin
  agents/                           ← 10 agentes de fase
  commands/                         ← 12 comandos (/iniciar-projeto-bi, /fase-N-*)
  skills/                           ← 18 skills de domínio
```
