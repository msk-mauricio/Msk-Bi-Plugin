---
name: bi-documentation
description: >
  Generates professional Power BI semantic model documentation as a .docx file, following the exact SIA Inteligência visual template with purple branding, structured tables, cover page, TOC, and comprehensive sections for tables, columns, relationships, DAX measures, naming conventions, data sources, and report pages. Also covers publishing/syncing that documentation to the MSK Code Notion workspace. Use this skill whenever the user asks to document a Power BI model, generate documentation from PBIR/TMDL/PBIP files, create a semantic model doc, produce a .docx report for a Power BI project, or mentions "documentação Power BI", "documentar modelo semântico", "gerar documentação do modelo", "doc do Power BI", "documentação PBIR", "relatório do modelo semântico", or any variation of documenting a Power BI semantic model or report. Also trigger when the user provides TMDL files, PBIR project folders, or Power BI metadata and wants a formatted Word document output, or asks to publish/sync/levar a documentação para o Notion. Even if the user just says "documenta isso" while working with Power BI files, this skill applies.
---

# Documentação Power BI: Gerador de Documento .docx

This skill generates a professional .docx document that fully documents a Power BI semantic model, following a branded template. The output replicates the exact formatting, spacing, headers, footers, tables, and structure of the reference template.

> **Branding ativa neste projeto: MSK Code.** O template foi reconfigurado para usar a marca MSK Code — logo `assets/msk-code-logo.png`, paleta azul `#367DD9` (primária) / `#3299D9` (secundária), com acentos em laranja `#F2A516`/`#D97A07` (fonte: `assets/paleta_cores Fonte League Spartan.jpg`). Ver `references/template-spec.md` seção 2 e 12 para os tokens completos. Se outro cliente pedir sua própria marca no lugar da MSK Code, substitua o logo e os tokens de cor mantendo a estrutura do template. O `.docx` é entregável **complementar** à documentação markdown de `docs/documentacao/` da Fase 8 — gere-o quando o cliente pedir documento formal.

> **Padrão da Fase 8 (D-25): somente local, em .md + .html + .pdf.** Os `.md` de `docs/documentacao/` são a fonte; `scripts/exportar_docs.py <pasta> --titulo "<Cliente> · <Projeto>"` gera `html/` (páginas autocontidas com a paleta MSK Code + `index.html`) e `pdf/` (Microsoft Edge headless). Publicar no Notion **não** faz parte do padrão — só quando o usuário pedir explicitamente (`references/notion-publishing.md`). O `.docx` continua opcional.

## When to Use

- User wants to document a Power BI semantic model
- User provides PBIR/TMDL/PBIP project files and wants a Word doc
- User asks to generate documentation from Power BI metadata
- User mentions "documentação", "documentar", "doc do modelo" in a Power BI context
- User asks to export the Markdown documentation to HTML/PDF (run `scripts/exportar_docs.py`)
- User explicitly asks to publish, sync, or "levar para o Notion" the documentation (see `references/notion-publishing.md`) — never by default

## Quick Start

1. Read the `references/template-spec.md` file for the complete visual specification
2. Collect the Power BI model data (from TMDL files, user input, or MCP tools)
3. Generate the .docx using `docx-js` following the exact template spec
4. Validate: confirm the file opens (non-zero size, valid zip — e.g. `node -e "require('fs').statSync('<file>')"`) and review the section list against the structure below
5. If the user also wants the documentation published/synced to Notion, read `references/notion-publishing.md` and follow it — do not improvise the Notion structure from scratch

## Document Structure

The document has exactly this structure, in this order:

1. **Cover Page** (Section 1, separate header): logo centered, title block, version info
2. **Table of Contents** (auto-generated from headings)
3. **1. Visão Geral do Modelo**: summary table with model properties
4. **2. Arquitetura do Modelo (Star Schema)**: table listing all tables with type and description
5. **3-7. Table Sections** (one per table): description, columns table, data source info
6. **8. Relacionamentos**: relationships table + observations
7. **9. Catálogo de Medidas DAX**: full measures catalog table
8. **10. Padrões DAX Utilizados**: DAX patterns summary table
9. **11. Convenções de Nomenclatura**: naming conventions table
10. **12. Fontes de Dados**: data sources table + file path blockquote
11. **13. Páginas do Relatório**: pages table + custom visuals + bookmarks

## How to Build the Document

Before writing any code, read:
- `references/template-spec.md` for complete formatting rules (CRITICAL)

### Data Collection

The skill needs this data to generate the document. Collect it from the user, TMDL files, or the Power BI MCP tools:

- **Model metadata**: name, storage mode, culture, compatibility level, table count, measure count, relationship count, data source, project format, visual theme
- **Tables**: name, type (Fato/Dimensão/Medidas), description, columns (name, type, summarize, description), data source info
- **Relationships**: from table/column, to table/column, cardinality, cross-filter direction
- **DAX Measures**: name, expression, format string, description
- **DAX Patterns**: pattern name, which measures use it, description
- **Naming Conventions**: element type, convention, examples
- **Data Sources**: table, source file, sheet/table name, observations
- **Report Pages**: page number, name, visual count, description
- **Custom Visuals**: visual name, type description
- **Bookmarks**: count and description

### Generation

Use `docx-js` (npm package `docx`) to create the .docx file. The `references/template-spec.md` file contains every detail needed: exact hex colors, font sizes in half-points, DXA measurements for margins and column widths, table cell shading patterns, header/footer configuration, and cover page layout.

The document uses two sections:
- **Section 1** (cover page): header with centered logo (787400 × 442592 EMU), no footer
- **Section 2** (content pages): header with left-aligned small logo + right-aligned italic text with purple bottom border, centered footer with page number

### Key Implementation Notes

- Use `npm install docx` (local, in a scratch folder) before generating
- The logo for this project is `assets/msk-code-logo.png` (MSK Code); `assets/sia-logo.png` remains bundled only as a fallback reference example
- All tables follow the same pattern: brand-color header row (#367DD9, white bold text), alternating data rows (white / #FCEFDC)
- Body text is 9pt, color #212121
- Headings use the brand's primary tones (#367DD9 for H1, #3299D9 for H2)
- Notes use italic 9pt #616161
- Validate the output opens correctly before delivering
- The document language is pt-BR

### Adapting to Different Models

The template is designed for any Power BI model. Adapt by:
- Adjusting the number of table sections (3-7 in the reference) based on actual tables
- Including or omitting sections based on available data
- Keeping the same visual formatting regardless of content volume

## Output

The final output is a single `.docx` file named following the pattern:
`Documentacao_{ModelName}.docx`

Place it in `docs/documentacao/` and present the path to the user.

If Notion publishing was also requested, the output additionally includes the Notion page URLs created/updated per `references/notion-publishing.md` — present those links to the user as well.
