import pickle
import os
import json
runs_directory = "N:\Dash\Runs"
def root_files(scan_type_string, name_of_test):

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

def generating_root_as_pickles():

    strobe_delay_roots = root_files("STROBE DELAY", "Strobe Delay Test")
    strobe_delay_roots.update({"Run_697": ["strun697_3.root"]}) # NEED TO GET RID of W5_ part of this run. 
    #print(strobe_delay_roots)
    pts_roots = root_files("TRIMDAC", "Pedestal Trim Scan" )
    pts_roots.update({"Run_697": ["strun697_2.root"]})
    #print(pts_roots)
    ts_roots = root_files("THRESHOLD (DAC)", "Threshold Scan")   #these are being calculating everytime. Can save in pickle files (pickle is a library)
    w5_ts = {
        "Run_697": [f"strun697_{i}.root" for i in range(4,18)]
    }
    ts_roots.update(w5_ts)
    keys=list(ts_roots.keys())
    for key in keys:
        unsorted_list=[x for x in ts_roots[key] if not x.endswith('1.root') and not x.endswith('2.root')]
        sort_threshold=sorted(unsorted_list,key= lambda x: int(x.split('.')[0].split('_')[1]))
        # print(sort_threshold)
        ts_roots.update(
            {key:sort_threshold}
        )
    
    # print(ts_roots)
    pickle.dump(ts_roots,open("data/ts_roots.pkl","wb"))
    pickle.dump(pts_roots,open("data/pts_roots.pkl","wb"))
    pickle.dump(strobe_delay_roots,open("data/strobe_delay_roots.pkl","wb"))

generating_root_as_pickles()

#delete all the strobe_delay roots