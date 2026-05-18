---
name: paperplot-figure-formatting
description: Use this skill whenever creating, editing, reviewing, or regenerating Matplotlib figures for papers, slides, reports, experiments, or result artifacts. It ensures figures use the standalone paperplot package for LaTeX-ready text, readable sizing, stable layout, PDF-first export, and overlap checks.
---

# Paperplot Figure Formatting

Use this skill whenever a task creates or modifies Matplotlib plotting code or regenerates Matplotlib figure artifacts.

## Workflow

1. Use `paperplot` as the default formatting layer:
   - `style_context(...)` for local Matplotlib rcParams.
   - `subplots(...)` for figure size and subplot spacing.
   - `apply_axes_style(...)` for axes, ticks, grid, and legend frame styling.
   - `savefig(...)` for exports.
2. Save canonical figures as PDF by default. Add PNG only when slides, web previews, or existing downstream tooling explicitly need raster copies.
3. Choose presets by target:
   - `manuscript_single` or `manuscript_double` for papers and reports.
   - `slides_single`, `slides_double`, or `slides_grid` for Beamer or slide figures.
   - `compact_panel` for small diagnostics.
4. Keep LaTeX rendering enabled for canonical results. Use `usetex=False` only for tests, CI environments without LaTeX, or temporary diagnostics.
5. Prefer layout overrides over ad hoc `plt.rcParams`, tiny font-size constants, or script-local style dictionaries.
6. Place shared legends outside axes when legends would obscure data. Remove redundant labels in dense grids if they cause overlap.
7. Render-check updated figures or the deck/manuscript pages that include them before finishing.
8. When the host repository has a research log, changelog, or result manifest convention, update it if regenerated figures or presentation/manuscript artifacts change the visible project state.

## Package Reference

The standalone package repository is:

- GitHub: `git@github.com:Chiahwa/paperplot.git`
- Local checkout: `C:\Users\Hwa\Repositories\Python\paperplot`

For API details, read the package `README.md` in the standalone checkout.
