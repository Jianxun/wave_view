#!/usr/bin/env python3
"""
SPICE Signal Explorer - Prototype
Demonstrates API for discovering and categorizing signals in SPICE raw files
"""

from spicelib import RawRead
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import numpy as np

@dataclass
class SignalInfo:
    """Information about a single signal"""
    name: str
    type: str  # 'voltage', 'current', 'device_terminal', 'other'
    units: str
    description: str
    device: Optional[str] = None  # For device terminals
    terminal: Optional[str] = None  # For device terminals

class SpiceSignalExplorer:
    """Explores and categorizes signals in SPICE raw files"""
    
    def __init__(self, raw_file_path: str):
        self.raw_file_path = raw_file_path
        self.raw_data = RawRead(raw_file_path)
        self._signals_info = None
        self._analyze_signals()
    
    def _analyze_signals(self):
        """Analyze and categorize all signals"""
        trace_names = self.raw_data.get_trace_names()
        self._signals_info = []
        
        for trace in trace_names:
            signal_info = self._categorize_signal(trace)
            self._signals_info.append(signal_info)
    
    def _categorize_signal(self, signal_name: str) -> SignalInfo:
        """Categorize a single signal and extract information"""
        name_lower = signal_name.lower()
        
        # Time axis
        if name_lower == 'time':
            return SignalInfo(
                name=signal_name,
                type='time',
                units='s',
                description='Time axis'
            )
        
        # Voltage signals: V(node) or v(node)
        if re.match(r'^[vV]\([^)]+\)$', signal_name):
            node_name = signal_name[2:-1]  # Extract node name
            return SignalInfo(
                name=signal_name,
                type='voltage',
                units='V',
                description=f'Voltage at node {node_name}'
            )
        
        # Current signals: I(element) or i(element)
        if re.match(r'^[iI]\([^)]+\)$', signal_name):
            element_name = signal_name[2:-1]  # Extract element name
            return SignalInfo(
                name=signal_name,
                type='current',
                units='A',
                description=f'Current through {element_name}'
            )
        
        # Device terminal signals: Ix(device:terminal)
        device_match = re.match(r'^[iI]x\(([^:]+):([^)]+)\)$', signal_name)
        if device_match:
            device_name = device_match.group(1)
            terminal_name = device_match.group(2)
            return SignalInfo(
                name=signal_name,
                type='device_terminal',
                units='A',
                description=f'Current at {terminal_name} terminal of {device_name}',
                device=device_name,
                terminal=terminal_name
            )
        
        # Frequency (for AC analysis)
        if name_lower in ['frequency', 'freq', 'f']:
            return SignalInfo(
                name=signal_name,
                type='frequency',
                units='Hz',
                description='Frequency axis'
            )
        
        # Default: other/unknown
        return SignalInfo(
            name=signal_name,
            type='other',
            units='unknown',
            description=f'Signal: {signal_name}'
        )
    
    @property
    def file_info(self) -> Dict[str, Any]:
        """Get file metadata"""
        return {
            'path': self.raw_file_path,
            'type': getattr(self.raw_data, 'raw_type', 'Unknown'),
            'variables': self.raw_data.nVariables,
            'data_points': self.raw_data.nPoints,
            'total_signals': len(self._signals_info)
        }
    
    @property
    def all_signals(self) -> List[SignalInfo]:
        """Get all signals"""
        return self._signals_info.copy()
    
    def get_signals_by_type(self) -> Dict[str, List[SignalInfo]]:
        """Get signals categorized by type"""
        categories = {}
        for signal in self._signals_info:
            signal_type = signal.type
            if signal_type not in categories:
                categories[signal_type] = []
            categories[signal_type].append(signal)
        return categories
    
    def get_devices(self) -> Dict[str, List[SignalInfo]]:
        """Get device terminal signals grouped by device"""
        devices = {}
        for signal in self._signals_info:
            if signal.type == 'device_terminal' and signal.device:
                if signal.device not in devices:
                    devices[signal.device] = []
                devices[signal.device].append(signal)
        return devices
    
    def search(self, query: str, case_sensitive: bool = False) -> List[SignalInfo]:
        """Search for signals containing the query string"""
        if not case_sensitive:
            query = query.lower()
        
        results = []
        for signal in self._signals_info:
            search_text = signal.name if case_sensitive else signal.name.lower()
            if query in search_text:
                results.append(signal)
        return results
    
    def get_signal_names(self, signal_type: Optional[str] = None) -> List[str]:
        """Get list of signal names, optionally filtered by type"""
        if signal_type is None:
            return [s.name for s in self._signals_info]
        return [s.name for s in self._signals_info if s.type == signal_type]
    
    def display_summary(self):
        """Display a formatted summary of the file and signals"""
        print("=" * 60)
        print(f"SPICE Raw File Analysis: {self.raw_file_path}")
        print("=" * 60)
        
        # File info
        info = self.file_info
        print(f"File Type: {info['type']}")
        print(f"Variables: {info['variables']}")
        print(f"Data Points: {info['data_points']}")
        print(f"Total Signals: {info['total_signals']}")
        print()
        
        # Signal categories
        by_type = self.get_signals_by_type()
        print("Signal Categories:")
        for signal_type, signals in by_type.items():
            print(f"  {signal_type.replace('_', ' ').title()}: {len(signals)}")
        print()
        
        # Detailed breakdown
        for signal_type, signals in by_type.items():
            if not signals:
                continue
                
            print(f"{signal_type.replace('_', ' ').title()} Signals:")
            for signal in signals[:10]:  # Show first 10
                print(f"  {signal.name:20} - {signal.description}")
            if len(signals) > 10:
                print(f"  ... and {len(signals) - 10} more")
            print()
        
        # Device breakdown (if any)
        devices = self.get_devices()
        if devices:
            print("Device Terminal Signals:")
            for device, terminals in devices.items():
                terminal_names = [t.terminal for t in terminals]
                print(f"  {device}: {', '.join(terminal_names)}")
            print()
    
    def display_tree(self):
        """Display signals in a tree-like structure"""
        print("Signal Tree Structure:")
        print("├── Time/Frequency")
        
        by_type = self.get_signals_by_type()
        
        # Time signals
        time_signals = by_type.get('time', []) + by_type.get('frequency', [])
        for signal in time_signals:
            print(f"│   └── {signal.name}")
        
        # Voltage signals
        if 'voltage' in by_type:
            print("├── Voltages")
            for signal in by_type['voltage']:
                print(f"│   └── {signal.name}")
        
        # Current signals
        if 'current' in by_type:
            print("├── Currents")
            for signal in by_type['current']:
                print(f"│   └── {signal.name}")
        
        # Device terminals
        devices = self.get_devices()
        if devices:
            print("├── Device Terminals")
            for device, terminals in devices.items():
                print(f"│   ├── {device}")
                for terminal in terminals:
                    print(f"│   │   └── {terminal.name} ({terminal.terminal})")
        
        # Other signals
        if 'other' in by_type:
            print("└── Other Signals")
            for signal in by_type['other']:
                print(f"    └── {signal.name}")

def quick_explore(raw_file_path: str):
    """Quick exploration function - simple API"""
    explorer = SpiceSignalExplorer(raw_file_path)
    explorer.display_summary()
    return explorer

# Example usage
if __name__ == "__main__":
    # Demonstrate the API
    explorer = quick_explore("./Ring_Oscillator_7stage.raw")
    
    print("\n" + "="*60)
    print("API DEMONSTRATION")
    print("="*60)
    
    # Show different ways to access signals
    print("1. All voltage signals:")
    voltages = explorer.get_signal_names('voltage')
    print(f"   {voltages}")
    
    print("\n2. Search for 'bus' signals:")
    bus_signals = explorer.search('bus')
    for signal in bus_signals:
        print(f"   {signal.name} - {signal.description}")
    
    print("\n3. Device breakdown:")
    devices = explorer.get_devices()
    for device, terminals in list(devices.items())[:3]:  # Show first 3 devices
        print(f"   {device}: {[t.terminal for t in terminals]}")
    
    print("\n4. Tree structure:")
    explorer.display_tree() 