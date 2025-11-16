from dash import html
def left_tabs():
    return html.Div(
        [
            html.Div(
                [
                #1-First Button: Material Parameters
                html.Button(     
                        [html.I(className="fa-solid fa-atom me-2"), "Material Parameters"],
                        id="btn-material",
                        className="param-btn active-param-btn"),      #Active by Defau.t
                
                #2-Second Button: Microscope Parameters
                html.Button(
                        [html.I(className="fa-solid fa-microscope me-2"), "Microscope Parameters"],
                        id="btn-microscope",
                        className="param-btn"
                    )
                ],
                className="param-btn-container"
            )
        ],
        className="left-panel"
    )