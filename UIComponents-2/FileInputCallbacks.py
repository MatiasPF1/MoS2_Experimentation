from dash import Input, Output, State

# Store for uploaded file contents
xyz_file_content = None
params_file_content = None
batch_file_content = None



def get_xyz_content():
    """Get the stored XYZ file content"""
    return xyz_file_content


def get_params_content():
    """Get the stored params file content"""
    return params_file_content

def get_batch_content():
    """Get the stored batch file content"""
    return batch_file_content


def register_file_upload_callbacks(app):
    @app.callback(
        Output("xyz-file-name", "children"),
        Input("xyz-file-upload", "contents"),
        State("xyz-file-upload", "filename"),
        prevent_initial_call=True
    )
    def store_xyz_file(contents, filename):
        global xyz_file_content
        if contents is not None:
            xyz_file_content = contents
            return f"{filename}"
        return ""

    @app.callback(
        Output("params-file-name", "children"),
        Input("params-file-upload", "contents"),
        State("params-file-upload", "filename"),
        prevent_initial_call=True
    )
    def store_params_file(contents, filename):
        global params_file_content
        if contents is not None:
            params_file_content = contents
            return f"{filename}"
        return ""

    @app.callback(
        Output("batch-file-name", "children"),
        Input("batch-file-upload", "contents"),
        State("batch-file-upload", "filename"),
        prevent_initial_call=True
    )
    def store_batch_file(contents, filename):
        global batch_file_content
        if contents is not None:
            batch_file_content = contents
            return f"{filename}"
        return ""