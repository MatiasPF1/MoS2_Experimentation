from dash import html
import dash_bootstrap_components as dbc


navbar = dbc.Navbar(
    dbc.NavbarBrand(
        "Computational 2D STEM-Images Generator", #Name of the Application
        className="navbar-title mx-auto"          #Center the Tittle
    ),
    className="navbar-custom shadow-sm py-3",     #Style of the Navbar
    color="light",                               
    dark=False
)