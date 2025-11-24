from dash import html, dcc

def material_properties():
    return html.Div(
        [
            html.H4("Basic Material Properties", className="section-title"),
            html.P("Define the fundamental properties of your material sample", className="section-subtitle"),

            html.Div(
                [
                    # Column 1
                    html.Div(
                        [
                            html.Label("Material Name"),
                            dcc.Input(
                                id="Material_Name",
                                type="text",
                                value="MoS2",
                                className="input-field"
                            ),

                            html.Label("Pixel Size (Å)"),
                            dcc.Input(
                                id="Pixel_size",
                                type="number",
                                value=0.1,
                                className="input-field"
                            ),

                            html.Label("Metal Site Atom Number"),
                            dcc.Input(
                                id="Metal_Site_Atom_Num",
                                type="number",
                                value=42,
                                className="input-field"
                            )
                        ],
                        className="form-col"
                    ),

                    # Column 2
                    html.Div(
                        [
                            html.Label("Lattice Constant a (Å)"),
                            dcc.Input(
                                id="Lattice_Constant_Å",
                                type="number",
                                value=3.184,
                                className="input-field"
                            ),

                            html.Label("Image Size (pixels)"),
                            dcc.Input(
                                id="Image_Size",
                                type="number",
                                value=512,
                                className="input-field"
                            ),

                            html.Label("Chalcogen Site Atom Number"),
                            dcc.Input(
                                id="Chalcogen_Site_Atom_Number",
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
        id="material-panel",
        className="material-panel"
    )
