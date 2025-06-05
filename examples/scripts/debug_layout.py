#!/usr/bin/env python3
"""
Debug script to analyze Plotly layout configuration for x-axis positioning issues.
"""

import wave_view as wv
import json
from pathlib import Path

def dump_layout_info(fig, title="Layout Analysis"):
    """Dump comprehensive layout information."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    
    # Basic figure info
    print(f"Number of traces: {len(fig.data)}")
    print(f"Figure height: {fig.layout.height}")
    
    # X-axis configuration
    print(f"\nX-AXIS CONFIGURATION:")
    print(f"  Title: {fig.layout.xaxis.title.text if fig.layout.xaxis.title else 'None'}")
    print(f"  Domain: {fig.layout.xaxis.domain}")
    print(f"  Anchor: {getattr(fig.layout.xaxis, 'anchor', 'default')}")
    print(f"  Position: {getattr(fig.layout.xaxis, 'position', 'default')}")
    print(f"  Side: {getattr(fig.layout.xaxis, 'side', 'default')}")
    print(f"  Range slider visible: {fig.layout.xaxis.rangeslider.visible if hasattr(fig.layout.xaxis, 'rangeslider') else 'No rangeslider'}")
    
    # Y-axes configuration
    y_axes = [attr for attr in dir(fig.layout) if attr.startswith('yaxis')]
    print(f"\nY-AXES CONFIGURATION ({len(y_axes)} found):")
    
    for y_axis_name in y_axes:
        y_axis = getattr(fig.layout, y_axis_name)
        print(f"  {y_axis_name.upper()}:")
        print(f"    Title: {y_axis.title.text if y_axis.title else 'None'}")
        print(f"    Domain: {y_axis.domain}")
        print(f"    Anchor: {getattr(y_axis, 'anchor', 'default')}")
        print(f"    Position: {getattr(y_axis, 'position', 'default')}")
        print(f"    Side: {getattr(y_axis, 'side', 'default')}")
    
    # Traces and their axis assignments
    print(f"\nTRACE ASSIGNMENTS:")
    for i, trace in enumerate(fig.data):
        y_ref = getattr(trace, 'yaxis', 'y')
        x_ref = getattr(trace, 'xaxis', 'x')
        print(f"  Trace {i} ({trace.name}): x={x_ref}, y={y_ref}")
    
    # Raw layout dump (for detailed inspection)
    print(f"\nRAW LAYOUT (JSON):")
    layout_dict = fig.layout.to_plotly_json()
    print(json.dumps(layout_dict, indent=2, default=str))

def test_single_y_axis():
    """Test case: Single Y-axis configuration."""
    print("\n" + "="*80)
    print("TEST 1: SINGLE Y-AXIS")
    print("="*80)
    
    config = {
        "title": "Single Y-Axis Test", 
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [
            {
                "label": "Voltage (V)",
                "signals": {"VDD": "v(vdd)"}
            }
        ],
        "show_rangeslider": True
    }
    
    fig = wv.plot("../data/Ring_Oscillator_7stage.raw", config, show=False)
    dump_layout_info(fig, "Single Y-Axis Test")
    return fig

def test_dual_y_axis():
    """Test case: Dual Y-axis configuration."""
    print("\n" + "="*80)
    print("TEST 2: DUAL Y-AXIS")
    print("="*80)
    
    config = {
        "title": "Dual Y-Axis Test",
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [
            {
                "label": "Voltage (V)", 
                "signals": {"VDD": "v(vdd)", "Output": "v(bus06)"}
            },
            {
                "label": "Current (A)",
                "signals": {"Supply Current": "i(c1)"}
            }
        ],
        "show_rangeslider": True
    }
    
    fig = wv.plot("../data/Ring_Oscillator_7stage.raw", config, show=False) 
    dump_layout_info(fig, "Dual Y-Axis Test")
    return fig

def test_triple_y_axis():
    """Test case: Triple Y-axis configuration."""
    print("\n" + "="*80)
    print("TEST 3: TRIPLE Y-AXIS")
    print("="*80)
    
    config = {
        "title": "Triple Y-Axis Test",
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [
            {
                "label": "VDD (V)",
                "signals": {"VDD": "v(vdd)"}
            },
            {
                "label": "Output (V)", 
                "signals": {"Output": "v(bus06)", "Bus07": "v(bus07)"}
            },
            {
                "label": "Current (A)",
                "signals": {"Supply Current": "i(c1)"}
            }
        ],
        "show_rangeslider": True
    }
    
    fig = wv.plot("../data/Ring_Oscillator_7stage.raw", config, show=False)
    dump_layout_info(fig, "Triple Y-Axis Test")
    return fig

def run_all_tests():
    """Run all test cases and analyze results."""
    print("WAVE_VIEW LAYOUT DEBUGGING SUITE")
    print("=" * 80)
    
    # Check if data file exists
    data_file = Path("../data/Ring_Oscillator_7stage.raw")
    if not data_file.exists():
        print(f"ERROR: Data file not found: {data_file}")
        return
    
    print(f"Data file: {data_file}")
    
    try:
        # Run test cases
        fig1 = test_single_y_axis()
        fig2 = test_dual_y_axis() 
        fig3 = test_triple_y_axis()
        
        print("\n" + "="*80)
        print("SUMMARY & ANALYSIS")
        print("="*80)
        
        print("\nKEY QUESTIONS TO INVESTIGATE:")
        print("1. Are all y-axes properly anchored to 'x'?")
        print("2. Is the x-axis appearing at the bottom of the figure?")
        print("3. Are y-axis domains calculated correctly?")
        print("4. Does the range slider work in all configurations?")
        
        print("\nNEXT STEPS:")
        print("- Examine y-axis domains for overlap/gaps")
        print("- Verify x-axis anchor behavior") 
        print("- Test with/without range slider")
        print("- Compare single vs multi y-axis layouts")
        
    except Exception as e:
        print(f"ERROR during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests() 