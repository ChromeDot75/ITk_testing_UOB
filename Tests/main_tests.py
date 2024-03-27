import os
import json
import re
import uproot
import pandas as pd
import plotly.express as px
import plotly.io as pio
import struct 

def root_files(scan_type_string, name_of_test):
    runs_directory = "N:\Dash\Runs"
    root_dict = {}
    
    for run_folder in os.listdir(runs_directory):
        run_folder_path = os.path.join(runs_directory, run_folder)
        if os.path.isdir(run_folder_path):
            data_folder = os.path.join(run_folder_path, "data")
            if os.path.isdir(data_folder):
                json_files = [f for f in os.listdir(data_folder) if f.endswith(".json")]
                if json_files: 
                    root_dict[run_folder] = []  # Initialize an empty list to store root files
                    for json_file in json_files:
                        with open(os.path.join(data_folder, json_file), 'r') as f:
                            json_data = json.load(f)
                            if "scan_points" in json_data and "scan_type_string" in json_data["scan_points"]:
                                if json_data["scan_points"]["scan_type_string"] == scan_type_string:
                                    index = os.path.splitext(json_file)[0].split("_")[2:]
                                    index = "_".join(index)
                                    strobe_delay_root = f"strun{index}.root"
                                    root_dict[run_folder].append(strobe_delay_root)  # Append root file to the list
                else: 
                    root_files = [f for f in os.listdir(run_folder_path) if f.endswith("_3.root")]
                    if root_files:
                        root_dict[run_folder] = root_files 
                        # Store root files as a list
    return root_dict

strobe_delay_roots = root_files("STROBE DELAY", "Strobe Delay Test")
strobe_delay_roots.update({"Run_697": ["strun697_3.root"]})
#print(strobe_delay_roots)
pts_roots = root_files("TRIMDAC", "Pedestal Trim Scan" )
pts_roots.update({"Run_697": ["strun697_2.root"]})
#print(pts_roots)
ts_roots = root_files("THRESHOLD (DAC)", "Threshold Scan")
w5_697_ts = {
    "Run_697": [f"strun697_{i}.root" for i in range(4,18)]
}

ts_roots.update(w5_697_ts)

items_to_delete = ['strun14_1.root', 'strun14_2.root']
for keyword in ts_roots:
    for item in items_to_delete:
        if item in ts_roots[keyword]:
            ts_roots[keyword].remove(item)

print(ts_roots['Run_14'])

#dict_length(ts_roots, "Threshold Scans")


def making_heatmaps(roots, dir, name_of_test, folder_location):
    heat_maps_dict = {}
    meta = {}

    output_dir = os.path.join(dir, folder_location)  
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist
    cycle_count=""

    print(roots.keys(),roots.items())
    for run_number, file_names in roots.items():

        heat_maps_dict[run_number] = []  # Initialize list to store heatmaps for each run
        for file_name in file_names:
            file_path = os.path.join(dir, run_number, "data", file_name)
            print(file_path)

            try:
                count_module=0
                fh = uproot.open(file_path)
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
                                                f'Stream {stream}, Module {module}, Run {run_number}, File: {file_name}')

                                fig.update_layout(coloraxis_colorbar=dict(title="Counts"))

                                heat_maps_dict[run_number+"_"+module+"_"+stream].append((fig, file_name)) 
                                count_module+=1 # Append each heatmap to the list
                                #create another dictionary that will store module and stream number, run, 
                                print(f"Created heatmap for Stream {stream}, Module {module}")
                            else:
                                print(f"Ignoring empty heatmap for Stream {stream}, Module {module - 1}")

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")


dir = "N:\\Dash\\Runs"
#sd_html, ts_html, pts_html, = "Strobe_delay_html", "Threshold_Scan_html", "Pedestal_Trim_Scan_html"

# sd_heatmaps = making_heatmaps(strobe_delay_roots, dir, "Strobe Delay")

#print(type(sd_heatmaps))

#ts_heatmaps = making_heatmaps(ts_roots, dir, "Threshold Scan", ts_html)

#pts_heatmaps = making_heatmaps(pts_roots, dir, "Pedestal Trim Scan", pts_html )

def get_cycles(run_name="Run_14"):
    run_files = {}

    for run in strobe_delay_roots.keys():
        run_dict = {}
        run_dict['Strobe Delay'] = strobe_delay_roots.get(run, [])
        run_dict['Pedestal Trim'] = pts_roots.get(run, [])
        run_dict['Threshold Scan'] = ts_roots.get(run, [])
        run_files[f'{run}'] = run_dict
        
    run_14_files = run_files.get(run_name, {})
    run_7_files = run_files.get('Run_7', {})
    run_files_all = {}
    for run, run_data in run_files.items():
        run_files_all[f'run_{run}_files'] = run_data

    run_14_cycles = {}

    # Assuming run_14_files is already defined as described in your code
    strobe_delay_list = run_14_files.get('Strobe Delay', [])
    num_cycles = len(strobe_delay_list)
    max_length = max(len(run_14_files.get('Pedestal Trim', [])), len(run_14_files.get('Threshold Scan', [])))

    for i in range(num_cycles):
        cycle_num = i + 1
        cycle_dict = {'Strobe Delay': strobe_delay_list[i]}

        if i < len(run_14_files.get('Pedestal Trim', [])):
            cycle_dict['Pedestal Trim'] = run_14_files['Pedestal Trim'][i]

        if i * 14 < len(run_14_files.get('Threshold Scan', [])):
            cycle_dict['Threshold Scan'] = run_14_files['Threshold Scan'][i*14:i*14+14]

        run_14_cycles[f'Cycle_{cycle_num}'] = cycle_dict
    return run_14_cycles

