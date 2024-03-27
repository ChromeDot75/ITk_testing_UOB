import os
import re
import json
import plotly.graph_objects as go
import plotly.io as pio

def get_IV_files(run_folder):
    IV_files_dict = {}
    results_folder = os.path.join(run_folder, 'results')
    if os.path.exists(results_folder) and os.path.isdir(results_folder):
        IV_files = [f for f in os.listdir(results_folder) if f.endswith('.json') and 'MODULE_IV' in f]
        IV_files_dict[os.path.basename(run_folder)] = IV_files
    return IV_files_dict

runs_directory = "N:\\DASH\\Runs"

IV_files_dict = {}

# Loop over folders inside the "Runs" directory
for folder in os.listdir(runs_directory):
    run_folder = os.path.join(runs_directory, folder)
    # Check if folder starts with "Run_" followed by a number and is a directory
    if re.match(r'^Run_\d+$', folder) and os.path.isdir(run_folder):
        # Get IV files for this run
        IV_files_dict.update(get_IV_files(run_folder))

class JsonData:

    def __init__(self, json_FP):
        with open(json_FP) as file:
            data = json.load(file)
            self.results = data.get('results', {}) #starts search when sees this keyword and braces
    

    def get_current(self):
        return self.results.get('CURRENT', [])    
    
    def get_voltage(self):
        return self.results.get('VOLTAGE', [])   
    
    
    
def extract_IV(json_FP):
    json_data = JsonData(json_FP)
    return  json_data.get_voltage(), json_data.get_current()

IV_data_dict = {}


iv_63_loc  = 'SN20USBHX2001092_UNKNOWN_20231009_63_18_MODULE_IV_AMAC.json'
iv_697_loc = 'SN20USBHX2001216_UNKNOWN_20231026_697_1_MODULE_IV_AMAC.json'
json_data = JsonData("N:\\DASH\\Runs\\Run_63\\results\\SN20USBHX2001092_UNKNOWN_20231009_63_18_MODULE_IV_AMAC.json")
json_data2 = JsonData("N:\\DASH\\Runs\\Run_697\\results\\SN20USBHX2001216_UNKNOWN_20231026_697_1_MODULE_IV_AMAC.json")
currents, currents2 = json_data.get_current(), json_data2.get_current()     #applies function to json_data & give them to 2 arrays of current & voltage
voltages, voltages2 = json_data.get_voltage(), json_data2.get_voltage() 

#IV_data_dict.update()

IV_files_dict['Run_63'] = [iv_63_loc]
IV_files_dict['Run_697'] = [iv_697_loc]
#print(IV_files_dict)

# Loop over the IV files dictionary
for run_number, IV_files in IV_files_dict.items():
    run_IV_data = []
    for IV_file in IV_files:
        IV_file_path = os.path.join(runs_directory, run_number, 'results', IV_file)
        currents, voltages = extract_IV(IV_file_path)
        run_IV_data.append([currents, voltages])
    IV_data_dict[run_number] = run_IV_data


#print(IV_data_dict['Run_29'])

plot_IV_dict = {} 

for run_number, iv_data_list in IV_data_dict.items():
    fig = go.Figure()
    
    for iv_data_set in iv_data_list:
        x_voltages = iv_data_set[0]
        y_currents = iv_data_set[1]
        
        fig.add_trace(go.Scatter(x= x_voltages, y = y_currents, 
                                 mode='lines+markers', name = f'{run_number} IV Data'))
    
    fig.update_layout(title = f'IV Data for {run_number}', xaxis_title= 'Bias Voltages [V]', yaxis_title = 'Current [µA]')
    #fig.show()
    plot_IV_dict[run_number] = fig   


#create a function that returns a dict, i.e. plot_IV_dict. Can then pass the key of the run, and will return the fig for that run. 
"""
for run_number, fig in plot_IV_dict.items():
    fig.show()
    

for run_number, fig in plot_IV_dict.items():
    pio.write_html(fig, f'{run_number}_plot.html')
"""

#print(plot_IV_dict)  