"""Environment / renderer helpers for yaml2plot.

These utilities detect whether the code is running inside a Jupyter environment
and configure Plotly's default renderer accordingly.
"""

from __future__ import annotations

import sys

import plotly.io as pio

__all__ = [
    "is_jupyter",
    "configure_plotly_renderer",
]


def is_jupyter() -> bool:
    """Return True if running in a Jupyter/IPython kernel (including Colab)."""
    try:
        from IPython import get_ipython  # type: ignore

        ip = get_ipython()  # noqa: D401  # pylint: disable=invalid-name
        if ip is not None and hasattr(ip, "kernel"):
            return True
    except ImportError:
        # IPython not installed → definitely not in Jupyter.
        pass

    # Google Colab exposes the module automatically.
    if "google.colab" in sys.modules:
        return True

    # ipykernel is loaded only when running inside a kernel.
    return "ipykernel" in sys.modules


def configure_plotly_renderer() -> None:
    """Choose a sensible Plotly default renderer based on environment."""
    if not is_jupyter():
        # In standalone scripts default to browser for best interactivity.
        pio.renderers.default = "browser"
