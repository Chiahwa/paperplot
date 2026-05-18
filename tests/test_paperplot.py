from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from paperplot import get_preset, savefig, style_context, subplots


def test_preset_computes_positive_panel_geometry():
    spec = get_preset("slides_grid", nrows=2, ncols=2, usetex=False)

    assert spec.plot_width_cm == 22.0
    assert spec.subplot_width_cm > 0.0
    assert spec.subplot_height_cm > 0.0
    assert spec.height_cm > spec.subplot_height_cm
    assert spec.figsize_inches[0] == spec.plot_width_cm / 2.54


def test_style_context_sets_rcparams_without_latex():
    with style_context("manuscript_single", usetex=False, font_size=13) as spec:
        assert spec.font_size == 13
        assert plt.rcParams["text.usetex"] is False
        assert plt.rcParams["font.size"] == 13


def test_subplots_uses_spec_layout():
    with style_context("slides_grid", nrows=2, ncols=2, usetex=False) as spec:
        fig, axes = subplots(2, 2, spec=spec, sharex=True)
        try:
            assert len(axes.ravel()) == 4
            width, height = fig.get_size_inches()
            assert width == spec.figsize_inches[0]
            assert height == spec.figsize_inches[1]
        finally:
            plt.close(fig)


def test_savefig_defaults_to_pdf_and_supports_png(tmp_path: Path):
    with style_context("compact_panel", usetex=False) as spec:
        fig, ax = subplots(spec=spec)
        try:
            ax.plot([0, 1], [0, 1])
            default_paths = savefig(fig, tmp_path / "line")
            explicit_paths = savefig(fig, tmp_path / "line_copy", formats=("pdf", "png"))
        finally:
            plt.close(fig)

    assert default_paths == [tmp_path / "line.pdf"]
    assert (tmp_path / "line.pdf").exists()
    assert explicit_paths == [tmp_path / "line_copy.pdf", tmp_path / "line_copy.png"]
    assert (tmp_path / "line_copy.png").exists()
