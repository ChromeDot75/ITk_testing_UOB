import dash 
from dash import html,dcc,callback,Input,Output,State
import dash_mantine_components as dmc
import glob
import pickle
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path="/gain-noise-graphs")

raw_names=glob.glob("N:\\Dash\\Runs\\Run_*")
run_names=[i.split("N:\\Dash\\Runs\\")[1] for i in raw_names]

vt50_graphs=pickle.load(open("data/vt50_graphs.pkl","rb"))
gain_graphs=pickle.load(open("data/gain_graphs.pkl","rb"))
noise_graphs=pickle.load(open("data/noise_graphs.pkl","rb"))



layout=html.Div(
    [dmc.Container([
        dmc.Grid(
        [
            dmc.Col(
                dmc.Select(
                            "Run Selection",
                            id="run_select_noise",
                            label="Select Run",
                            data=run_names,
                            value=run_names[0],
                        ),
                        span=4
            ),
            dmc.Col(
                dmc.Select(
                    "Select an Interval",
                    id="intervals_noise",
                     label="Select value",

                    
                ),
                        span=4

            ),
            dmc.Col(
                dmc.Button(
                    "Submit",
                            id="submit_btn_noise",
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

                     dmc.Container(
        [
        dmc.LoadingOverlay(
                dcc.Graph(

                                 id="vt50_graph"
                )
            ),

        dmc.LoadingOverlay(
                dcc.Graph(
                                id="noise_graph"
                )
            ),
      
        dmc.LoadingOverlay(
                dcc.Graph(

                                id="gain_graph"
                )
            ),
          
        ]
    )
            
   
    ],style={
        "width":"98svw"
                }
)

@callback(Output("intervals_noise","data"),Output("intervals_noise","value"),Input("run_select_noise","value"))
def update_intervals(run_name):
    if run_name:
        raw_graph_interval=list(noise_graphs.keys())
        # print(raw_graph_interval)
        graph_interval=[f"{x.split('_')[2]}_{x.split('_')[3]}" for x in raw_graph_interval if x.startswith(run_name)]
        intervals=sorted((set(graph_interval)),key=lambda x: int(x.split('_')[1]))
        # if run_name=='Run_'' or run_name==639:
        #     intervals=[interval for interval in intervals if interval.startswith('SN')]
        # else:
        intervals=[interval for interval in intervals if interval.startswith('3')]
        #write   
        return intervals,intervals[0]
    else:
        raise PreventUpdate
    
@callback([Output('vt50_graph',"figure"),Output('noise_graph','figure'), Output('gain_graph', "figure")],Input("submit_btn_noise","n_clicks"),State("run_select_noise","value"),State("intervals_noise","value"))
def update_graphs(nclicks,run_name,interval):
    if nclicks:
        vt50_graph=vt50_graphs[f"{run_name}_{interval}"]
        noise_graph=noise_graphs[f"{run_name}_{interval}"]
        gain_graph=gain_graphs[f"{run_name}_{interval}"]
    
        return vt50_graph, noise_graph, gain_graph
    raise PreventUpdate
#go through noise graphs, why is it generating the other values like 92_4. 
