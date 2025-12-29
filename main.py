''''                                                Imports Of UI Components                                                          '''


##########################################################################################################################
# Essential/Base Imports 
##########################################################################################################################
from dash import Dash, html, Input, Output, State, dcc
import dash_bootstrap_components as dbc
import dash

##########################################################################################################################
#1-Imports for XYZ/Params Generation page and All the Main UI Components
##########################################################################################################################
#First Tab Components
from UIComponents_MainUI.Navbar import navbar
from UIComponents_MainUI.Sidebar import sidebar
from UIComponents_MainUI.tabs import left_tabs
from UIComponents_MainUI.MaterialProperties import material_properties
from UIComponents_MainUI.MaterialProperties2 import metal_site_defects
from UIComponents_MainUI.MaterialProperties3 import chalcogen_site_defects
from UIComponents_MainUI.SettingsGeneration import generation_settings
#Second Tab Components 
from UIComponents_MainUI.BasicMicroscopeSettings import Microscope_Settings
from UIComponents_MainUI.aberrationCoeficcients import Abberation_Coeficients
from UIComponents_MainUI.ADF_Settings import ADF_Settings
from UIComponents_MainUI.GaussianParameters import Gaussian_Parameters
# Callback For Display Vallues Collumn 
from UIComponents_MainUI.DisplayValues import register_display_values_callback

##########################################################################################################################
#2-)Imports for STEM-Generation page 
##########################################################################################################################
from _1_xyz_params_generation import Generation
from UIComponents_StemGeneration.FileInputPanel import file_input_panel
from UIComponents_StemGeneration.FileInputCallbacks import register_file_upload_callbacks



''''                                                Main UI Work                                                            '''


##########################################################################################################################
#                                          0- ALL Modules/Options For The WebApp
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


"""Content for Pre-Processing page"""
def pre_processing_page():
    return html.Div(
        [],
        className="main-content"
    )


"""Content for ResUnet page"""
def resunet_page():
    return html.Div(
        [],
        className="main-content"
    )


##########################################################################################################################
#                                          1- Main Layout For the WebApp
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
    elif ctx == "nav-stem-generation":
        return (
            stem_generation_page(),
            inactive_class, inactive_class, active_class, inactive_class
        )
    elif ctx == "nav-pre-processing":
        return (
            pre_processing_page(),
            inactive_class, active_class, inactive_class, inactive_class
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

def safe_float(value, default=0.0):
    """Convert value to float, return default if None or empty"""
    if value is None or value == '':
        return default
    return float(value)

def safe_int(value, default=0):
    """Convert value to int, return default if None or empty"""
    if value is None or value == '':
        return default
    return int(value)

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
    
    # Helper function converts None/empty to default values
    # Generation.py variables with safe conversions
    Generation.file_name = mat_name if mat_name else 'MoS2'
    Generation.pixel_size = safe_float(pixel_size, 0.1) # Default pixel size 0.1 
    Generation.image_size = safe_float(img_size, 512) # Default image size 512
    Generation.metal_atom = safe_int(metal_atom, 42) # Default Mo
    Generation.chalcogen_atom = safe_int(chal_atom, 16) # Default S
    Generation.lattice_constant_a = safe_float(lattice_const, 3.16) # Default MoS2 lattice constant
    Generation.doped_metal_atom = safe_int(sub_atom_metal, 42) # Default Mo
    Generation.metal_atom_concentration = safe_float(metal_sub_conc)
    Generation.metal_atom_vacancy_concentration = safe_float(metal_vac_conc)
    Generation.doped_chalcogen_atom = safe_int(sub_atom_chal, 16)
    Generation.chalcogen_atom_concentration_two_subsititution = safe_float(sub_two_conc)
    Generation.chalcogen_atom_concentration_one_subsititution = safe_float(sub_one_conc)
    Generation.chalcogen_atom_concentration_one_vacancy = safe_float(vac_one_conc)
    Generation.chalcogen_atom_concentration_two_vacancy = safe_float(vac_two_conc)
    
    Generation.voltage = safe_float(voltage, 300) # Default 300kV
    Generation.Cs3_param_mean = safe_float(cs3_mean)
    Generation.Cs3_param_std = safe_float(cs3_std)
    Generation.Cs5_param_mean = safe_float(cs5_mean)
    Generation.Cs5_param_std = safe_float(cs5_std)
    Generation.df = safe_float(defocus)
    Generation.aperture = safe_float(aperture, 25) # Default 25 mrad
    Generation.ADF_angle_min = safe_float(adf_angle_min, 70)
    Generation.ADF_angle_max = safe_float(adf_angle_max, 200)
    Generation.Source_size_param_mean = safe_float(src_size_mean, 0.5) # Default 0.5
    Generation.Source_size_param_std = safe_float(src_size_std, 0.1) # Default 0.1
    Generation.defocus_spread_param_mean = safe_float(defoc_spread_mean, 10) # Default 10
    Generation.defocus_spread_param_std = safe_float(defoc_spread_std, 1) # Default 1
    Generation.probe_current_param_mean = safe_float(probe_cur_mean, 100) # Default 100
    Generation.probe_current_param_std = safe_float(probe_cur_std, 10) # Default 10
    Generation.dwell_time = safe_float(dwell_time, 1.0) # Default 1.0 
    
    # Run the generation process
    Generation.run_generation(int(batch_size))
    return n_clicks


# Register display values callback
register_display_values_callback(app)

# Register file upload callbacks for STEM Generation page
register_file_upload_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)