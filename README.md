# paperplot

`paperplot` is a small reusable Matplotlib formatting package for LaTeX-ready
research figures. It centralizes figure size, font sizes, subplot spacing, grid
styling, DPI, and export formats so scripts can produce readable figures for
papers, slides, and reports without project-local style boilerplate.

The package uses centimeter-based geometry because manuscript and slide figure
sizes are usually chosen from document layout rather than screen pixels. Text is
rendered with LaTeX by default, and figures are saved as vector PDF by default.

## Installation

Install from a local checkout:

```powershell
python -m pip install C:\Users\Hwa\Repositories\Python\paperplot
```

Install for editable development:

```powershell
git clone git@github.com:Chiahwa/paperplot.git
cd paperplot
python -m pip install -e ".[dev]"
```

Install directly from the private GitHub repository when your environment has
access to `Chiahwa/paperplot`:

```powershell
python -m pip install "paperplot @ git+ssh://git@github.com/Chiahwa/paperplot.git@v0.1.0"
```

For `pyproject.toml` dependencies:

```toml
dependencies = [
    "paperplot @ git+ssh://git@github.com/Chiahwa/paperplot.git@v0.1.0",
]
```

## Quick Start

```python
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from paperplot import apply_axes_style, savefig, style_context, subplots


with style_context("slides_single") as spec:
    fig, ax = subplots(spec=spec)
    ax.plot(x, density, label=r"$n(x)$")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel("density")
    ax.legend(loc="best")
    apply_axes_style(ax)
    savefig(fig, "results/figures/example_density")
    plt.close(fig)
```

This writes `results/figures/example_density.pdf`. To also write a PNG copy for
tools that require raster images:

```python
savefig(fig, "results/figures/example_density", formats=("pdf", "png"))
```

## Presets

Choose the preset for the final target, then override only the dimensions the
figure genuinely needs.

| Preset | Intended use |
| --- | --- |
| `manuscript_single` | One-column paper figure. |
| `manuscript_double` | Two-column paper figure or wide manuscript panel. |
| `slides_single` | One large slide figure. |
| `slides_double` | Wide slide figure, such as 1-by-3 panels. |
| `slides_grid` | Slide-readable multi-panel grids, such as 2-by-2 overlays. |
| `compact_panel` | Small diagnostics and inset-like panels. |

Example with explicit multi-panel layout overrides:

```python
with style_context(
    "slides_grid",
    nrows=2,
    ncols=2,
    margin_top_cm=2.0,
    margin_bottom_cm=2.2,
    space_height_cm=1.6,
) as spec:
    fig, axes = subplots(2, 2, spec=spec, sharex=True)
    for ax in axes.flat:
        apply_axes_style(ax)
    fig.suptitle(r"Riemann density overlays", y=0.965)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncols=3)
    savefig(fig, "results/figures/riemann_density_overlays")
```

## API

### `PlotSpec`

Immutable dataclass containing figure width and optional height, margins,
subplot spacing, row/column count, subplot aspect ratio, font size, DPI, LaTeX
settings, and default export formats. Dimensions are stored in centimeters.
Useful computed properties include `figsize_inches` and `subplot_adjust`.

### `get_preset(name, nrows=1, ncols=1, **overrides)`

Returns a `PlotSpec` for a named preset. Override values are passed directly to
the dataclass, so use names such as `plot_width_cm`, `margin_left_cm`,
`space_height_cm`, `subplot_ratio`, `font_size`, or `plot_height_cm`.

### `style_context(preset="manuscript_single", nrows=1, ncols=1, usetex=True, **overrides)`

Applies the preset through `matplotlib.pyplot.rc_context` and yields the active
`PlotSpec`. The style is local to the `with` block.

### `subplots(...)`

Creates `fig, axes` with the `PlotSpec` figure size, DPI, and
`fig.subplots_adjust(...)` values already applied.

### `apply_axes_style(ax, grid=True, legend_fontsize=None)`

Applies consistent tick direction, top/right ticks, light grid lines, and legend
frame styling.

### `savefig(fig, path, formats=None, dpi=None)`

Saves a figure to one or more formats. When `formats=None`, the default is PDF:

```python
savefig(fig, "results/figures/name")              # name.pdf
savefig(fig, "results/figures/name.pdf")          # name.pdf
savefig(fig, "results/figures/name", formats="png")
savefig(fig, "results/figures/name", formats=("pdf", "png"))
```

The function returns a list of written `Path` objects.

## LaTeX Requirements

`paperplot` uses `text.usetex=True` by default. The `latex` executable must be
available on `PATH`; otherwise `style_context(...)` raises a clear runtime
error. For tests, CI, or minimal environments without LaTeX, explicitly use:

```python
with style_context("manuscript_single", usetex=False) as spec:
    ...
```

Do not silently disable LaTeX for canonical research figures unless the output
is only a temporary diagnostic.

## Layout Guidance

- Prefer PDF for canonical figures.
- Generate PNG only for slides, web previews, or tooling that cannot consume
  PDF.
- Put shared legends outside axes with `fig.legend(...)` when in-panel legends
  cover important curves.
- In dense grids, remove redundant labels when they crowd neighboring panels.
- After changing layout, render or inspect the PDF and check for title,
  axis-label, legend, colorbar, and caption overlap.

## Development

Install development dependencies and run tests:

```powershell
python -m pip install -e ".[dev]"
python -m pytest
python -m build
```

The tests avoid a hard LaTeX dependency by using `usetex=False` where needed.
