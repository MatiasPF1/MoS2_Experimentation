from dash import Dash, html, Input, Output
import dash_bootstrap_components as dbc
import dash

#First Tab Components
from UIComponents.Navbar import navbar
from UIComponents.tabs import left_tabs
from UIComponents.MaterialProperties import material_properties
from UIComponents.MaterialProperties2 import metal_site_defects
from UIComponents.MaterialProperties3 import chalcogen_site_defects
from UIComponents.SettingsGeneration import generation_settings

#Second Tab Components 
from UIComponents.BasicMicroscopeSettings import Microscope_Settings
from UIComponents.aberrationCoeficcients import Abberation_Coeficients






                                            # 0-Main UI Layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    navbar,
    html.Div(
        [
            # Left side - Tabs and parameter panels
            html.Div(
                [
                    left_tabs(),

                    #Material Section Panels 
                    material_properties(),
                    metal_site_defects(),
                    chalcogen_site_defects(),

                    #Miscroscope Section Panels
                    Microscope_Settings(),
                    Abberation_Coeficients()
                ],
                className="tab-with-panel"
            ),
            # Right side - Generation settings and config
            generation_settings()
        ],
        className="section-container"
    )
])





                                        #1-Functions for Interactivity

                                        # On/Off Button Functionality
@app.callback(
    #Button Outputs 
    Output("btn-material", "className"),
    Output("btn-microscope", "className"),

    #First Tab Ouputs
    Output("material-panel", "style"),
    Output("metal-defects-panel", "style"),
    Output("metal-Chalcogen-panel", "style"),

    #Second Tab Outputs
    Output("microscope-panel", "style"),
    Output("aberration-panel", "style"),


    #Click Inputs by User
    Input("btn-material", "n_clicks"),
    Input("btn-microscope", "n_clicks"),
)


def toggle_buttons(material_clicks, microscope_clicks):
    # Styles for show/hide
    visible = {"display": "block"} # Show
    hidden = {"display": "none"} #Hide

                                        #1-Default State(param-btn By Default Active)

    if not material_clicks and not microscope_clicks:
        return (
            "param-btn active-param-btn",    # Material active
            "param-btn",                     # Microscope inactive
            visible,                         # Material panel Visible
            visible,                         # Metal defects panel Visible
            visible,                          # Chalcogen defects panel Visible

            hidden,                        # Microscope panel Hidden
            hidden                         # Aberration panel Hidden
        )

                                        #2- User Selection of Button
                                        
     # Which button was clicked?
    ctx = dash.callback_context.triggered_id


    # If Material Button Clicked
    if ctx == "btn-material":
        return (
        "param-btn active-param-btn",
        "param-btn",
        visible,  # material
        visible,  # metal defects
        visible,  # chalcogen defects
        hidden,   # microscope is hidden
        hidden    # aberration is hidden
    )

    # If Microscope Button Clicked
    elif ctx == "btn-microscope":
        return (
        "param-btn",
        "param-btn active-param-btn",
        hidden,   # material  is hidden
        hidden,   # metal defects is hidden
        hidden,   # chalcogen defects is hidden
        visible,  # microscope
        visible   # aberration
    )


if __name__ == "__main__":
    app.run(debug=True)