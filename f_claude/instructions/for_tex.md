# Instructions for Generating LaTeX (.tex) Files

## Document Structure

### Standalone Document
- Use `\documentclass[11pt, a4paper]{article}` for standalone PDFs.
- Include all required packages in the preamble.
- Each section follows the pattern: **figure → table → paragraph analysis**.

### Section Order
Each metric section should contain (in order):
1. Main line chart (figure)
2. Raw data table
3. Brief analytical paragraph with enumerated sentences

---

## Caption Conventions

### Placement (follows top AI paper standard)
- **Tables**: caption **above** the table (after `\centering`, before `\begin{tabular}`)
- **Figures**: caption **below** the figure (after the tikzpicture/content)

### Format
- **First sentence**: bold, concise main caption — the title of the figure/table.
- **Subsequent sentences**: each on its own line (`\\`), in `\footnotesize`, providing details.
- Use `\\[2pt]` between the main caption and the detail lines.

```latex
% Figure caption (below figure)
\caption{\textbf{Main caption title.}\\[2pt]
{\footnotesize First detail sentence.\\
Second detail sentence.}}

% Table caption (above table)
\caption{\textbf{Main caption title.}\\[2pt]
{\footnotesize First detail sentence.\\
Second detail sentence.}}
```

---

## Table Style

### Layout
- Use `booktabs` rules: `\toprule`, `\midrule`, `\bottomrule`.
- Use `r` columns with manually formatted numbers (avoids siunitx/bold conflicts).
- Use `\small` font inside tables.

### Number Formatting
- **Thousands separator**: comma (e.g., `42,198` not `42198`).
- **Time values**: 2 decimal places (e.g., `2.25`).
- **Node counts**: integers with commas.
- **Percentages**: appropriate precision (e.g., `0.26\%`, `6.8\%`).

### Highlighting
- **Bold** the better value per row.
- Add **Ratio** columns where the gap is large and meaningful (e.g., elapsed time, h-calculations).
- Add **$\Delta$** and **$\Delta\%$** columns where the gap is small (e.g., explored nodes, borderline).
- When both values are identical (e.g., surely expanded), skip the table entirely — use a single sentence.

---

## Figure Style

### pgfplots Charts
- Define a shared style (e.g., `omspp chart`) for consistent appearance.
- Define per-series styles (e.g., `inc line`, `agg line`) with distinct colors, markers, and line styles.
- Use `\tikzset` for annotation styles (not `\pgfplotsset`) when annotations use `\node` or `\draw`.

### Annotations
- Use **dashed vertical lines** at key x-values with ratio/percentage labels.
- Style labels with `fill=white, draw=gray!60, rounded corners, font=\scriptsize\bfseries`.

### Trend Lines
- Add trend lines as visual guides only — **do not put statistical values (r, r²) in chart legends**.
- Use `forget plot` to exclude trend lines from the legend.
- Keep r/r² values for the text or correlation tables where they can be properly explained.

### Delta/Gap Charts
- When showing $\Delta\%$ over a variable, add dashed vertical lines at representative points (e.g., low-k, mid-k, high-k) with the percentage values.

### Normalization Charts
- When showing a ratio is roughly constant, add a **horizontal dashed reference line** at the expected value (e.g., mean generated-node count).

### Redundancy Rule
- Do not create a separate chart if the same information is already clearly visible in another chart + table.
  - Example: a ratio chart is redundant if the main chart already has dashed ratio annotations and the table has a Ratio column.

---

## Colors

- Define domain-specific colors in the preamble and use them consistently.
- Use distinct colors + markers + line styles (solid/dashed) for each series — ensures readability in grayscale print.

```latex
\definecolor{inccolor}{RGB}{34, 139, 34}   % green for Incremental
\definecolor{aggcolor}{RGB}{200, 40, 40}    % red for Aggregative
```

---

## Text Style

### Paragraph Headers
- Use `\paragraph{...}` for brief analytical summaries after figures/tables.
- Express findings in mathematical terms where possible (e.g., $\Theta(k \cdot N)$ instead of "~50x more").

### Enumerated Sentences
- Use a custom `sentences` list environment for observations.
- Each sentence should be self-contained and concise.
- Do not include raw statistical values (like Pearson r) in enumerated sentences — keep them in dedicated analysis sections.

---

## Compilation and Upload Workflow

1. Compile with `tectonic` (lightweight, auto-downloads packages).
2. When updating a `.tex` file on Drive, **always compile and upload the `.pdf` alongside it**.
3. Use `/tmp` for local compilation — do not save permanently to the local filesystem.
