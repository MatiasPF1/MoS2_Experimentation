''''                                                Imports Of UI Components                                                          '''
##########################################################################################################################
# Essential/Base Imports 
##########################################################################################################################
from dash import Dash, html, Input, Output, State, dcc
import dash_bootstrap_components as dbc
import dash

##########################################################################################################################
# Imports for XYZ/Params Generation page 
##########################################################################################################################
#First Tab Components
from UIComponents.Navbar import navbar
from UIComponents.Sidebar import sidebar
from UIComponents.tabs import left_tabs
from UIComponents.MaterialProperties import material_properties
from UIComponents.MaterialProperties2 import metal_site_defects
from UIComponents.MaterialProperties3 import chalcogen_site_defects
from UIComponents.SettingsGeneration import generation_settings
#Second Tab Components 
from UIComponents.BasicMicroscopeSettings import Microscope_Settings
from UIComponents.aberrationCoeficcients import Abberation_Coeficients
from UIComponents.ADF_Settings import ADF_Settings
from UIComponents.GaussianParameters import Gaussian_Parameters
# Callback For Display Vallues Collumn 
from UIComponents.DisplayValues import register_display_values_callback
# Import Generation module to update variables
from XYZ_Params_Generation import Generation

##########################################################################################################################
# Imports for STEM-Generation page 
##########################################################################################################################
import importlib
FileInputPanel = importlib.import_module("UIComponents-2.FileInputPanel")
file_input_panel = FileInputPanel.file_input_panel
FileInputCallbacks = importlib.import_module("UIComponents-2.FileInputCallbacks")
register_file_upload_callbacks = FileInputCallbacks.register_file_upload_callbacks



''''                                                Main UI Work                                                            '''
##########################################################################################################################
#                                          0- ALL Modules/Options 
##########################################################################################################################


"""Content for XYZ/Parameter File Generation page"""
def xyz_generation_page():
    return html.Div(
        [
            # Left side - Tabs and parameter panels
            html.Div(
                [
                    left_tabs(),

                    #Material Section Panels 
                    material_properties(),
                    metal_site_defects(),
                    chalcogen_site_defects(),

                    #Microscope Section Panels
                    Microscope_Settings(),
                    Abberation_Coeficients(),
                    ADF_Settings(),
                    Gaussian_Parameters(),
                ],
                className="tab-with-panel"
            ),
            # Right side - Generation settings and config
            generation_settings()
        ],
        className="main-content"
    )

"""Content for Pre-Processing page"""
def pre_processing_page():
    return html.Div(
        [],
        className="main-content"
    )

"""Content for STEM-Generation page"""
def stem_generation_page():
    return html.Div(
        [
            html.Div(
                [
                    file_input_panel()
                ],
                className="tab-with-panel"
            )
        ],
        className="main-content"
    )

"""Content for ResUnet page"""
def resunet_page():
    return html.Div(
        [],
        className="main-content"
    )


##########################################################################################################################
#                                          1- Main Layout
##########################################################################################################################

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"], suppress_callback_exceptions=True)
app.layout = html.Div([
    dcc.Store(id='current-page', data='xyz-generation'),     # Store for current page
    navbar,
    html.Div(
        [
            sidebar, # Sidebar on the left
            html.Div(id='page-content', children=xyz_generation_page()) # Main content area 

        ],
        className="section-container"
    )
])



