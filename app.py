from dash import Dash, Input,Output,dcc,html,page_container
import dash_bootstrap_components as dbc

external_style_sheets=[
    dbc.themes.BOOTSTRAP
]

app = Dash(__name__,external_stylesheets=external_style_sheets,use_pages=True)
image_src = "https://cdn.filestackcontent.com/gSyQy63eRaukn5pZbQWA"

app.layout=html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink("Home",href="/")
            ),
            dbc.NavItem(
                dbc.NavLink("RC Graphs",href="/gain-noise-graphs"),
                ),
            dbc.NavItem(
                dbc.NavLink("T-Test",href="/Page-2")
            ),
        ],
        brand=html.Img(src=image_src,
                       className="logo",
                    #    style={
                    #        "width":"45px", #import logo, see what changes to height and width keywords. #write a file called CSS and reference
                        
                    #    }
                       ), # 
        dark=True,
        color="primary"
    ),
    page_container
])

if __name__=="__main__":

    app.run_server(debug=True)