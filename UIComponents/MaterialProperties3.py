from dash import html, dcc

def chalcogen_site_defects():
    return html.Div(
        [
            html.H4("Chalcogen Site Defects", className="section-title"),
            html.P("Configure substitutions and vacancies on Chalcogen sites: Defects accept from 0 to 1.0 concentrations", className="section-subtitle"),

            html.Div(
                [
                    # Column 1
                    html.Div(
                        [
                            html.Label("Substitution Atom Number"),
                            dcc.Input(
                                type="number",
                                value=0,
                                className="input-field"
                            ),

                            html.Label("Chalcogen Substitution Concentration"),
                            dcc.Input(
                                type="number",
                                value=0.000,
                                step=0.001,
                                max=1.000,
                                className="input-field"
                            ),

                            html.Label("One Vacancy Type Concentration"),
                            dcc.Input(
                                type="number",
                                value=0.000,
                                step=0.001,
                                max=1.000,
                                className="input-field"
                            ),
                        ],
                        className="form-col"
                    ),

                    # Column 2
                    html.Div(
                        [
                            html.Label("Two Vacancy Type Concentration"),
                            dcc.Input(
                                type="number",
                                value=0.000,
                                step=0.001,
                                max=1.000,
                                className="input-field"
                            ),

                            html.Label("Two Substitution Type Concentration"),
                            dcc.Input(
                                type="number",
                                value=0.000,
                                step=0.001,
                                max=1.000,
                                className="input-field"
                            ),

                            html.Label("One Substitution Type Concentration"),
                            dcc.Input(
                                type="number",
                                value=0.000,
                                step=0.001,
                                max=1.000,
                                className="input-field"
                            ),
                        ],
                        className="form-col"
                    ),
                ],
                className="form-grid"
            )
        ],
        id="metal-Chalcogen-panel",
        className="material-panel2"
    )