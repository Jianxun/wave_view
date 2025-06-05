#!/usr/bin/env python3
"""
Jupyter Signal Browser - Interactive signal discovery for SPICE files
"""

from signal_explorer import SpiceSignalExplorer, SignalInfo
import pandas as pd
from typing import List, Dict, Optional

class JupyterSignalBrowser:
    """Jupyter-friendly signal browser with rich display capabilities"""
    
    def __init__(self, raw_file_path: str):
        self.explorer = SpiceSignalExplorer(raw_file_path)
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert signals to a pandas DataFrame for easy viewing"""
        signals = self.explorer.all_signals
        data = []
        for signal in signals:
            data.append({
                'Signal': signal.name,
                'Type': signal.type,
                'Units': signal.units,
                'Description': signal.description,
                'Device': signal.device or '',
                'Terminal': signal.terminal or ''
            })
        return pd.DataFrame(data)
    
    def display_rich_summary(self):
        """Display a rich HTML summary for Jupyter"""
        try:
            from IPython.display import display, HTML, Markdown
            
            # File info
            info = self.explorer.file_info
            html = f"""
            <div style="border: 2px solid #3498db; padding: 15px; margin: 10px 0; border-radius: 8px;">
                <h3 style="color: #2c3e50; margin-top: 0;">📊 SPICE Raw File Analysis</h3>
                <p><strong>File:</strong> {info['path']}</p>
                <p><strong>Type:</strong> {info['type']}</p>
                <p><strong>Signals:</strong> {info['total_signals']} | 
                   <strong>Data Points:</strong> {info['data_points']:,}</p>
            </div>
            """
            
            # Signal categories
            by_type = self.explorer.get_signals_by_type()
            html += """
            <div style="border: 2px solid #27ae60; padding: 15px; margin: 10px 0; border-radius: 8px;">
                <h4 style="color: #2c3e50; margin-top: 0;">📈 Signal Categories</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 10px;">
            """
            
            icons = {
                'time': '⏰',
                'voltage': '⚡',
                'current': '🔌',
                'device_terminal': '🔧',
                'frequency': '〰️',
                'other': '❓'
            }
            
            for signal_type, signals in by_type.items():
                icon = icons.get(signal_type, '📊')
                html += f"""
                <div style="background: #ecf0f1; padding: 10px; border-radius: 5px; min-width: 120px;">
                    <div style="font-size: 20px;">{icon}</div>
                    <div style="font-weight: bold;">{signal_type.replace('_', ' ').title()}</div>
                    <div style="color: #7f8c8d;">{len(signals)} signals</div>
                </div>
                """
            
            html += "</div></div>"
            display(HTML(html))
            
        except ImportError:
            # Fallback to text display
            self.explorer.display_summary()
    
    def create_signal_selector(self, signal_types: Optional[List[str]] = None):
        """Create an interactive signal selector widget"""
        try:
            import ipywidgets as widgets
            from IPython.display import display
            
            # Get signals of specified types
            if signal_types:
                all_signals = []
                by_type = self.explorer.get_signals_by_type()
                for stype in signal_types:
                    all_signals.extend(by_type.get(stype, []))
            else:
                all_signals = self.explorer.all_signals
            
            # Create options for the widget
            options = [(f"{s.name} ({s.type})", s.name) for s in all_signals]
            
            # Create multi-select widget
            selector = widgets.SelectMultiple(
                options=options,
                value=[],
                description='Signals:',
                disabled=False,
                style={'description_width': '80px'},
                layout=widgets.Layout(width='400px', height='200px')
            )
            
            # Create output widget
            output = widgets.Output()
            
            def on_selection_change(change):
                with output:
                    output.clear_output()
                    if change['new']:
                        print("Selected signals:")
                        for signal_name in change['new']:
                            signal = next(s for s in all_signals if s.name == signal_name)
                            print(f"  {signal.name} - {signal.description}")
                        
                        # Generate YAML config snippet
                        print("\nYAML Configuration Snippet:")
                        print("Y:")
                        print("  - label: \"Your Label\"")
                        print("    signals:")
                        for signal_name in change['new']:
                            print(f"      {signal_name}: \"{signal_name.lower()}\"")
            
            selector.observe(on_selection_change, names='value')
            
            display(widgets.VBox([
                widgets.HTML("<h4>🔍 Interactive Signal Selector</h4>"),
                selector,
                output
            ]))
            
            return selector
            
        except ImportError:
            print("ipywidgets not available. Install with: pip install ipywidgets")
            return None
    
    def search_widget(self):
        """Create an interactive search widget"""
        try:
            import ipywidgets as widgets
            from IPython.display import display
            
            # Create search input
            search_input = widgets.Text(
                placeholder='Search for signals...',
                description='Search:',
                style={'description_width': '80px'}
            )
            
            # Create output widget
            output = widgets.Output()
            
            def on_search_change(change):
                with output:
                    output.clear_output()
                    query = change['new'].strip()
                    if query:
                        results = self.explorer.search(query)
                        if results:
                            print(f"Found {len(results)} signals matching '{query}':")
                            for signal in results:
                                print(f"  {signal.name:20} - {signal.description}")
                        else:
                            print(f"No signals found matching '{query}'")
            
            search_input.observe(on_search_change, names='value')
            
            display(widgets.VBox([
                widgets.HTML("<h4>🔍 Signal Search</h4>"),
                search_input,
                output
            ]))
            
            return search_input
            
        except ImportError:
            print("ipywidgets not available. Install with: pip install ipywidgets")
            return None

def explore_signals_jupyter(raw_file_path: str):
    """Main function for Jupyter signal exploration"""
    browser = JupyterSignalBrowser(raw_file_path)
    
    # Display rich summary
    browser.display_rich_summary()
    
    # Show signals dataframe
    try:
        from IPython.display import display, HTML
        display(HTML("<h4>📋 All Signals</h4>"))
        display(browser.to_dataframe())
    except ImportError:
        print("\nAll Signals:")
        print(browser.to_dataframe().to_string(index=False))
    
    return browser

# Convenience functions for the main API
def quick_signals_info(raw_file_path: str) -> Dict:
    """Quick function to get signal information as a dictionary"""
    explorer = SpiceSignalExplorer(raw_file_path)
    return {
        'file_info': explorer.file_info,
        'signals_by_type': {k: [s.name for s in v] for k, v in explorer.get_signals_by_type().items()},
        'devices': {k: [s.terminal for s in v] for k, v in explorer.get_devices().items()},
        'all_signals': [s.name for s in explorer.all_signals]
    }

def get_suggested_config(raw_file_path: str, max_signals: int = 5) -> Dict:
    """Generate a suggested plot configuration based on available signals"""
    explorer = SpiceSignalExplorer(raw_file_path)
    by_type = explorer.get_signals_by_type()
    
    config = {
        'title': f'SPICE Analysis - {raw_file_path}',
        'source': raw_file_path,
        'X': {
            'label': 'Time (s)',
            'signal_key': 'raw.time'
        },
        'Y': []
    }
    
    # Add voltage signals
    voltages = by_type.get('voltage', [])
    if voltages:
        voltage_signals = {}
        for signal in voltages[:max_signals]:
            node_name = signal.name[2:-1] if signal.name.startswith('V(') else signal.name
            voltage_signals[node_name] = signal.name.lower()
        
        config['Y'].append({
            'label': 'Voltage (V)',
            'signals': voltage_signals
        })
    
    # Add current signals if available
    currents = by_type.get('current', [])
    if currents and len(config['Y']) == 0:  # Only if no voltages
        current_signals = {}
        for signal in currents[:max_signals]:
            element_name = signal.name[2:-1] if signal.name.startswith('I(') else signal.name
            current_signals[element_name] = signal.name.lower()
        
        config['Y'].append({
            'label': 'Current (A)',
            'signals': current_signals
        })
    
    return config

# Example usage
if __name__ == "__main__":
    print("Testing Jupyter Signal Browser...")
    
    # Test basic functionality
    info = quick_signals_info("./Ring_Oscillator_7stage.raw")
    print(f"File has {len(info['all_signals'])} signals")
    print(f"Voltage signals: {info['signals_by_type'].get('voltage', [])}")
    
    # Test suggested config
    print("\nSuggested configuration:")
    import yaml
    config = get_suggested_config("./Ring_Oscillator_7stage.raw")
    print(yaml.dump(config, default_flow_style=False)) 