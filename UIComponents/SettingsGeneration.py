from dash import html, dcc

def generation_settings():
    return html.Div(
        [
            # Input Values Display Box - appears first
            values_display(),
            
            # Generation Settings Panel - appears below
            html.Div(
                [
                    html.Div(
                        [
                            html.I(className="fas fa-sliders-h", style={"marginRight": "10px"}),
                            html.Span("Generation Settings")
                        ],
                        className="right-panel-title"
                    ),
                    html.P("Configure batch size and start generation", className="right-panel-subtitle"),
                    html.Label("Batch Size", className="batch-label"),
                    dcc.Dropdown(
                        id="batch-size-dropdown",
                        options=[
                            {"label": "1 image", "value": 1},
                            {"label": "5 images", "value": 5},
                            {"label": "10 images", "value": 10},
                            {"label": "20 images", "value": 20},
                            {"label": "50 images", "value": 50},
                            {"label": "100 images", "value": 100},
                            {"label": "200 images", "value": 200},
                            {"label": "300 images", "value": 300},
                            {"label": "500 images", "value": 500},
                            {"label": "700 images", "value": 700},
                            {"label": "1000 images", "value": 1000},
                        ],
                        value=1,
                        clearable=False,
                        className="batch-dropdown"
                    ),
                    
                    html.Button(
                        [
                            html.I(className="fas fa-play", style={"marginRight": "10px"}),
                            "Input the Parameters"
                        ],
                        id="generate-btn",
                        className="generate-btn"
                    )
                ],
                className="right-panel generation-panel"
            )
        ],
        className="right-panel-container"
    )

def values_display():
    return html.Div(
        [
            html.Div(
                [
                    html.I(className="fas fa-clipboard-list", style={"marginRight": "10px"}),
                    html.Span("Input Values")
                ],
                className="right-panel-title"
            ),
            html.Div(id="values-display-content", className="values-display-box")
        ],
        className="right-panel values-panel"
    )
