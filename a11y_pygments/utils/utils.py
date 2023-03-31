import os
from pathlib import Path
from typing import List

from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pygments.token import Text
from setuptools import find_packages


def find_all_themes_packages() -> List[str]:
    """Finds the current supported themes in the a11y pygments package."""
    exclude = {"test", "a11y_pygments", "a11y_pygments.utils"}
    packages = set(find_packages())
    themes = list(packages - exclude)
    themes = [x.split(".")[1] for x in themes]
    return themes


def find_all_themes() -> List[str]:
    """Finds the current supported themes names in the a11y pygments package."""
    exclude = {"test", "a11y_pygments", "a11y_pygments.utils"}
    packages = set(find_packages())
    themes = list(packages - exclude)
    themes = [x.split(".")[1] for x in themes]
    themes = [x.replace("_", "-") for x in themes]
    return themes


def generate_css(themes: List[str], save_dir=""):
    """Generate css for the given themes."""
    basedir = "a11y_pygments"
    for theme in themes:
        style = get_style_by_name(theme)
        formatter = HtmlFormatter(style=style, full=True, hl_lines=[2, 3, 4])
        css = formatter.get_style_defs()
        color = style.style_for_token(Text)["color"]
        css += (
            f"\n.highlight {{ background: {style.background_color}; color: #{color}; }}"
        )
        package = theme.replace("-", "_")
        out = Path(basedir) / package / "style.css"
        with open(out, "w") as f:
            f.write(css)

        if save_dir:
            if not Path(save_dir).joinpath("css").exists():
                os.mkdir(Path(save_dir).joinpath("css"))
            out = Path(save_dir).joinpath("css", f"{package}-style.css")
            with open(out, "w") as f:
                f.write(css)