##########################################################################################################################
#                             2- Main Section Interactivity(1st) -- Sidebar Page Selection
##########################################################################################################################
# Sidebar Navigation Callback
@app.callback(
    Output("page-content", "children"),
    Output("nav-xyz-generation", "className"),
    Output("nav-pre-processing", "className"),
    Output("nav-stem-generation", "className"),
    Output("nav-resunet", "className"),
    
    Input("nav-xyz-generation", "n_clicks"),
    Input("nav-pre-processing", "n_clicks"),
    Input("nav-stem-generation", "n_clicks"),
    Input("nav-resunet", "n_clicks"),
    prevent_initial_call=True
)
def navigate_pages(xyz_clicks, pre_clicks, stem_clicks, resunet_clicks):
    ctx = dash.callback_context.triggered_id
    # Base classes for sidebar items
    active_class = "sidebar-item active-sidebar-item"
    inactive_class = "sidebar-item"
    if ctx == "nav-xyz-generation":
        return (
            xyz_generation_page(),
            active_class, inactive_class, inactive_class, inactive_class
        )
    elif ctx == "nav-pre-processing":
        return (
            pre_processing_page(),
            inactive_class, active_class, inactive_class, inactive_class
        )
    elif ctx == "nav-stem-generation":
        return (
            stem_generation_page(),
            inactive_class, inactive_class, active_class, inactive_class
        )
    elif ctx == "nav-resunet":
        return (
            resunet_page(),
            inactive_class, inactive_class, inactive_class, active_class
        )
    # Default - XYZ Generation
    return (
        xyz_generation_page(),
        active_class, inactive_class, inactive_class, inactive_class
    )

##########################################################################################################################
#                        2- Main Section Interactivity(2nd) -- XYZ Page Interactivity(default): toggle_buttons
##########################################################################################################################


# On/Off Button Functionality
@app.callback(
    #Button Outputs 
    Output("btn-material", "className"),
    Output("btn-microscope", "className"),

    #First Tab Outputs
    Output("material-panel", "style"),
    Output("metal-defects-panel", "style"),
    Output("metal-Chalcogen-panel", "style"),

    #Second Tab Outputs
    Output("microscope-panel", "style"),
    Output("aberration-panel", "style"),
    Output("ADF_Panel", "style"),
    Output("Gausian_Panel","style"),

    #Click Inputs by User
    Input("btn-material", "n_clicks"),
    Input("btn-microscope", "n_clicks"),
)
def toggle_buttons(material_clicks, microscope_clicks):
    # Styles for show/hide
    visible = {"display": "block"} # Show
    hidden = {"display": "none"} #Hide

    # 1-Default State(param-btn By Default Active)
    if not material_clicks and not microscope_clicks:
        return (
            "param-btn active-param-btn",    # Material active
            "param-btn",                     # Microscope inactive
            visible,                         # Material panel Visible
            visible,                         # Metal defects panel Visible
            visible,                         # Chalcogen defects panel Visible
            hidden,                          # Microscope panel Hidden
            hidden,                          # Aberration panel Hidden
            hidden,                          # ADF panel Hidden
            hidden                           # Gaussian Panel Hidden
        )

    # 2- User Selection of Button

    # Which button was clicked?
    ctx = dash.callback_context.triggered_id

    # If Material Button Clicked
    if ctx == "btn-material":
        return (
            "param-btn active-param-btn",
            "param-btn",
            visible,  # material
            visible,  # metal defects
            visible,  # chalcogen defects
            hidden,   # microscope is hidden
            hidden,   # aberration is hidden
            hidden,   # ADF is hidden 
            hidden    # gaussian is Hidden 
        )

    # If Microscope Button Clicked
    elif ctx == "btn-microscope":
        return (
            "param-btn",
            "param-btn active-param-btn",
            hidden,   # material is hidden
            hidden,   # metal defects is hidden
            hidden,   # chalcogen defects is hidden
            visible,  # microscope
            visible,  # aberration
            visible,  # ADF
            visible   # Gaussian
        )

##########################################################################################################################
#                               2-  Main Section Interactivity(3rd) -- Send inputs to the Generation Module
##########################################################################################################################



