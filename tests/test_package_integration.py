#!/usr/bin/env python3
"""
Integration test for Wave View package using real SPICE data.

This script tests the main package functionality with the test data
from the prototype directory.
"""

import sys
import os

# Add wave_view package to path
sys.path.insert(0, './wave_view')

try:
    import wave_view as wv
    print("✓ Successfully imported wave_view package")
except ImportError as e:
    print(f"❌ Failed to import wave_view: {e}")
    sys.exit(1)

def test_spice_data_loading():
    """Test loading SPICE data."""
    print("\n=== Testing SpiceData Loading ===")
    raw_file = "prototype/script/Ring_Oscillator_7stage.raw"
    
    try:
        data = wv.load_spice(raw_file)
        print(f"✓ Loaded SPICE file: {data}")
        print(f"✓ Found {len(data.signals)} signals")
        print(f"✓ Sample signals: {data.signals[:5]}")
        
        # Test case-insensitive access
        vdd_lowercase = data.get_signal("v(vdd)")
        vdd_uppercase = data.get_signal("V(VDD)")
        vdd_mixed = data.get_signal("V(vdd)")
        
        if len(vdd_lowercase) == len(vdd_uppercase) == len(vdd_mixed):
            print("✓ Case-insensitive signal access works")
        else:
            print("❌ Case-insensitive access failed")
            return None
        
        return data
    except Exception as e:
        print(f"❌ Failed to load SPICE data: {e}")
        return None

def test_config_loading():
    """Test loading configuration."""
    print("\n=== Testing Configuration Loading ===")
    config_file = "prototype/script/plot_config.yaml"
    
    try:
        config = wv.config_from_file(config_file)
        print(f"✓ Loaded configuration: {config}")
        print(f"✓ Config type: {type(config)}")
        print(f"✓ Config has title: {'title' in config.config}")
        return config
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return None

def test_config_validation():
    """Test configuration validation with SPICE data."""
    print("\n=== Testing Configuration Validation ===")
    
    try:
        config_file = "test_config_corrected.yaml"
        raw_file = "prototype/script/Ring_Oscillator_7stage.raw"
        
        warnings = wv.validate_config(config_file, raw_file)
        if warnings:
            print("⚠️  Configuration warnings:")
            for warning in warnings:
                print(f"   - {warning}")
        else:
            print("✓ Configuration validation passed")
        return len(warnings) == 0
    except Exception as e:
        print(f"❌ Failed to validate configuration: {e}")
        return False

def test_advanced_plotter():
    """Test advanced plotter functionality."""
    print("\n=== Testing Advanced Plotter ===")
    
    try:
        raw_file = "prototype/script/Ring_Oscillator_7stage.raw"
        config_file = "test_config_corrected.yaml"
        
        # Create plotter
        plotter = wv.SpicePlotter(raw_file)
        plotter.load_config(config_file)
        
        print(f"✓ Created plotter: {plotter}")
        
        # Test processed signals - use lowercase signal name
        plotter.add_processed_signal("inverted_vdd", lambda d: -d["v(vdd)"])
        print("✓ Added processed signal")
        
        # Create figure (but don't show it)
        fig = plotter.create_figure()
        print(f"✓ Created figure with {len(fig.data)} traces")
        
        return True
    except Exception as e:
        print(f"❌ Failed advanced plotter test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_api():
    """Test the simple API."""
    print("\n=== Testing Simple API ===")
    
    try:
        raw_file = "prototype/script/Ring_Oscillator_7stage.raw"
        config_file = "test_config_corrected.yaml"
        
        # Test plot function (don't show)
        fig = wv.plot(raw_file, config_file, show=False)
        print(f"✓ Simple plot created with {len(fig.data)} traces")
        
        return True
    except Exception as e:
        print(f"❌ Failed simple API test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_signal_exploration():
    """Test signal exploration functionality."""
    print("\n=== Testing Signal Exploration ===")
    
    try:
        raw_file = "prototype/script/Ring_Oscillator_7stage.raw"
        
        # Test explore_signals function
        signals = wv.explore_signals(raw_file)
        print(f"✓ Signal exploration completed, found {len(signals)} signals")
        
        # Verify we got a list of strings
        if isinstance(signals, list) and len(signals) > 0:
            print(f"✓ Signal list contains: {signals[:3]}...")  # Show first 3
            return True
        else:
            print("❌ Signal exploration returned invalid data")
            return False
            
    except Exception as e:
        print(f"❌ Failed signal exploration test: {e}")
        return False

def main():
    """Run all integration tests."""
    print("🧪 Wave View Package Integration Tests")
    print("=" * 50)
    
    tests = [
        test_spice_data_loading,
        test_config_loading,
        test_config_validation,
        test_advanced_plotter,
        test_simple_api,
        test_signal_exploration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result is not False)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("🏁 Test Summary")
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The package is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Package needs fixes.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 