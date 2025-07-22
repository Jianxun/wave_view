#!/usr/bin/env python
"""
Detailed exploration of spicelib RawRead metadata capabilities.
This script tries various methods to extract all available metadata from SPICE raw files.
"""

from spicelib import RawRead
from pathlib import Path
import sys

def detailed_metadata_exploration(raw_file_path: str):
    """Thoroughly explore all available metadata from a SPICE raw file."""
    
    try:
        raw = RawRead(raw_file_path)
        print(f"=== Detailed Analysis: {raw_file_path} ===\n")
        
        # Basic file information
        print("1. BASIC FILE INFORMATION:")
        print(f"   File path: {raw_file_path}")
        print(f"   Number of traces: {len(raw.get_trace_names())}")
        print(f"   Number of steps: {len(raw.get_steps())}")
        
        # Try to access the raw object's internal attributes
        print("\n2. RAW OBJECT ATTRIBUTES:")
        attrs = [attr for attr in dir(raw) if not attr.startswith('_')]
        print(f"   Available attributes: {attrs}")
        
        # Try get_raw_property with no arguments (should return all)
        print("\n3. RAW PROPERTIES (get_raw_property()):")
        try:
            properties = raw.get_raw_property()
            if properties:
                if isinstance(properties, dict):
                    for key, value in properties.items():
                        print(f"   {key}: {value}")
                else:
                    print(f"   Raw properties: {properties}")
            else:
                print("   No properties returned")
        except Exception as e:
            print(f"   Error getting properties: {e}")
            
        # Try accessing specific properties that might exist
        print("\n4. SPECIFIC PROPERTY ATTEMPTS:")
        common_properties = [
            'title', 'date', 'plotname', 'flags', 'command',
            'no_of_variables', 'no_of_points', 'variables'
        ]
        
        for prop in common_properties:
            try:
                value = raw.get_raw_property(prop)
                print(f"   {prop}: {value}")
            except Exception as e:
                print(f"   {prop}: Error - {e}")
        
        # Check if there's a header or metadata attribute
        print("\n5. INTERNAL DATA STRUCTURES:")
        internal_attrs = ['header', 'metadata', '_header', '_metadata', 'raw_params']
        for attr in internal_attrs:
            if hasattr(raw, attr):
                try:
                    value = getattr(raw, attr)
                    print(f"   {attr}: {type(value)} - {value}")
                except Exception as e:
                    print(f"   {attr}: Error accessing - {e}")
            else:
                print(f"   {attr}: Not available")
                
        # Try to get trace information with units
        print("\n6. TRACE DETAILS:")
        trace_names = raw.get_trace_names()
        for i, trace_name in enumerate(trace_names[:5]):  # First 5 traces
            try:
                trace = raw.get_trace(trace_name)
                print(f"   [{i}] {trace_name}:")
                print(f"       Type: {type(trace)}")
                if hasattr(trace, 'get_wave'):
                    wave = trace.get_wave(0)  # Get first step
                    print(f"       Wave shape: {wave.shape if hasattr(wave, 'shape') else len(wave)}")
                    print(f"       Wave type: {type(wave)}")
                # Check if trace has any metadata
                trace_attrs = [attr for attr in dir(trace) if not attr.startswith('_')]
                print(f"       Trace attributes: {trace_attrs}")
            except Exception as e:
                print(f"   [{i}] {trace_name}: Error - {e}")
        
        # Check axis information
        print("\n7. AXIS INFORMATION:")
        try:
            axis = raw.get_axis()
            print(f"   Axis type: {type(axis)}")
            print(f"   Axis shape: {axis.shape if hasattr(axis, 'shape') else len(axis)}")
            if hasattr(axis, '__len__') and len(axis) > 0:
                print(f"   Range: {axis[0]} to {axis[-1]}")
                print(f"   Sample values: {axis[:3]} ... {axis[-3:]}")
        except Exception as e:
            print(f"   Error accessing axis: {e}")
            
        # Check step information
        print("\n8. STEP DETAILS:")
        try:
            steps = raw.get_steps()
            print(f"   Steps: {steps}")
            print(f"   Step type: {type(steps)}")
        except Exception as e:
            print(f"   Error accessing steps: {e}")
            
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"ERROR: Could not analyze {raw_file_path}: {e}")

if __name__ == "__main__":
    # Look for test raw files
    test_dirs = [
        Path("tests/raw_files"),
        Path("tests/data"), 
        Path("test_data"),
        Path("examples")
    ]
    
    raw_files = []
    for test_dir in test_dirs:
        if test_dir.exists():
            raw_files.extend(test_dir.glob("*.raw"))
    
    if not raw_files and len(sys.argv) > 1:
        raw_files = [Path(sys.argv[1])]
    
    if not raw_files:
        print("No .raw files found. Please provide a path as an argument.")
        sys.exit(1)
    
    # Analyze the first raw file found
    detailed_metadata_exploration(str(raw_files[0]))