from dash import Dash, html, Input, Output
import dash_bootstrap_components as dbc
import dash

from UIComponents.Navbar import navbar
from UIComponents.tabs import left_tabs
from UIComponents.MaterialProperties import material_properties
from UIComponents.MaterialProperties2 import metal_site_defects
from UIComponents.MaterialProperties3 import chalcogen_site_defects




                                            # 0-Main UI Layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    navbar,
    html.Div(
        [
            html.Div(
                [
                    left_tabs(),
                    material_properties(),
                    metal_site_defects(),
                    chalcogen_site_defects(),
                ],
                className="tab-with-panel"
            )
        ],
        className="section-container"
    )
])



                                        #1-Functions for Interactivity

                                        # On/Off Button Functionality
@app.callback(
    # Update the CSS classes of both buttons
    Output("btn-material", "className"),
    Output("btn-microscope", "className"),
    # Show or hide the Material Properties panel
    Output("material-panel", "style"),
    # Show or hide the Metal Site Defects panel
    Output("metal-defects-panel", "style"),
    # Show or hide the Chalcogen Site Defects panel
    Output("metal-Chalcogen-panel", "style"),

    # Track clicks for both buttons
    Input("btn-material", "n_clicks"),
    Input("btn-microscope", "n_clicks"),
)

def toggle_buttons(material_clicks, microscope_clicks):
    # Styles for show/hide
    visible = {"display": "block"} # Show
    hidden = {"display": "none"} #Hide

    # Default State
    if not material_clicks and not microscope_clicks:
        return (
            "param-btn active-param-btn",    # Material active
            "param-btn",                     # Microscope inactive
            visible,                         # Material panel Visible
            visible,                         # Metal defects panel Visible
            visible                          # Chalcogen defects panel Visible
        )

    # Which button was clicked?
    ctx = dash.callback_context.triggered_id

    # Update Button styles
    if ctx == "btn-material":
        return (
            "param-btn active-param-btn",
            "param-btn",
            visible,
            visible,
            visible
        )
    else:
        return (
            "param-btn",
            "param-btn active-param-btn",
            hidden,
            hidden,
            hidden
        )

if __name__ == "__main__":
    app.run(debug=True)