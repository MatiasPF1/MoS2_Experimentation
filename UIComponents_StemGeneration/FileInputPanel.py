from dash import html


########################################################################################################################
#                                    File Input Panel Component - Placeholder
#########################################################################################################################


def file_input_panel():
    """
    Placeholder panel for STEM image visualization
    Will be implemented in future versions with automatic generation
    """
    return html.Div(
        [
            html.Div(
                [
                    html.I(className="fas fa-microscope", style={
                        "fontSize": "64px",
                        "color": "#666",
                        "marginBottom": "20px"
                    }),
                    html.H3("STEM Image Visualization", style={
                        "color": "#333",
                        "marginBottom": "15px"
                    }),
                    html.P(
                        "You will be able to visualize STEM images here in future versions.",
                        style={
                            "color": "#666",
                            "fontSize": "16px",
                            "textAlign": "center",
                            "maxWidth": "600px"
                        }
                    ),
                    html.P(
                        "The system will automatically generate and display STEM images after XYZ/Parameter file generation.",
                        style={
                            "color": "#999",
                            "fontSize": "14px",
                            "textAlign": "center",
                            "maxWidth": "600px",
                            "marginTop": "10px"
                        }
                    )
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "minHeight": "400px",
                    "padding": "40px"
                }
            )
        ],
        id="file-input-panel",
        className="material-panel"
    )
