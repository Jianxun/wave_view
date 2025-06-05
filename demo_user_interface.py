#!/usr/bin/env python3
"""
Demo: Wave View Package - End User Interface
============================================

This script demonstrates how an end user would typically interact with 
the Wave View package for SPICE waveform visualization.
"""

import sys
import os

# Add the package to path (in real usage, this would be: pip install wave_view)
sys.path.insert(0, './wave_view')

import wave_view as wv

def main():
    print("🌊 Wave View Package Demo")
    print("=" * 40)
    
    # Use the test data we have available
    spice_file = "prototype/script/Ring_Oscillator_7stage.raw"
    
    if not os.path.exists(spice_file):
        print(f"❌ Test data not found: {spice_file}")
        print("Please run this from the wave_view project root directory.")
        return
    
    # 1. EXPLORE AVAILABLE SIGNALS
    print("\n1️⃣  Exploring Available Signals")
    print("-" * 30)
    
    data = wv.load_spice(spice_file)
    print(f"📁 Loaded: {data}")
    print(f"🔍 Total signals: {len(data.signals)}")
    print(f"📊 Sample signals: {data.signals[:8]}")
    
    # Show signal categorization
    voltages = [s for s in data.signals if s.startswith('v(')]
    currents = [s for s in data.signals if s.startswith('i(')]
    print(f"⚡ Voltage signals: {len(voltages)} (e.g., {voltages[:3]})")
    print(f"🔌 Current signals: {len(currents)} (e.g., {currents[:3]})")
    
    # 2. QUICK PLOT WITH AUTO-CONFIGURATION  
    print("\n2️⃣  Quick Plot (Auto-Configuration)")
    print("-" * 35)
    
    print("Creating automatic plot from SPICE data...")
    fig1 = wv.plot(spice_file, show=False)  # Don't open browser in demo
    print(f"✅ Auto-plot created with {len(fig1.data)} traces")
    print("   (In normal usage, this would open in your browser)")
    
    # 3. CUSTOM CONFIGURATION
    print("\n3️⃣  Custom Configuration")
    print("-" * 25)
    
    # Create a custom config for specific signals
    custom_config = {
        "title": "Ring Oscillator - Key Nodes",
        "X": {
            "signal_key": "raw.time", 
            "label": "Time (s)"
        },
        "Y": [
            {
                "label": "Voltages (V)",
                "signals": {
                    "VDD": "v(vdd)",
                    "Output": "v(bus06)",
                    "Bus07": "v(bus07)"
                }
            },
            {
                "label": "Current (A)", 
                "signals": {
                    "Supply Current": "i(c1)"
                }
            }
        ],
        "plot_height": 600,
        "show_rangeslider": True
    }
    
    print("Creating plot with custom configuration...")
    fig2 = wv.plot(spice_file, custom_config, show=True)
    print(f"✅ Custom plot created with {len(fig2.data)} traces")
    
    # 4. ADVANCED PLOTTER WITH SIGNAL PROCESSING
    print("\n4️⃣  Advanced Features")
    print("-" * 20)
    
    plotter = wv.SpicePlotter(spice_file)
    
    # Add processed signals
    plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(c1)"])
    plotter.add_processed_signal("inverted_output", lambda d: -d["v(bus06)"])
    
    print(f"📈 Added {len(plotter.processed_signals)} processed signals")
    
    # Use config with processed signals
    advanced_config = {
        "title": "Ring Oscillator - With Processing",
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [
            {
                "label": "Processed Signals",
                "signals": {
                    "Power": "data.power",
                    "Inverted Output": "data.inverted_output"
                }
            }
        ]
    }
    
    plotter.load_config(advanced_config)
    fig3 = plotter.create_figure()
    print(f"✅ Advanced plot with processed signals: {len(fig3.data)} traces")
    
    # 5. CONFIGURATION TEMPLATE GENERATION
    print("\n5️⃣  Configuration Template")
    print("-" * 27)
    
    template_file = "demo_template.yaml"
    wv.create_config_template(template_file, spice_file)
    print(f"📝 Template created: {template_file}")
    
    # Show template content
    with open(template_file, 'r') as f:
        lines = f.readlines()[:15]  # Show first 15 lines
        print("📄 Template preview:")
        for line in lines:
            print(f"   {line.rstrip()}")
        if len(lines) == 15:
            print("   ...")
    
    # 6. CONFIGURATION VALIDATION
    print("\n6️⃣  Configuration Validation")
    print("-" * 28)
    
    warnings = wv.validate_config(template_file, spice_file)
    if warnings:
        print("⚠️  Configuration warnings:")
        for warning in warnings:
            print(f"   • {warning}")
    else:
        print("✅ Configuration validation passed")
    
    # Clean up
    os.remove(template_file)
    
    print("\n" + "=" * 40)
    print("🎉 Demo Complete!")
    print("\nTypical user workflow:")
    print("1. wv.load_spice() - explore signals")  
    print("2. wv.plot() - quick visualization")
    print("3. Custom configs - detailed analysis")
    print("4. SpicePlotter - advanced processing")
    print("5. Templates - reusable configurations")
    
    print("\n💡 To see plots in browser, use show=True")
    print("   Example: wv.plot('file.raw', show=True)")

if __name__ == "__main__":
    main() 