import dash 
from dash import html,dcc,callback,Input,Output,State
import dash_mantine_components as dmc
import glob
from Tests.t_test_2 import get_t_value
from dash.exceptions import PreventUpdate
dash.register_page(__name__, path="/Page-2")

raw_names=glob.glob("N:\\Dash\\Runs\\Run_*")
run_names=[i.split("N:\\Dash\\Runs\\")[1] for i in raw_names]

layout=html.Div(
    [dmc.Container([
        dmc.Grid(
        [
            dmc.Col(
                dmc.Select(
                            "Run Selection",
                            id="run_select_pvalue",
                            label="Select Run",
                            data=run_names,
                            value=run_names[0],
                        ),
                        span=4
            ),
            dmc.Col(
                dmc.Select(
                    "Select a strip",
                    id="strip_selector",
                     label="Select value",
                    data=['x','y'],
                    value='x'
                    
                ),
                        span=4

            ),
            dmc.Col(
                dmc.Button(
                    "Submit",
                            id="submit_btn_pvalue",
                            color="primary",
                            variant="filled",
                            n_clicks=0,
                            style={
                                "margin":"21px"
                            }
                ),
                span=3
            ),
        ]
    )
    ]),
    dmc.LoadingOverlay(
        dcc.Graph(id="p_value")
    )
]
)     

@callback(Output('p_value','figure'),Input('submit_btn_pvalue','n_clicks'),State('run_select_pvalue',"value"),State("strip_selector","value"))
def update_p_value_graph(n,run_name,strip):
    if n:
        fig=get_t_value(run_name,strip)
        return fig
    raise PreventUpdate
     
     
     
     
     
     
     
     
     
     
     
     
     
     
"""  
     
stats=[

        {
            "run_name":"run_23",
            "isexcepted":True,
            "tscore":0.1242
        },
 
        {
            "run_name":"run_24",
            "isexcepted":False,
            "tscore":0.1242
        },

        {
            "run_name":"run_25",
            "isexcepted":True,
            "tscore":0.1242
        },
]

status_bar=[]

for i in stats:
    status_bar.append(
        dmc.Alert(
    i.get('tscore'),
    title=i.get("run_name"),
    style={
        "margin":"10px"
    },
    color="green" if i.get('isexcepted') else "red"   #CSS styling done  here
)
    )

layout = html.Div(
    id="content",
    children=status_bar
)#Pass html.div here. 




# Create noise and gain dictionaries
"""