from dash import html, dcc




'''
Second Part, Part 1
'''

def Microscope_Settings():
    return html.Div(
        [
            html.H4("Basic Microscope Settings", className="section-title"),
            html.P("Configure electron microscope operational parameters", className="section-subtitle"),

            html.Div(
                [
                    # Column 1
                    html.Div(
                        [
                            html.Label("Voltage(kV)"),
                            dcc.Input(
                                type="text",
                                value=300,
                                className="input-field"
                            ),

                            html.Label("Aperture"),
                            dcc.Input(
                                type="number",
                                value=75,
                                className="input-field"
                            ),
                        ],
                        className="form-col"
                    ),

                    # Column 2
                    html.Div(
                        [
                            html.Label("Defocus(df)"),
                            dcc.Input(
                                type="number",
                                value=25,
                                className="input-field"
                            ),

                            html.Label("Dwell Time"),
                            dcc.Input(
                                type="number",
                                value=1,
                                className="input-field"
                            ),

                            html.Label("Chalcogen Site Atom Number"),
                            dcc.Input(
                                type="number",
                                value=16,
                                className="input-field"
                            )
                        ],
                        className="form-col"
                    )
                ],
                className="form-grid"
            )
        ],
        id="microscope-panel",
        className="microscope-panel"
    )
