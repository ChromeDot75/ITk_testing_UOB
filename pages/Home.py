import dash
from dash import html,Input,Output,callback,dcc,State,no_update
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
import glob
import pickle
from Tests.IV_2 import plot_IV_dict

from generate_graph import get_cycles,get_modules,get_dict_of_heatmaps
dash.register_page(__name__,path='/')

#use pickle.dump whenever a new run is added, and then can be opened with pickle.load

def layout()->None:
    raw_names=glob.glob("N:\\Dash\\Runs\\Run_*")
    run_names=[i.split("N:\\Dash\\Runs\\")[1] for i in raw_names]
    return html.Div(
        [
            dmc.Container(
                [
                    dmc.Grid(
                [
                    dmc.Col(
                        dmc.Select(
                            "Run Selection",
                            id="run_select",
                            label="Select Run",
                            data=run_names,
                            value=run_names[0],
                        ),
                                 span=3
                    ),

                    dmc.Col(
                        dmc.Select(
                            "Cycle Selection",
                                            id="cycle_select",
                            label="Select Cycle",
                            disabled=True,
                            
                        ),
                                 span=2
                    ),
                     dmc.Col(
                            dmc.Select(
                            "Module Selection",
                                            id="module_select",
                            label="Select Module",
                       disabled=True,
                        ),
                                 span=2
                    ),
                     dmc.Col(
                        dmc.Select(
                            "Stream Selection",
                            id="stream_select",
                            label="Select Stream",
                            data=[
                                "0","1"
                            ],
                            value="0"
                        ),
                                 span=2
                    ),
                    dmc.Col(
                        [
                        dmc.Button(             #pass styling to submit. A key called a style. it is a dictionairy 
                            "Submit",
                            id="submit_btn",
                            color="primary",
                            variant="filled",
                            n_clicks=0,
                            style={
                                "margin":"21px"
                            }
                            
                        )],
                       
                                 span=3
                    )
                ],
                gutter="xl"
            )
                ]
            ),
            dmc.Grid(
                [
                    dmc.Col(
                        dmc.LoadingOverlay(dcc.Graph(id='strobe_delay')),  #add dmc loading overlay to IV, gain and noise.
                        span=6
                    ),
                    dmc.Col(
                        dmc.LoadingOverlay(dcc.Graph(id='padestal_trim')),
                        span=6
                    ),
                    
                ],
                gutter="xl"
            ),
            dmc.Grid(
                [
                    dmc.Col(
                        dmc.LoadingOverlay(dcc.Graph(id='threshold_scan')),
                        span=6
                    ),
                    dmc.Col(
                        dmc.LoadingOverlay(dcc.Graph(id='iv_graph')),
                        span=6
                    ),
                    # dmc.Col(
                    #     dmc.LoadingOverlay(dcc.Graph(id='gain_graph')),
                    #     span=4
                    # ),
                    # dmc.Col(
                    #     dmc.LoadingOverlay(dcc.Graph(id='noise_graph')),
                    #     span=4
                    # )
                ],
                gutter="xl"
            ),
        ],
        style={
            "maxWidth":"98vw"
        }
    )


@callback([Output("cycle_select","data"),Output("cycle_select","value"),Output("cycle_select","disabled")],Input("run_select","value"))
def update_cycles(value):
    if value:
        strobe_delay_roots=pickle.load(open("data/strobe_delay_roots.pkl","rb"))
        pts_roots=pickle.load(open("data/pts_roots.pkl","rb"))
        ts_roots=pickle.load(open("data/ts_roots.pkl","rb"))
        
        Cycles=get_cycles(strobe_delay_roots,pts_roots,ts_roots,run_name=value)
        Cycles_keys=Cycles.keys()
        return list(Cycles_keys),list(Cycles_keys)[0],False
    else:
        raise PreventUpdate
    
@callback([Output("module_select","data"),Output("module_select","value"),Output("module_select","disabled")],[Input("cycle_select","value"),Input("run_select","value")])
def update_module(cycle,run_name):
    if cycle and run_name:
        modules=get_modules(cycle,run_name) # Modules
        return modules,modules[0],False
    else:
        raise PreventUpdate

@callback(Output("strobe_delay","figure"),
          Output("padestal_trim","figure"),
          Output("threshold_scan","figure"),
          Output("iv_graph", "figure"),   # return this for noise, gain. pass output as sequence
          [State("run_select","value"),
           State("cycle_select","value"),
           State("module_select","value"),
           State("stream_select","value")],
           Input("submit_btn","n_clicks"))
#IV scan do same callback with inputs it requires. 
def update_heatmaps(run_name,cycle,module,stream,n):
    if n:
        if run_name and cycle and module and stream:
            dict_strobe_delay,heat_maps_dict_pts,heat_maps_dict_ts=get_dict_of_heatmaps(cycle,run_name) #instead of loading everytime, use numpy (pickle formatting stores)
            temp_dict_strobe_delay=dict_strobe_delay[f"{run_name}_{module}_{stream}_{cycle.split('_')[1]}"]
            temp_dict_strobe_delay.update_layout(title="XYZ") # saving the plotly graph in this variable.
            if heat_maps_dict_ts:
                return temp_dict_strobe_delay,heat_maps_dict_pts[f"{run_name}_{module}_{stream}_{cycle.split('_')[1]}"],heat_maps_dict_ts[f"{run_name}_{module}_{stream}_{cycle.split('_')[1]}"],plot_IV_dict[F'{run_name}']  # return iv, noise, gain in right order.
            # return temp_dict_strobe_delay,heat_maps_dict_pts[f"{run_name}_{module}_{stream}_{cycle.split('_')[1]}"],no_update,no_update  # return iv, noise, gain in right order.

    else:
        raise PreventUpdate
    
# https://www.dash-mantine-components.com/ SUBMIT Button. 
# play with Dash documentation to mess around with  styling. 
#State. To refresh graph. 
#add line 90 loadding for other graphs. 
#Give padding to submit button, and align it with selectors. 
#

# pass run_number for iv_graph 
#pass gain, noise pass cycle number. 
