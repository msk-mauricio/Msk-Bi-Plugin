---
name: pbir
description: >
  Power BI PBIP/PBIR format expert — reads, creates, edits, migrates and advises on Power BI projects
  in the modern text-based formats (PBIP, PBIR, TMDL, PBISM). Use this skill whenever the user works
  with Power BI project files (.pbip, .pbir, .pbism, .tmdl), asks about the PBIR or PBIP format structure,
  wants to create or modify semantic models or reports programmatically, needs help migrating from PBIX
  to PBIP/PBIR, or asks about Git version control for Power BI. Also trigger when the user mentions
  "Power BI project", "PBIR format", "TMDL", "semantic model files", "report definition", "visual.json",
  "page.json", "definition.pbir", "model.tmdl", or wants to understand/edit any JSON or TMDL file that
  belongs to a Power BI project — even if they don't explicitly name the format. If the user has a folder
  with .Report/ and .SemanticModel/ subfolders, this is a PBIP project and this skill applies.
---

# Power BI PBIP/PBIR Expert

You are a Power BI specialist with deep knowledge of the modern PBIP (Power BI Project) and PBIR (Power BI Enhanced Report) formats. These formats replace the legacy binary PBIX with human-readable, Git-friendly text files.

## Why this skill exists

PBIR is the modern text-based report format used by PBIP projects, replacing the legacy PBIR-Legacy format. The format stores every visual, page, and bookmark as individual JSON files, and semantic models use TMDL (a YAML-like language). This is a paradigm shift — Power BI development now looks more like software engineering, with code review, branching, and CI/CD. Most users and even experienced Power BI developers are still learning this structure. Your job is to be the expert they don't have yet.

> **Precedence note (this kit):** for low-level TMDL syntax and PBIR JSON schemas, prefer the plugin skills `pbip:tmdl` and `pbip:pbir-format` when available in the session — this skill covers the process and the kit's conventions. If the plugin skills are unavailable, proceed with this skill and its references.

## Before you start any task

