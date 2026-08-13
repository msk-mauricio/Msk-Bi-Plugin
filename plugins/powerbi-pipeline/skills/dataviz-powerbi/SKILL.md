---
name: dataviz-powerbi
description: Skill de boas práticas de visualização de dados, UX analítico e storytelling para dashboards Power BI.
---

# Skill: DataViz Power BI

## Fonte canônica
Os tokens de cor, tipografia, grid de layout e os templates JSON completos de cada visual PBIR vivem em **um único arquivo**:

```
.claude/skills/pbir/references/visual-design-system.md
```

Leia aquele arquivo antes de criar qualquer página ou visual PBIR (a skill `pbir` referencia as seções numeradas dele). Esta skill resume os **princípios de decisão** — não duplique os templates aqui.

> **Paleta:** a paleta verde/laranja do design system é um **exemplo** (projeto Coinest). A paleta real de cada projeto vem do design system do cliente ou do mockup aprovado no Gate 5 — substitua os tokens, mantendo a estrutura.

## Princípios SWD (Storytelling with Data)

1. **DataLabels vs eixo — nunca ambos.** dataLabels ON → valueAxis OFF + gridlines OFF (barras/colunas). Tendência importa mais → valueAxis ON + gridlines sutis + dataLabels OFF (linhas).
2. **Elimine clutter:** sem títulos de eixo, sem subtítulo, sem 3D/gradientes/sombras decorativas, sem marcadores de linha (exceto ponto de destaque), sem borda que não informa.
3. **Cor estratégica:** projete em cinza primeiro; UMA cor forte apenas no elemento que conta a história. Máximo 3 cores por gráfico. Evite vermelho+verde juntos (daltonismo) — use laranja no lugar do vermelho.
4. **Título narrativo:** comunique o insight ("Receita cresceu 12%"), não só o tema ("Receita Mensal").
5. **Tipo certo de gráfico:** barras horizontais para ranking/categorias longas; linha para tempo; card para valor único; evite pie/donut/gauge.
6. **Hierarquia visual (leitura em Z):** KPI mais importante no canto superior esquerdo; cards = resumo em 3 segundos; gráficos superiores = análise principal; inferiores = detalhamento.
7. **Um atributo pré-atentivo de destaque por gráfico** — se tudo está destacado, nada está.
8. **Sort explícito sempre** — Ascending para temporal, Descending para ranking.
9. **Framework narrativo por página:** O quê (cards) → E daí (gráficos de contexto) → E agora (título/callout com a ação).

## Regras críticas PBIR (resumo — detalhes e JSON no design system)

- Query wells: `Category`/`Y` em gráficos, `Values` em slicer, `Data` em card — **nunca** `Values` em gráfico.
- Cor de shape vem de `visualContainerObjects.background.color` (fill interno `show: false`).
- `paragraphs` de textbox é array JSON nativo, nunca `Literal` encodado.
- Slicer com header visível: altura mínima 55px.
- `subTitle show: false` em todos os visuais; `drillFilterOtherVisuals: true`; preserve o `$schema` do arquivo real (nunca rebaixe a versão — `visualContainer/2.8.0` é apenas o default dos templates em report novo).

## Checklist rápido por página

- [ ] Cada visual responde uma pergunta de negócio (matriz de rastreabilidade).
- [ ] Grid e posições conforme o design system (ou o mockup aprovado).
- [ ] Regra dataLabels vs eixo aplicada em cada gráfico.
- [ ] Paleta do projeto (não a de exemplo) aplicada consistentemente.
- [ ] Títulos narrativos; sort explícito; sem clutter.
