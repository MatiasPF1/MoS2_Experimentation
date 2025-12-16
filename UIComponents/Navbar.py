from dash import html
import dash_bootstrap_components as dbc


navbar = html.Div(
    [
        dbc.Navbar(
            dbc.Container(
                [
                    html.Div(
                        [
                            html.I(className="", style={
                                "fontSize": "24px", 
                                "marginRight": "12px",
                                "color": "#f0f0f5",
                            }),
                            html.Span("MoS₂", style={
                                "fontWeight": "700",
                                "fontSize": "22px",
                                "color": "#f0f0f5",
                            }),
                            html.Span(" Image Synthesis Platform", style={
                                "fontWeight": "600",
                                "fontSize": "20px",
                                "color": "#f0f0f5",
                                "marginLeft": "4px"
                            }),
                        ],
                        style={"display": "flex", "alignItems": "center"}
                    )
                ],
                fluid=True,
                style={"display": "flex", "justifyContent": "center", "alignItems": "center"}
            ),
            className="navbar-custom",
            dark=True
        ),
        html.Hr(className="navbar-separator")
    ]
)