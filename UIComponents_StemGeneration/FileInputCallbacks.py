"""
File Input Callbacks Module
Handles file upload callbacks and storage for STEM generation files (XYZ, Params, Batch)
"""

from dash import Input, Output, State, html
from _2_computem_stem_generation import stem_executor


########################################################################################################################
#                                    Main Functionality: File input and Storage 
#########################################################################################################################


# Global storage for uploaded file contents

xyz_file_content = None
params_file_content = None
batch_file_content = None


# Getter functions to access stored file contents from other modules
def get_xyz_content():
    """
    Get the stored XYZ file content
    
    """
    return xyz_file_content


def get_params_content():
    """
    Get the stored params file content
    
    """
    return params_file_content


def get_batch_content():
    """
    Get the stored batch file content
    
    """
    return batch_file_content


"""
    Register all file upload callbacks with the Dash app
    
    Creates three callbacks that:
    1. Listen for file uploads from dcc.Upload components
    2. Store the file contents in global variables
    3. Display the filename to confirm upload
    
    Args:
        app: The Dash application instance
    """
def register_file_upload_callbacks(app):
    #1-Callback for XYZ file upload
    @app.callback(
        Output("xyz-file-name", "children"),  # Updates the filename display
        Input("xyz-file-upload", "contents"),  # Triggered when file is uploaded
        State("xyz-file-upload", "filename"),  # Gets the filename
        prevent_initial_call=True  # Don't run on page load
    )
    def store_xyz_file(contents, filename):
        """
        Store uploaded XYZ file content and display filename
        
        """
        global xyz_file_content
        if contents is not None:
            # Store content in global variable
            xyz_file_content = contents
            # Return filename to display in UI
            return f"✓ {filename}"
        return ""



    #2-Callback for Params file upload
    @app.callback(
        Output("params-file-name", "children"),  # Updates the filename display
        Input("params-file-upload", "contents"),  # Triggered when file is uploaded
        State("params-file-upload", "filename"),  # Gets the filename
        prevent_initial_call=True  # Don't run on page load
    )
    def store_params_file(contents, filename):
        """
        Store uploaded params file content and display filename
        
        """
        global params_file_content
        if contents is not None:
            # Store the content in global variable
            params_file_content = contents
            # Return filename to display in UI
            return f"{filename}"
        return ""


    #3-Callback for Batch file upload
    @app.callback(
        Output("batch-file-name", "children"),  # Updates the filename display
        Input("batch-file-upload", "contents"),  # Triggered when file is uploaded
        State("batch-file-upload", "filename"),  # Gets the filename
        prevent_initial_call=True  # Don't run on page load
    )
    def store_batch_file(contents, filename):
        """
        Store uploaded batch file content and display filename
        
        """
        global batch_file_content
        if contents is not None:
            # Store the content in global variable
            batch_file_content = contents
            return f"{filename}"            # Return filename to display in UI
        return ""


    #4-Callback for Generate STEM Images button
    @app.callback(
        Output("generate-stem-btn", "children"),  # Updates button text to show status
        Input("generate-stem-btn", "n_clicks"),  # Triggered when button is clicked
        State("xyz-file-upload", "filename"),  # Gets XYZ filename
        State("params-file-upload", "filename"),  # Gets params filename
        prevent_initial_call=True  # Don't run on page load
    )
    def generate_stem_images(n_clicks, xyz_filename, params_filename):
        """
        Execute incostem.exe with uploaded XYZ and params files
        """
        global xyz_file_content, params_file_content
        
        # Check if required files are uploaded
        if xyz_file_content is None or params_file_content is None:
            return [
                html.I(className="fas fa-exclamation-triangle", style={"marginRight": "8px"}),
                "Please upload both XYZ and Params files first!"
            ]
        # Execute incostem.exe
        result = stem_executor.execute_incostem(
            xyz_file_content,
            params_file_content,
            xyz_filename,
            params_filename
        )
        
        # Update button text based on result
        if result["success"]:
            return [
                html.I(className="fas fa-check-circle", style={"marginRight": "8px"}),
                "Generation Complete!"
            ]
        else:
            return [
                html.I(className="fas fa-times-circle", style={"marginRight": "8px"}),
                f"Error: {result['message']}"
            ]