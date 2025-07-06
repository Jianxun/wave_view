"""
Wave View CLI interface.

Provides command-line interface for plotting SPICE waveforms using the v1.0.0 API.
"""

import click
import sys
from pathlib import Path
from typing import Optional

import plotly.io as pio

from .core.plotspec import PlotSpec
from .core.plotting import plot as create_plot
from .loader import load_spice_raw
from .utils.env import configure_plotly_renderer


@click.group()
@click.version_option()
def cli():
    """Wave View - SPICE Waveform Visualization CLI."""
    pass


@cli.command()
@click.argument('raw_file', type=click.Path(exists=True, path_type=Path))
@click.option('--spec', '-s', 'spec_file',
              type=click.Path(exists=True, path_type=Path),
              required=True,
              help='YAML specification file for plot configuration')
@click.option('--output', '-o', 'output_file',
              type=click.Path(path_type=Path),
              help='Output file path (HTML, PNG, PDF, etc.). If not specified, plot will be displayed.')
@click.option('--width', type=int,
              help='Plot width in pixels (overrides spec file)')
@click.option('--height', type=int,
              help='Plot height in pixels (overrides spec file)')
@click.option('--title', type=str,
              help='Plot title (overrides spec file)')
@click.option('--theme', type=click.Choice(['plotly', 'plotly_white', 'plotly_dark', 'ggplot2', 'seaborn', 'simple_white']),
              help='Plot theme (overrides spec file)')
@click.option('--renderer', type=click.Choice(['auto', 'browser', 'notebook', 'plotly_mimetype', 'json']), default='auto',
              show_default=True,
              help='Plotly renderer to use when displaying plot')
def plot(raw_file: Path, spec_file: Path, output_file: Optional[Path] = None,
         width: Optional[int] = None, height: Optional[int] = None,
         title: Optional[str] = None, theme: Optional[str] = None,
         renderer: str = 'auto'):
    """
    Plot SPICE waveforms using a specification file.
    
    Examples:
        wave_view plot sim.raw --spec spec.yaml
        wave_view plot sim.raw --spec spec.yaml --output plot.html
        wave_view plot sim.raw --spec spec.yaml --width 1200 --height 800
        wave_view plot sim.raw --spec spec.yaml --title "My Analysis" --theme plotly_dark
    """
    try:
        # Load the specification file
        click.echo(f"Loading plot specification from: {spec_file}")
        spec = PlotSpec.from_file(spec_file)
        
        # Apply CLI overrides via helper
        _apply_overrides(spec, width=width, height=height, title=title, theme=theme)
        
        # Load SPICE data using helper
        click.echo(f"Loading SPICE data from: {raw_file}")
        data, _ = load_spice_raw(raw_file)
        
        # Create the plot using v1.0.0 API
        click.echo("Creating plot...")
        fig = create_plot(data, spec)
        
        if output_file:
            # Save to file
            click.echo(f"Saving plot to: {output_file}")
            _save_figure(fig, output_file)
            click.echo("Plot saved successfully!")
        else:
            # Display the plot
            click.echo("Displaying plot...")
            # Configure renderer based on environment and CLI option
            configure_plotly_renderer()
            if renderer != 'auto':
                pio.renderers.default = renderer
            click.echo(f"Using Plotly renderer: {pio.renderers.default}")
            fig.show()
            
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Configuration Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected Error: {e}", err=True)
        sys.exit(1)


def _save_figure(fig, output_file: Path):
    """Save figure to various formats based on file extension using a writer map."""
    writers = {
        '.html': fig.write_html,
        '.json': fig.write_json,
        '.png': fig.write_image,
        '.pdf': fig.write_image,
        '.svg': fig.write_image,
        '.jpg': fig.write_image,
        '.jpeg': fig.write_image,
    }

    suffix = output_file.suffix.lower()
    writer = writers.get(suffix)

    if writer is None:
        click.echo(f"Warning: Unknown file extension '{suffix}', defaulting to HTML")
        writer = fig.write_html
        output_file = output_file.with_suffix('.html')

    writer(output_file)


def _apply_overrides(spec: PlotSpec, **overrides):
    """Apply non-None overrides to a PlotSpec instance."""
    for key, value in overrides.items():
        if value is not None and hasattr(spec, key):
            setattr(spec, key, value)
    return spec


@cli.command()
@click.argument('raw_file', type=click.Path(exists=True, path_type=Path))
@click.option('--limit', '-l', type=int, default=10,
              help='Limit number of signals to display (default: 10)')
def signals(raw_file: Path, limit: int):
    """
    List available signals in a SPICE raw file.
    
    Examples:
        wave_view signals sim.raw
        wave_view signals sim.raw --limit 20
    """
    try:
        click.echo(f"Loading SPICE data from: {raw_file}")
        data, _ = load_spice_raw(raw_file)
        
        signals = list(data.keys())
        click.echo(f"\nFound {len(signals)} signals:")
        
        # Display signals with numbering
        for i, signal in enumerate(signals[:limit], 1):
            click.echo(f"  {i:2d}. {signal}")
        
        if len(signals) > limit:
            click.echo(f"  ... and {len(signals) - limit} more signals")
            click.echo(f"  (Use --limit {len(signals)} to show all)")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli() 