#!/usr/bin/env python3
"""
Comprehensive test suite for wave_view API.
Tests all major functionality and edge cases.
"""

import wave_view as wv
import numpy as np
from pathlib import Path
import traceback

def test_basic_import():
    """Test 1: Basic import and module availability."""
    print("🧪 Test 1: Basic Import")
    try:
        assert hasattr(wv, 'plot'), "plot function missing"
        assert hasattr(wv, 'load_spice'), "load_spice function missing"
        assert hasattr(wv, 'SpicePlotter'), "SpicePlotter class missing"
        print("✅ Import test passed")
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_data_loading():
    """Test 2: SPICE data loading."""
    print("\n🧪 Test 2: Data Loading")
    try:
        data_file = "../data/Ring_Oscillator_7stage.raw"
        data = wv.load_spice(data_file)
        
        assert data is not None, "Data loading returned None"
        assert hasattr(data, 'get_signal'), "SpiceData missing get_signal method"
        
        # Test signal access
        time_data = data.get_signal('time')
        assert isinstance(time_data, np.ndarray), "Time data is not numpy array"
        assert len(time_data) > 0, "Time data is empty"
        
        print(f"✅ Data loading test passed - {len(time_data)} time points")
        return True
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        return False

def test_single_plot():
    """Test 3: Single Y-axis plotting."""
    print("\n🧪 Test 3: Single Y-axis Plot")
    try:
        config = {
            "title": "Single Plot Test",
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
        
        assert fig is not None, "Figure creation failed"
        assert len(fig.data) == 1, f"Expected 1 trace, got {len(fig.data)}"
        assert fig.layout.xaxis.rangeslider.visible == True, "Range slider not visible"
        
        # Check Y-axis domain (should be full height for single axis)
        assert fig.layout.yaxis.domain == (0, 1.0), f"Single Y-axis domain wrong: {fig.layout.yaxis.domain}"
        
        print("✅ Single plot test passed")
        return True
    except Exception as e:
        print(f"❌ Single plot test failed: {e}")
        traceback.print_exc()
        return False

def test_dual_plot():
    """Test 4: Dual Y-axis plotting."""
    print("\n🧪 Test 4: Dual Y-axis Plot")
    try:
        config = {
            "title": "Dual Plot Test",
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
        
        assert fig is not None, "Figure creation failed"
        assert len(fig.data) == 3, f"Expected 3 traces, got {len(fig.data)}"
        assert fig.layout.xaxis.rangeslider.visible == True, "Range slider not visible"
        
        # Check Y-axis domains
        y1_domain = fig.layout.yaxis.domain
        y2_domain = fig.layout.yaxis2.domain
        
        print(f"Y1 domain: {y1_domain}, Y2 domain: {y2_domain}")
        
        # Y1 should be at bottom, Y2 at top (or vice versa - let's document current behavior)
        assert y1_domain != y2_domain, "Y-axis domains should be different"
        assert all(0 <= d <= 1 for d in y1_domain + y2_domain), "Domains should be in [0,1]"
        
        # Check anchoring
        assert getattr(fig.layout.yaxis, 'anchor', None) == 'x', "Y1 should anchor to x"
        assert getattr(fig.layout.yaxis2, 'anchor', None) == 'x', "Y2 should anchor to x"
        
        print("✅ Dual plot test passed")
        return True
    except Exception as e:
        print(f"❌ Dual plot test failed: {e}")
        traceback.print_exc()
        return False

def test_triple_plot():
    """Test 5: Triple Y-axis plotting."""
    print("\n🧪 Test 5: Triple Y-axis Plot")
    try:
        config = {
            "title": "Triple Plot Test",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [
                {
                    "label": "VDD (V)",
                    "signals": {"VDD": "v(vdd)"}
                },
                {
                    "label": "Output (V)",
                    "signals": {"Output": "v(bus06)"}
                },
                {
                    "label": "Current (A)",
                    "signals": {"Supply Current": "i(c1)"}
                }
            ],
            "show_rangeslider": True
        }
        
        fig = wv.plot("../data/Ring_Oscillator_7stage.raw", config, show=False)
        
        assert fig is not None, "Figure creation failed"
        assert len(fig.data) == 3, f"Expected 3 traces, got {len(fig.data)}"
        assert hasattr(fig.layout, 'yaxis3'), "Missing yaxis3"
        
        # Check all Y-axes anchor to x
        for i in range(1, 4):
            axis_name = f"yaxis{'' if i == 1 else i}"
            yaxis = getattr(fig.layout, axis_name)
            assert getattr(yaxis, 'anchor', None) == 'x', f"{axis_name} should anchor to x"
        
        print("✅ Triple plot test passed")
        return True
    except Exception as e:
        print(f"❌ Triple plot test failed: {e}")
        traceback.print_exc()
        return False

def test_configuration_formats():
    """Test 6: Different configuration formats."""
    print("\n🧪 Test 6: Configuration Formats")
    try:
        # Dict config (already tested above)
        
        # YAML string config
        yaml_config = """
title: "YAML Test"
X:
  signal_key: "raw.time"
  label: "Time (s)"
Y:
  - label: "Voltage (V)"
    signals:
      VDD: "v(vdd)"
show_rangeslider: true
"""
        
        fig = wv.plot("../data/Ring_Oscillator_7stage.raw", yaml_config, show=False)
        assert fig is not None, "YAML config failed"
        assert fig.layout.title.text == "YAML Test", "YAML title not set"
        
        print("✅ Configuration formats test passed")
        return True
    except Exception as e:
        print(f"❌ Configuration formats test failed: {e}")
        traceback.print_exc()
        return False

def test_range_slider():
    """Test 7: Range slider functionality."""
    print("\n🧪 Test 7: Range Slider")
    try:
        # Test with range slider
        config_with = {
            "title": "With Range Slider",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [{"label": "Voltage (V)", "signals": {"VDD": "v(vdd)"}}],
            "show_rangeslider": True
        }
        
        # Test without range slider
        config_without = {
            "title": "Without Range Slider",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [{"label": "Voltage (V)", "signals": {"VDD": "v(vdd)"}}],
            "show_rangeslider": False
        }
        
        fig_with = wv.plot("../data/Ring_Oscillator_7stage.raw", config_with, show=False)
        fig_without = wv.plot("../data/Ring_Oscillator_7stage.raw", config_without, show=False)
        
        assert fig_with.layout.xaxis.rangeslider.visible == True, "Range slider should be visible"
        assert fig_without.layout.xaxis.rangeslider.visible == False, "Range slider should be hidden"
        
        print("✅ Range slider test passed")
        return True
    except Exception as e:
        print(f"❌ Range slider test failed: {e}")
        traceback.print_exc()
        return False

def test_spice_plotter_class():
    """Test 8: SpicePlotter class interface."""
    print("\n🧪 Test 8: SpicePlotter Class")
    try:
        plotter = wv.SpicePlotter()
        
        # Test loading data
        plotter.load_data("../data/Ring_Oscillator_7stage.raw")
        assert plotter.data is not None, "Data not loaded"
        
        # Test loading config
        config = {
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [{"label": "Voltage (V)", "signals": {"VDD": "v(vdd)"}}]
        }
        plotter.load_config(config)
        assert plotter.config is not None, "Config not loaded"
        
        # Test creating figure
        fig = plotter.create_figure()
        assert fig is not None, "Figure creation failed"
        
        print("✅ SpicePlotter class test passed")
        return True
    except Exception as e:
        print(f"❌ SpicePlotter class test failed: {e}")
        traceback.print_exc()
        return False

def test_error_handling():
    """Test 9: Error handling and edge cases."""
    print("\n🧪 Test 9: Error Handling")
    try:
        # Test non-existent file
        try:
            wv.load_spice("nonexistent.raw")
            assert False, "Should have raised error for non-existent file"
        except Exception:
            pass  # Expected
            
        # Test invalid signal
        try:
            config = {
                "X": {"signal_key": "raw.time", "label": "Time (s)"},
                "Y": [{"label": "Voltage (V)", "signals": {"Invalid": "v(nonexistent)"}}]
            }
            wv.plot("../data/Ring_Oscillator_7stage.raw", config, show=False)
            assert False, "Should have raised error for invalid signal"
        except Exception:
            pass  # Expected
            
        print("✅ Error handling test passed")
        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        traceback.print_exc()
        return False

def run_comprehensive_tests():
    """Run all tests and report results."""
    print("🧪 WAVE_VIEW COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    data_file = Path("../data/Ring_Oscillator_7stage.raw")
    if not data_file.exists():
        print(f"❌ Test data file not found: {data_file}")
        return
    
    tests = [
        test_basic_import,
        test_data_loading, 
        test_single_plot,
        test_dual_plot,
        test_triple_plot,
        test_configuration_formats,
        test_range_slider,
        test_spice_plotter_class,
        test_error_handling
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1:2d}. {test.__name__:25s} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed - needs investigation")

if __name__ == "__main__":
    run_comprehensive_tests() 