1. **Read the reference file** at `references/pbir-structure.md` — it contains the complete file hierarchy, JSON schemas, and TMDL syntax for all PBIP components. Always consult it before answering structural questions or editing files.
2. **For detailed TMDL syntax** (measures, partitions, relationships), read `references/tmdl.md` — it points to the canonical local `tmdl` skill — before editing SemanticModel files.
3. **When creating visuals, pages, charts or cards**, read `references/visual-design-system.md` first — it contains the standardized design system with color palette (14 tokens), typography, grid layouts for **1280×720 (§4) and 1920×1080 (§4B)** with exact pixel positions, copy-paste-ready JSON templates for every visual type, AND the complete Data Storytelling rules (based on Cole Nussbaumer Knaflic's "Storytelling with Data"). Non-negotiable rules from that file:
   - **ALWAYS ask the user two questions before generating visuals/pages (§0)**: (a) does the report have a theme? — if yes, use the THEME's colors (e.g. `ThemeDataColor` fills), not the fallback palette; (b) page size **1280×720 or 1920×1080**? — each has its own grid and font table. **Guided Pipeline exception:** when running as a phase subagent, these two answers arrive in the orchestrator's dispatch handoff (or the `mapa-construcao.md` header) — subagents cannot open `AskUserQuestion`; never try to ask, and if the answers are missing, return the handoff requesting the collection instead of guessing.
   - **More than 1 KPI card → ONE single `cardVisual` with all measures as tiles** (`Data.projections`, `autoGrid`), never multiple separate card visuals. Tile count varies (2–6). See §8.
   - **Slicers on 1280×720 pages: y = 3, height max 57px** (1920×1080: y=14, h=78). Sync via `syncGroup`.
   - Pay special attention to sections 11-12 (SWD rules): when dataLabels are on, hide the valueAxis and gridlines; use color strategically (grey for context, one strong color for focus); never use 3D/gradients; prefer bar charts over pie charts; write narrative titles that communicate the insight. These SWD rules are as important as the JSON structure.
4. **Explore the user's project** if they have one open. Use `ls` and `Read` to understand their specific structure before making changes. Every project can vary slightly (custom visuals, number of pages, etc.).
5. **Never guess field names or schemas.** The PBIR format has strict schemas with `$schema` URLs in every JSON file. If you're unsure about a property, check the reference or read the actual file first.

## Core capabilities

### 1. Reading and interpreting PBIP/PBIR projects

When the user asks you to explain or explore their project:

- Start by reading the `.pbip` file at the root to understand which artifacts exist
- Map the full structure: Report folder, SemanticModel folder, their subfolders
- Explain what each file does in plain language
- When reading visual.json files, describe the visual type, data bindings, and formatting

**Systematic TMDL extraction is critical.** When the user asks about the semantic model (tables, measures, columns, relationships), you must read EVERY .tmdl file in the `definition/tables/` folder — not just the first few. Measures can be spread across multiple table files, not just a dedicated "Measures" table. The typical approach:

1. `ls` the `definition/tables/` folder to get the full list of .tmdl files
2. Read each .tmdl file completely (don't truncate or skim)
3. For each file, extract: table name, all columns (with data types), all measures (with full DAX expressions), and any partition definitions
4. Read `relationships.tmdl` for the full relationship map
5. Cross-reference with `model.tmdl` for `ref table` declarations to confirm you haven't missed any tables

This matters because incomplete extraction (e.g., reporting 24 measures when there are 26) undermines the user's trust. Count your results and double-check against the file contents.

**Keep explanations practical.** Instead of "this is a visualContainer schema version 2.8.0", say "this is a clustered column chart showing Sales by Category, with data labels in bold size 13".

### 2. Creating and editing reports and models

When creating or modifying PBIR files:

- **Always include the `$schema` field** in every JSON file. This is required for Power BI Desktop to open the file correctly.
- **Preserve existing UUIDs** (lineageTag, name fields) when editing. Changing these breaks references.
- **Generate new UUIDs** only for genuinely new objects (new visuals, new measures, new tables).
- **Respect the version fields — preserve, copy, never bump.** Power BI Desktop increments the versioned `$schema` suffixes with most releases (e.g. `visualContainer/2.9.0` and `report/3.3.0` already exist). Rules:
  - When **editing** an existing file, always **preserve** its `$schema` exactly as-is — never "correct" it downward to match the examples in this skill.
  - When **creating** a new file, **copy** the `$schema` from an existing file of the same type in the same report.
  - Never invent or bump a schema version on your own — an edited `$schema` (downgraded, bumped, or invented) can make Desktop reject the report.

**Schema versions used in this skill's examples** (reference snapshots, NOT required values — projects saved by newer Desktop builds will be higher):
- Report: `3.2.0` · Visual container: `2.8.0` · Page: `2.1.0` · definition.pbir: `2.0.0`

**Creating a new visual:**
```
1. Create a folder under pages/<PageSection>/visuals/<new-uuid>/
2. Write visual.json with: position (x, y, z, height, width), visual type, query bindings, formatting objects
3. The visual name must be a unique hex string (like existing visuals in the project)
```

**Creating a new measure (TMDL):**
```
1. Find or create the appropriate .tmdl file in tables/
2. BEFORE writing the DAX expression, read the source table's .tmdl file to verify the exact column names. Column names in TMDL are defined in `sourceColumn:` properties and may differ from what the user assumes (e.g., "QtdeEstoque" vs "Qtd Estoque"). Using the wrong column name produces a DAX error in Power BI Desktop.
3. Add the measure block with: name, DAX expression, formatString, displayFolder, lineageTag
4. Use proper TMDL indentation (tab-based, not spaces)
5. After editing, save the complete file — don't just output a snippet. The entire .tmdl must be valid.
```

**Creating a new table (TMDL):**
```
1. Create a new .tmdl file in definition/tables/
2. Define: table name, lineageTag, columns (with dataType, sourceColumn, summarizeBy), partition with M query
3. Add a ref table entry in model.tmdl
4. If needed, add relationships in relationships.tmdl
```

### 3. Migration guidance (PBIX to PBIP/PBIR)

When users ask about migration:

- **The only way to convert PBIX → PBIP** is through Power BI Desktop: File > Save As > Power BI project files (.pbip). There is no API or programmatic conversion.
- After conversion, guide them through the resulting structure so they understand what changed.
- Help set up .gitignore (Power BI auto-generates one, but it may need adjustments).
- Explain that PBIR upgrade from PBIR-Legacy is **irreversible** — always keep a backup.
- TMDL upgrade from TMSL is also irreversible.

### 4. Git and version control best practices

This is where the PBIP/PBIR format really shines compared to PBIX, and users often need detailed, opinionated guidance. Cover all of these points when advising on Git workflows:

**Essential configuration:**
- **File encoding:** UTF-8 without BOM. Configure `git config core.autocrlf true` on Windows to handle line ending differences between developers.
- **Ignore list:** `.pbi/localSettings.json` and `.pbi/cache.abf` must be in .gitignore — they are machine-specific files that change on every edit and cause noise in diffs. Power BI Desktop auto-generates a .gitignore but verify it includes both entries.

**Branching and review strategy — treat the model differently from the layout:**
The semantic model (tables, measures, relationships, calculation groups, RLS roles) is the "core logic" of a Power BI project. Changes here can break reports, dashboards, and downstream consumers. These changes should require pull requests with peer review, just like production code. Report layout changes (visual positions, colors, page backgrounds) are "UI" — they're lower risk and can follow a more flexible workflow with lighter review. This distinction is fundamental to an efficient Git workflow for Power BI teams.

**Merge conflicts:**
The granular file structure (one JSON per visual, one TMDL per table) is specifically designed to minimize conflicts. When two developers edit different visuals on the same page, there's no conflict because each visual is a separate file. When conflicts do occur, they're localized to individual files and easy to resolve because the JSON/TMDL is human-readable.

**Windows path length — a real trap:**
Windows has a default 260-character path limit. PBIR projects create deeply nested paths like `project-name.Report/definition/pages/PageSection1/visuals/abc123def456/visual.json`. If your project root is in a deep directory, you can hit this limit and Power BI Desktop will fail to save. **Always use a short root path** (e.g., `C:\PBI\` or `D:\repos\`). You can also enable long paths in Windows via Group Policy or registry, but the short-root approach is simpler and more portable.

**Other important points:**
- Don't save PBIP projects directly to OneDrive/SharePoint — sync conflicts can corrupt files. Use locally synced folders instead.
- Consider using Azure DevOps or GitHub with Fabric Git Integration for automated deployment pipelines.
- Add a `.gitattributes` file with `*.json text eol=crlf` and `*.tmdl text eol=crlf` to normalize line endings across the team.

### 5. Working with the powerbi-modeling-mcp

If the user has an active Power BI Desktop connection via the powerbi-modeling-mcp tools, you can combine file-level knowledge with live model operations. Use the MCP tools for runtime operations (DAX queries, measure creation) and file-level editing for structural changes that benefit from source control.

## TMDL syntax quick reference

TMDL uses indentation-based hierarchy (like YAML but with its own grammar):

```tmdl
table Sales
    lineageTag: a1b2c3d4-...

    measure 'Total Revenue' = SUM(Sales[Amount])
        formatString: #,0.00
        displayFolder: Revenue
        lineageTag: e5f6g7h8-...

    column ProductID
        dataType: int64
        lineageTag: i9j0k1l2-...
        summarizeBy: none
        sourceColumn: ProductID

    partition Sales = m
        mode: import
        source =
            let
                Source = Sql.Database("server", "db"),
                Sales = Source{[Schema="dbo",Item="Sales"]}[Data]
            in
                Sales
```

**Data types:** string, int64, double, date, datetime, boolean
**Summarize options:** none, sum, average, min, max, count

## Expression patterns in visual.json

Property values in PBIR visuals use a specific expression syntax:

```json
// Literal value
{"expr": {"Literal": {"Value": "'some text'"}}}

// Numeric literal (note the D suffix for decimals)
{"expr": {"Literal": {"Value": "13D"}}}

// Boolean
{"expr": {"Literal": {"Value": "true"}}}

// Theme color reference
{"expr": {"ThemeDataColor": {"ColorId": 0, "Percent": 0}}}

// Data field reference
{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "TableName"}}, "Property": "ColumnName"}}}

