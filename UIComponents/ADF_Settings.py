from dash import html, dcc

'''
Second Part, Part 3
'''
def ADF_Settings():
    return html.Div(
        [
            html.H4("ADF Detector Settings", className="section-title"),
            html.P("Angle Configuration", className="section-subtitle"),

            html.Div(
                [
                    # Column 1
                    html.Div(
                        [
                            html.Label("ADF Angle Min"),
                            dcc.Input(
                                id="adf-angle-min",
                                type="number",
                                value=0,
                                className="input-field"
                            ),

                            html.Label("ADF Angle Max"),
                            dcc.Input(
                                id="adf-angle-max",
                                type="number",
                                value=0,
                                className="input-field"
                            ),
                        ],
                        className="form-col"
                    ),
                ]
            ),
        ],
        id="ADF_Panel",
        className="ADF_Panel"
    )