@app.callback(
    Output('generate-btn', 'n_clicks'),
    Input('generate-btn', 'n_clicks'),
    State('batch-size-dropdown', 'value'),
    
    # Material Properties States
    State('mat-name', 'value'),
    State('pixel-size', 'value'),
    State('metal-atom', 'value'),
    State('lattice-const', 'value'),
    State('img-size', 'value'),
    State('chal-atom', 'value'),
    
    # Metal Site Defects States
    State('sub-atom-metal', 'value'),
    State('metal-sub-conc', 'value'),
    State('metal-vac-conc', 'value'),
    
    # Chalcogen Site Defects States
    State('sub-atom-chal', 'value'),
    State('chal-sub-conc', 'value'),
    State('vac-one-conc', 'value'),
    State('vac-two-conc', 'value'),
    State('sub-two-conc', 'value'),
    State('sub-one-conc', 'value'),
    
    # Microscope Settings States
    State('voltage', 'value'),
    State('aperture', 'value'),
    State('defocus', 'value'),
    State('dwell-time', 'value'),
    
    # Aberration Coefficients States
    State('cs3-mean', 'value'),
    State('cs3-std', 'value'),
    State('cs5-mean', 'value'),
    State('cs5-std', 'value'),
    
    # ADF Settings States
    State('adf-angle-min', 'value'),
    State('adf-angle-max', 'value'),
    
    # Gaussian Parameters States
    State('src-size-mean', 'value'),
    State('defoc-spread-mean', 'value'),
    State('probe-cur-mean', 'value'),
    State('src-size-std', 'value'),
    State('defoc-spread-std', 'value'),
    State('probe-cur-std', 'value'),
    
    prevent_initial_call=True
)
def store_parameters_RunGeneration(n_clicks, batch_size, mat_name, pixel_size, metal_atom, 
                     lattice_const, img_size, chal_atom, sub_atom_metal,
                     metal_sub_conc, metal_vac_conc, sub_atom_chal,
                     chal_sub_conc, vac_one_conc, vac_two_conc,
                     sub_two_conc, sub_one_conc,
                     voltage, aperture, defocus, dwell_time,
                     cs3_mean, cs3_std, cs5_mean, cs5_std,
                     adf_angle_min, adf_angle_max,
                     src_size_mean, defoc_spread_mean, probe_cur_mean,
                     src_size_std, defoc_spread_std, probe_cur_std):
    
    # If button not clicked, do nothing
    if not n_clicks:
        return dash.no_update
    
    # Update Generation.py variables directly
    Generation.file_name = mat_name
    Generation.pixel_size = float(pixel_size)
    Generation.image_size = float(img_size)
    Generation.metal_atom = int(metal_atom)
    Generation.chalcogen_atom = int(chal_atom)
    Generation.lattice_constant_a = float(lattice_const)
    Generation.doped_metal_atom = int(sub_atom_metal) 
    Generation.metal_atom_concentration = float(metal_sub_conc) 
    Generation.metal_atom_vacancy_concentration = float(metal_vac_conc) 
    Generation.doped_chalcogen_atom = int(sub_atom_chal) 
    Generation.chalcogen_atom_concentration_two_subsititution = float(sub_two_conc) 
    Generation.chalcogen_atom_concentration_one_subsititution = float(sub_one_conc) 
    Generation.chalcogen_atom_concentration_one_vacancy = float(vac_one_conc) 
    Generation.chalcogen_atom_concentration_two_vacancy = float(vac_two_conc) 
    
    Generation.voltage = float(voltage)
    Generation.Cs3_param_mean = float(cs3_mean)
    Generation.Cs3_param_std = float(cs3_std)
    Generation.Cs5_param_mean = float(cs5_mean)
    Generation.Cs5_param_std = float(cs5_std)
    Generation.df = float(defocus)
    Generation.aperture = float(aperture)
    Generation.ADF_angle_min = float(adf_angle_min)
    Generation.ADF_angle_max = float(adf_angle_max)
    Generation.Source_size_param_mean = float(src_size_mean)
    Generation.Source_size_param_std = float(src_size_std)
    Generation.defocus_spread_param_mean = float(defoc_spread_mean)
    Generation.defocus_spread_param_std = float(defoc_spread_std)
    Generation.probe_current_param_mean = float(probe_cur_mean)
    Generation.probe_current_param_std = float(probe_cur_std)
    Generation.dwell_time = float(dwell_time)
    # Run the generation process with batch_size
    Generation.run_generation(int(batch_size))
    return n_clicks


# Register display values callback
register_display_values_callback(app)

# Register file upload callbacks for STEM Generation page
register_file_upload_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)