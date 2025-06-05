#!/usr/bin/env python3
"""
Test to verify Y-axis ordering: first in config should appear at top of plot.
"""

import wave_view as wv

def test_y_axis_order():
    """Test that Y-axis order in config matches visual order in plot."""
    print("🧪 Testing Y-axis order behavior...")
    
    config = {
        "title": "Y-Axis Order Test",
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [
            {"label": "FIRST in config", "signals": {"VDD": "v(vdd)"}},
            {"label": "SECOND in config", "signals": {"Current": "i(c1)"}},
            {"label": "THIRD in config", "signals": {"Output": "v(bus06)"}}
        ]
    }
    
    fig = wv.plot("../data/Ring_Oscillator_7stage.raw", config, show=False)
    
    print("\nConfig order → Plot position:")
    print(f"1. '{config['Y'][0]['label']}' → ", end="")
    
    # Find which axis has the first config's label
    axes = ['yaxis', 'yaxis2', 'yaxis3']
    for axis_name in axes:
        if hasattr(fig.layout, axis_name):
            axis = getattr(fig.layout, axis_name)
            if axis.title.text == "FIRST in config":
                domain = axis.domain
                position = "TOP" if domain[1] > 0.7 else "MIDDLE" if domain[1] > 0.4 else "BOTTOM"
                print(f"{axis_name} domain {domain} ({position})")
                break
    
    print(f"2. '{config['Y'][1]['label']}' → ", end="")
    for axis_name in axes:
        if hasattr(fig.layout, axis_name):
            axis = getattr(fig.layout, axis_name)
            if axis.title.text == "SECOND in config":
                domain = axis.domain
                position = "TOP" if domain[1] > 0.7 else "MIDDLE" if domain[1] > 0.4 else "BOTTOM"
                print(f"{axis_name} domain {domain} ({position})")
                break
    
    print(f"3. '{config['Y'][2]['label']}' → ", end="")
    for axis_name in axes:
        if hasattr(fig.layout, axis_name):
            axis = getattr(fig.layout, axis_name)
            if axis.title.text == "THIRD in config":
                domain = axis.domain
                position = "TOP" if domain[1] > 0.7 else "MIDDLE" if domain[1] > 0.4 else "BOTTOM"
                print(f"{axis_name} domain {domain} ({position})")
                break
    
    # Verify expected behavior: first in config should be at top
    first_axis = None
    for axis_name in axes:
        if hasattr(fig.layout, axis_name):
            axis = getattr(fig.layout, axis_name)
            if axis.title.text == "FIRST in config":
                first_axis = axis
                break
    
    if first_axis and first_axis.domain[1] > 0.7:
        print("\n✅ CORRECT: First in config appears at TOP of plot")
        return True
    else:
        print("\n❌ INCORRECT: First in config does not appear at top")
        return False

if __name__ == "__main__":
    test_y_axis_order() 