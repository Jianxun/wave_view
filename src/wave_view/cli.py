"""
Wave View CLI interface.

Provides command-line interface for plotting SPICE waveforms using the v1.0.0 API.
"""

import click
from pathlib import Path
from typing import Optional
import sys

from .core.plotspec import PlotSpec
from .core.wavedataset import WaveDataset
from .core.plotting import plot as create_plot


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
@click.option('--no-browser', is_flag=True,
              help='Don\'t open browser when displaying plot')
def plot(raw_file: Path, spec_file: Path, output_file: Optional[Path] = None, 
         width: Optional[int] = None, height: Optional[int] = None, 
         title: Optional[str] = None, theme: Optional[str] = None,
         no_browser: bool = False):
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
        click.echo(f"📊 Loading plot specification from: {spec_file}")
        spec = PlotSpec.from_file(spec_file)
        
        # Apply CLI overrides
        if width:
            spec.width = width
        if height:
            spec.height = height
        if title:
            spec.title = title
        if theme:
            spec.theme = theme
        
        # Load the SPICE data using v1.0.0 API
        click.echo(f"📈 Loading SPICE data from: {raw_file}")
        wave_data = WaveDataset.from_raw(str(raw_file))
        
        # Convert to Dict[str, np.ndarray] format for v1.0.0 plotting
        data = {signal: wave_data.get_signal(signal) for signal in wave_data.signals}
        
        # Create the plot using v1.0.0 API
        click.echo("🎯 Creating plot...")
        fig = create_plot(data, spec)
        
        if output_file:
            # Save to file
            click.echo(f"💾 Saving plot to: {output_file}")
            _save_figure(fig, output_file)
            click.echo("✅ Plot saved successfully!")
        else:
            # Display the plot
            click.echo("🚀 Displaying plot...")
            import plotly.io as pio
            if no_browser:
                # Configure to not open browser
                pio.renderers.default = "json"
                click.echo("📋 Plot data generated (use --output to save)")
            else:
                # Configure for browser rendering
                pio.renderers.default = "browser"
                fig.show()
            
    except FileNotFoundError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"❌ Configuration Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected Error: {e}", err=True)
        sys.exit(1)


def _save_figure(fig, output_file: Path):
    """Save figure to various formats based on file extension."""
    suffix = output_file.suffix.lower()
    
    if suffix == '.html':
        fig.write_html(output_file)
    elif suffix == '.png':
        fig.write_image(output_file)
    elif suffix == '.pdf':
        fig.write_image(output_file)
    elif suffix == '.svg':
        fig.write_image(output_file)
    elif suffix == '.jpg' or suffix == '.jpeg':
        fig.write_image(output_file)
    elif suffix == '.json':
        fig.write_json(output_file)
    else:
        # Default to HTML
        click.echo(f"⚠️  Warning: Unknown file extension '{suffix}', saving as HTML")
        fig.write_html(output_file.with_suffix('.html'))


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
        click.echo(f"📊 Loading SPICE data from: {raw_file}")
        wave_data = WaveDataset.from_raw(str(raw_file))
        
        signals = wave_data.signals
        click.echo(f"\n🔍 Found {len(signals)} signals:")
        
        # Display signals with numbering
        for i, signal in enumerate(signals[:limit], 1):
            click.echo(f"  {i:2d}. {signal}")
        
        if len(signals) > limit:
            click.echo(f"  ... and {len(signals) - limit} more signals")
            click.echo(f"  (Use --limit {len(signals)} to show all)")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli() 