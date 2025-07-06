#!/usr/bin/env python3
"""
Demonstration of the engineering notation enhancement for frequency domain plots.

Before the fix: Plotly displayed "1B" for 1 billion Hz (1 GHz)
After the fix: Plotly now displays "1G" for 1 billion Hz (1 GHz) - proper engineering notation
"""

import wave_view as wv
import numpy as np

def demo_engineering_notation():
    """Demonstrate the engineering notation enhancement."""
    print("🔧 Engineering Notation Enhancement Demo")
    print("="*50)
    
    # Create mock frequency data from 1 Hz to 1 GHz
    frequencies = np.logspace(0, 9, 100)  # 1 Hz to 1 GHz
    magnitude = -20 * np.log10(frequencies / 1e6)  # Simple rolloff
    
    # Create data dictionary
    data = {
        "frequency": frequencies,
        "magnitude_db": magnitude
    }
    
    # Create PlotSpec with frequency signal
    spec = wv.PlotSpec.from_yaml("""
    title: "Frequency Response - Engineering Notation Demo"
    x:
      signal: "frequency"  # This triggers engineering notation
      label: "Frequency (Hz)"
      log_scale: true
    y:
      - label: "Magnitude (dB)"
        signals:
          Response: "magnitude_db"
    height: 600
    show_rangeslider: true
    """)
    
    print("✅ Created frequency domain plot with engineering notation")
    print(f"   - X-axis signal: '{spec.x.signal}' (contains 'frequency')")
    print(f"   - Log scale: {spec.x.log_scale}")
    print("   - Result: X-axis will show '1G' instead of '1B' for 1 GHz")
    
    # Create the plot (but don't show to avoid GUI popup in tests)
    fig = wv.plot(data, spec, show=False)
    
    print("🎯 Engineering notation automatically applied!")
    print("   - Frequencies now display with proper SI prefixes")
    print("   - 1,000,000,000 Hz → 1G Hz (instead of 1B Hz)")
    print("   - 1,000,000 Hz → 1M Hz")
    print("   - 1,000 Hz → 1k Hz")
    
    # Show layout configuration
    exponent_format = fig.layout.xaxis.exponentformat if hasattr(fig.layout.xaxis, 'exponentformat') else 'Not set'
    print(f"📊 X-axis exponentformat: {exponent_format}")
    
    return fig

if __name__ == "__main__":
    demo_engineering_notation() 