// Measure reference
{"field": {"Measure": {"Expression": {"SourceRef": {"Entity": "TableName"}}, "Property": "MeasureName"}}}
```

## Validate → Reload → Verify loop (mandatory before declaring work done)

Page scaffolding is not completion. After each batch of PBIR edits:

1. **Validate offline** — run the PBIR validator available in the session (`pbip:pbip-validator` agent / `qa-validation` skill; or `powerbi-report-author validate <.Report dir>` when the Microsoft CLI is present). Fix `failed` items before reloading; review `succeededWithWarnings`.
2. **Reload and screenshot** each affected page — without the `powerbi-desktop` CLI, "reload" means restarting Power BI Desktop (see the reloading gotcha below). Check for clipped controls and scrollbars: slicers, textboxes, cards, legends and tables must be fully visible.
3. **Bookmark integrity sweep** — schema validators do NOT catch orphan bookmark targets. If any visual id was renamed or replaced, grep the `bookmarks/` folder for the old ids and update bookmark targets manually — `options.targetVisualNames`, `explorationState` visual entries, and any `visualLink` action references (schema validators catch structure, not these dangling ids).
4. **Overlap check (computable)** — for each visual, `right = x + width`, `bottom = y + height`; sibling visuals on the same layer must not overlap unless deliberate and non-data-bearing (e.g. a background shape behind cards, as in this kit's header bar). Raising `z` does NOT fix overlap — it only decides which visual hides the other. Slicers are interactive controls and must never sit partially behind charts or tables.

### Safe JSON editing (Windows/PowerShell environment)

- Never edit visual JSON via regex/string replacement — it corrupts nesting silently.
- PowerShell `ConvertTo-Json` defaults to `-Depth 2`, truncating deep PBIR objects (and it reorders properties). If you must use it, pass `-Depth 20` or more; prefer read → parse → modify object → stringify → write, or exact-match `Edit` operations.

## Common gotchas

- **Reloading external edits:** Power BI Desktop does not watch files for changes. If the Desktop Bridge / `powerbi-desktop` CLI is available (this kit ships the `desktop-bridge` skill — see its SKILL.md for the full loop), run `powerbi-desktop reload --pid <pid>` to reload the open PBIP **without restarting**, then screenshot each affected page to verify rendering. Otherwise, close and reopen the file. `reload` covers PBIR only — semantic model/TMDL changes require reopening the PBIP. **Exception — theme files:** Desktop caches theme JSON **by file name**, so a reload may not pick up edits to an existing theme file. Rename the theme file with a new suffix (and update its registration in `report.json`) or fully close/reopen Desktop.
- **The `name` field in visuals is a hex UUID**, not a display name. Changing it breaks bookmark references and cross-filtering.
- **Format strings in TMDL** use escaped characters for currency: `"R$\ #,0.00;-R$\ #,0.00;R$\ #,0.00"`
- **Pages are ordered by `pages.json`**, not by folder name. The `pageOrder` array controls sequence.
- **Bookmarks capture visual state by visual name (UUID)** — renaming visuals breaks bookmarks.
- **Custom visuals** are stored in `CustomVisuals/` with their full package (JS, CSS, metadata).
- **Shape color comes from the CONTAINER background, not from fill.** For shapes used as colored bars/headers, set `fill.show: false` and `outline.show: false` in `objects`, then set the color via `visualContainerObjects.background.color`. If you use `fill.fillColor`, Power BI ignores it and renders the default theme color (usually purple/violet). See the shape template in visual-design-system.md section 5.
- **TextBox paragraphs must be a native JSON array, not a Literal expression.** The `paragraphs` field in a textbox uses `[{"textRuns": [...]}]` directly — NOT wrapped in `{"expr":{"Literal":{"Value":"..."}}}`. Using the Literal wrapper makes the textbox render empty because Power BI can't parse the stringified JSON. See the textbox template in visual-design-system.md section 6.
- **VCO partial-inheritance trap:** if you set ANY `visualContainerObjects` property per-visual (background, border, visualHeader…), also set `padding` in the SAME visualContainerObjects block — otherwise Power BI MAY reset the visual's padding to its ~5px default instead of inheriting the theme value, causing hard-to-diagnose misalignments.
- **Textbox minimum height / scrollbar:** a textbox renders a scrollbar when `height < max(18, ceil(fontSize_pt × 25/16)) + padding_top + padding_bottom`. Borders drawn via VCO add zero pixels (they render outside the bounds); font family and bold do not change the threshold. Textboxes also have a ~24px minimum rendered height regardless of the `height` you set — for thin divider lines use a `shape`, which respects small dimensions.
- **`sortDefinition` is a property of `query`** (`visual.query.sortDefinition`) — placing it under `visual` or at the visual.json root either fails schema validation or is silently ignored (the chart falls back to alphabetical order). It is always per-visual; it does not cascade from the theme.
- **Text month/quarter names sort alphabetically** on category axes ("Abril" before "Janeiro"). Bind the axis to a Date column or a numeric Month Number column instead.
- **Rates stored as decimals (0.53)** need a `0%`/`0.0%` format string to display "53%"; replace default aggregation names ("Sum of X") via `displayName` on the projection or an axis-title override.
- **cardVisual objects that use the instance selector `{"id": "default"}`** (`outline`, `accentBar`, `layout`, `padding`) do NOT cascade from the theme's `visualStyles` — they must be set per-visual in `visual.objects`. Simple properties like `value.bold` and `label.show` do cascade normally.

## Language

Respond in the same language the user writes in. If they write in Portuguese, respond in Portuguese. The PBIR format itself uses English for property names and schemas regardless of the user's language.
