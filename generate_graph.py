import os
import json
import re
import uproot
import pandas as pd
import plotly.express as px
import plotly.io as pio
import struct 
import numpy as np

runs_directory = "N:\Dash\Runs"

# ts_roots.update(w5_ts)
import pickle
if not os.path.exists("ts_roots.pkl"):
    from generate_roots import generating_root_as_pickles
    generating_root_as_pickles()
    
def get_cycles(strobe_delay_roots,pts_roots,ts_roots,run_name="Run_14"):
    """
    This function takes strobe_delay_roots
    pts roots and ts roots to generate the cycles.
    """
    run_files = {}

    for run in strobe_delay_roots.keys():
        run_dict = {}
        run_dict['Strobe Delay'] = strobe_delay_roots.get(run, [])
        run_dict['Pedestal Trim'] = pts_roots.get(run, [])
        run_dict['Threshold Scan'] = ts_roots.get(run, [])
        run_files[f'{run}'] = run_dict
        
    run_files = run_files.get(run_name, {})
    run_files_all = {}
    for run, run_data in run_files.items():
        run_files_all[f'run_{run}_files'] = run_data

    run_cycles = {}

    # Assuming run_14_files is already defined as described in your code
    strobe_delay_list = run_files.get('Strobe Delay', [])
    num_cycles = len(strobe_delay_list)

    # Unused Variable (Future Task)
    max_length = max(len(run_files.get('Pedestal Trim', [])), len(run_files.get('Threshold Scan', [])))
    # This loop is generating the cycles with respective files.
    for i in range(num_cycles):
        cycle_num = i + 1
        cycle_dict = {'Strobe Delay': strobe_delay_list[i]}

        if i < len(run_files.get('Pedestal Trim', [])):
            cycle_dict['Pedestal Trim'] = run_files['Pedestal Trim'][i]

        if i * 14 < len(run_files.get('Threshold Scan', [])):
            
            if len(run_files['Threshold Scan'][i*14:i*14+14])>3:
                cycle_dict['Threshold Scan'] = run_files['Threshold Scan'][i*14:i*14+14][3]
            else:
                cycle_dict['Threshold Scan'] = run_files['Threshold Scan'][i*14:i*14+14][1]
                 #missing _1 and _2. So this could be 
            # print(cycle_dict['Threshold Scan'])

        run_cycles[f'Cycle_{cycle_num}'] = cycle_dict

    return run_cycles


def generate_heatmaps(filename,cycle_number,run_name):
    heat_maps_dict={}
    try:
        pull_path=os.path.join(os.path.join(runs_directory,run_name),"data")
        fh = uproot.open(os.path.join(pull_path,filename))
        for stream in range(2):  # Streams numbers from 0 and 1
            for module in range(1, 7):    # Module numbers 1 and 11
                hist_name = f"h_scan{stream};{module}"
                if hist_name in fh:
                    hist = fh[hist_name]
                    data_transposed = hist.values().T
                    df = pd.DataFrame(data_transposed)

                    # Check if DataFrame is empty (all values are the same)
                    if not df.apply(lambda x: x.nunique()).eq(1).all():

                        fig = px.imshow(df, aspect='auto', labels=dict(x='Channel number', y='Counts'), title=
                                        f'Stream {stream}, Module {module}, Run {run_name}, File: {filename}')

                        fig.update_layout(coloraxis_colorbar=dict(title="Counts"))
                        # fig.show()
                        heat_maps_dict[f"{run_name}_{module}_{stream}_{cycle_number.split('_')[1]}"]=fig 
                        #create another dictionary that will store module and stream number, run, 
                        # print(f"Created heatmap for Stream {stream}, Module {module}")
                        
                    else:
                        # print(f"Ignoring empty heatmap for Stream {stream}, Module {module - 1}")
                        pass
        return heat_maps_dict
    except Exception as e:
        # print(e)
        pass

def get_dict_of_heatmaps(cycle_number,run_name="Run_14"):
    ts_roots=pickle.load(open("data/ts_roots.pkl","rb"))
    strobe_delay_roots=pickle.load(open("data/strobe_delay_roots.pkl","rb"))
    pts_roots=pickle.load(open("data/pts_roots.pkl","rb"))

    cycles=get_cycles(strobe_delay_roots,pts_roots,ts_roots,run_name)
    cycle=cycles[cycle_number]
    heat_maps_dict_strobe_delay=generate_heatmaps(cycle["Strobe Delay"],cycle_number,run_name)
    heat_maps_dict_pts=generate_heatmaps(cycle["Pedestal Trim"],cycle_number,run_name)

    heat_maps_dict_ts=generate_heatmaps(cycle['Threshold Scan'],cycle_number,run_name) if "Threshold Scan" in cycle else None

    return heat_maps_dict_strobe_delay,heat_maps_dict_pts,heat_maps_dict_ts


def get_modules(cycle_number,run_name):
    dict_strobe_delay,heat_maps_dict_pts,heat_maps_dict_ts=get_dict_of_heatmaps(cycle_number,run_name)
    modules=[i.split("_")[2] for i in dict_strobe_delay.keys()]
    return np.unique(modules)
