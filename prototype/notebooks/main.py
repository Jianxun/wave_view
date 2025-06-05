#  %%

import plotly.graph_objects as go
import numpy as np
import pandas as pd # pandas is imported but not used, can be removed if not needed elsewhere

t = np.linspace(start=0, stop=np.pi*20, num=1000)

fig = go.Figure()

fig.add_trace(
    go.Scatter(x=t, y=np.sin(t), yaxis="y")
)

fig.add_trace(
    go.Scatter(x=t, y=np.cos(t), yaxis="y2")
)

# Setup vertically stacked y-axes
fig.update_layout(
    xaxis=dict(
        domain=[0, 1],
        rangeslider=dict(visible=True),
        title="Time"
        # fixedrange will be controlled by buttons
    ),
    yaxis=dict(
        domain=[0, 0.45],
        title="Voltage"

        # fixedrange defaults to False, allowing zoom
    ),
    yaxis2=dict(
        domain=[0.55, 1],
        anchor="x",
        title="V"
        # fixedrange defaults to False, allowing zoom
    ),
    height=600,
    
    # Default dragmode
    dragmode='zoom', # Initial mode can be Zoom XY

    # Add modebar buttons
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=1,
            y=1.15, # Adjusted y to ensure buttons are well-placed
            buttons=list([
                dict(
                    label="Zoom XY",
                    method="relayout",
                    args=[{
                        "dragmode": "zoom",
                        "xaxis.fixedrange": False,
                        "yaxis.fixedrange": False, # Explicitly ensure y-axes are zoomable
                        "yaxis2.fixedrange": False
                    }]
                ),
                dict(
                    label="Zoom Y",
                    method="relayout",
                    args=[{
                        "dragmode": "zoom",      # Use 'zoom' dragmode
                        "xaxis.fixedrange": True, # Fix X-axis for Y-only zoom
                        "yaxis.fixedrange": False,
                        "yaxis2.fixedrange": False
                    }]
                ),
                dict(
                    label="Zoom X",
                    method="relayout",
                    args=[{
                        "dragmode": "zoom",      # Use 'zoom' dragmode
                        "xaxis.fixedrange": False, # Fix X-axis for Y-only zoom
                        "yaxis.fixedrange": True,
                        "yaxis2.fixedrange": True
                    }]
                ),
            ]),
            showactive=True,
            pad=dict(t=10) # Added padding for better button appearance
        )
    ]
)

fig.show()

# %%
