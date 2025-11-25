from dash import html, dcc

def metal_site_defects():
    return html.Div(
        [
            html.H4("Metal Site Defects", className="section-title"),
            html.P("Configure substitutions and vacancies on metal sites: Defects accept from 0 to 1.0 concentrations", className="section-subtitle"),

            html.Div(
                [
                    # Column 1
                    html.Div(
                        [
                            html.Label("Substitution Atom Number"),
                            dcc.Input(
                                id="sub-atom-metal",
                                type="number",
                                value=0,
                                className="input-field"
                            ),

                            html.Label("Metal Substitution Concentration"),
                            dcc.Input(
                                id="metal-sub-conc",
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
                            html.Label("Metal Vacancy Concentration"),
                            dcc.Input(
                                id="metal-vac-conc",
                                type="number",
                                value=0.080,
                                step=0.001,
                                max=1.000,
                                className="input-field"
                            ),
                        ],
                        className="form-col"
                    )
                ],
                className="form-grid"
            )
        ],
        id="metal-defects-panel",
        className="material-panel2"
    )
