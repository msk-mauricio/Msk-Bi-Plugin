# Cores de SVG × tema do relatório × dark mode

## Fatos que definem o desenho da solução

1. **DAX não lê o theme JSON em runtime.** Não existe função que acesse `dataColors` ou qualquer
   token do tema. A única ponte runtime é o conditional formatting *Field value* de visuais nativos,
   cujo **host** resolve, além de cores CSS, os tokens `"good"`, `"bad"`, `"neutral"`, `"minColor"`,
   `"midColor"`, `"maxColor"` (minúsculos, case-sensitive). Nada disso funciona **dentro** da string
   SVG — lá só valem cores CSS literais (no kit: hex com `#`).
2. **Dark mode (Desktop, Service, mobile) nunca recolore o conteúdo do relatório** — só o chrome do
   aplicativo ("Power BI content, however, isn't affected", doc oficial mobile). Não há
   prefers-color-scheme para a imagem. Dark mode de relatório é decisão de design-time.
3. O modo de alto contraste recolore visuais nativos, mas **não** reescreve imagens data URI — SVGs
   mantêm as cores de origem (registrar em QA de acessibilidade).
4. `DaxLib.SVG.Color.Theme`/`PerformanceTheme` **não leem o tema do relatório** — são DATATABLEs de
   paletas embutidas na função ("Power BI", "Stoplight" etc.).

## Padrão do kit: medidas de token (build-time, mesmo commit)

Como o elo tema↔SVG é por build, não por runtime, a paleta vive em **um lugar só** e viaja no mesmo
commit:

- **Medidas de cor** na tabela `Medidas` (D-17), `displayFolder: 91. Cores` — uma por token:

  ```tmdl
  	measure 'Cor Positiva' = "#1C8757"
  		formatString: "General"
  		displayFolder: 91. Cores
  	measure 'Cor Alerta' = "#F57C00"
  		formatString: "General"
  		displayFolder: 91. Cores
  ```

- **Regra de consumo**: medidas SVG **nunca** contêm hex literal — só `VAR __Cor = [Cor Positiva]`
  no bloco CONFIG. Lint trivial de QA: nenhum `#RRGGBB` em medida com sufixo ` SVG` fora da pasta
  `91. Cores`.
- Os mesmos hex alimentam o theme JSON (`StaticResources/RegisteredResources/`): `dataColors`,
  `good`/`bad`/`neutral` — fonte canônica de tokens do kit:
  `.claude/skills/pbir/references/visual-design-system.md`. Alteração de cor = editar tokens →
  atualizar tema + medidas → **mesmo commit** + CHANGELOG.
- Em projetos com muitos tokens/derivações, alternativa: UDF própria
  (`<Projeto>.Color.Token("positiva")` com DATATABLE) — objeto TMDL versionável (requer UDF GA,
  compat level 1702+). Derivações (hover/clareado): no tema usa-se `ThemeDataColor.Percent`; em DAX,
  a lib `EvaluationContext.Colour` (`HEX.AdjustLuminance`, `HEX.TextColour`) reproduz o mesmo efeito.
- Para CF de visuais nativos com semântica bom/ruim, preferir medida que retorna os **nomes**
  `"good"`/`"bad"`/`"neutral"` — troca de tema propaga sem tocar no modelo. (Não vale dentro de SVG.)

## Fundo transparente é regra

Não desenhar `<rect>` de fundo no SVG: o alpha é preservado e o fundo da célula/cartão/página continua
sendo do tema — trocar o tema não "descasca" o SVG. Um fundo hardcoded é o que mais destoa em
migração de tema.

Se o projeto tiver variante escura: segundo conjunto de tokens (tema escuro dedicado) **ou** toggle
in-report com tabela desconectada `dModo` + `SELECTEDVALUE` + `SWITCH` nas medidas de cor — nesse
caso os SVGs acompanham automaticamente (a medida recalcula), enquanto propriedades estáticas do tema
não mudam. Texto `#666`/`#333` hardcoded fica ilegível no escuro — mais um motivo para tokens.

## Limitação residual (honesta)

Trocar apenas o theme JSON depois de publicado **não** atualiza as cores dentro dos SVGs (elas moram
no modelo/reportExtensions). O acoplamento é por build — tokens, tema e medidas no mesmo commit é o
que mantém a paridade.
