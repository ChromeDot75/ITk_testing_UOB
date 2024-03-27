import json
import os
import re
import plotly.graph_objects as go
import itertools
import pickle

def get_noise_files(run_folder):
    IV_files_dict = {}
    results_folder = os.path.join(run_folder, 'results')
    if os.path.exists(results_folder) and os.path.isdir(results_folder):
        noise_files = [f for f in os.listdir(results_folder) if f.endswith('.json') and 'RESPONSE_CURVE' in f]
        noise_files_dict[os.path.basename(run_folder)] = noise_files
    return noise_files_dict

runs_directory = "N:\\DASH\\Runs"

noise_files_dict = {}

# Loop over folders inside the "Runs" directory
for folder in os.listdir(runs_directory):
    run_folder = os.path.join(runs_directory, folder)
    # Check if folder starts with "Run_" followed by a number and is a directory
    if re.match(r'^Run_\d+$', folder) and os.path.isdir(run_folder):
        # Get IV files for this run
        noise_files_dict.update(get_noise_files(run_folder))
        
       

class JsonData:

    def __init__(self, json_FP):
        with open(json_FP) as file:
            data = json.load(file)
            self.results = data.get('results', {}) #starts search when sees this keyword and braces
    

    def get_innse(self):
        innse_away = self.results.get('innse_away', [])
        flattened_list = []
        for item in innse_away:
            if isinstance(item, list):
                flattened_list.extend(item)
            else:
                flattened_list.append(item)
        return flattened_list
    
    def get_gain(self):
        gain_away = self.results.get('gain_away', [])
        flattened_list = [] 
        for item in gain_away:
            if isinstance(item, list):
                flattened_list.extend(item)
            else:
                flattened_list.append(item)
        return flattened_list
    
    def get_vt50(self):
        vt50_away = self.results.get('vt50_away', [])
        flattened_list = [] 
        for item in vt50_away:
            if isinstance(item, list):
                flattened_list.extend(item)
            else:
                flattened_list.append(item)
        return flattened_list
        
        #return self.results.get('innse_away', [])    
    
    
def extract_noise(json_FP):
    json_data = JsonData(json_FP)
    return json_data.get_innse()

def extract_gain(jsonFP):
    json_data = JsonData(jsonFP)
    return json_data.get_gain()

def extract_vt50(jsonFP):
    json_data = JsonData(jsonFP)
    return json_data.get_vt50()


noise_data_dict = {}

gain_data_dict = {}

vt50_data_dict = {}

def process_files(noise_files_dict, runs_directory, extraction_function, data_dict):
    for run_number, noise_files in noise_files_dict.items():
        run_noise_data = []
        for noise_file in noise_files:
            noise_file_path = os.path.join(runs_directory, run_number, 'results', noise_file)
            innse = extraction_function(noise_file_path)
            run_noise_data.append({f"{noise_file.split('_')[0][-2:]}_{noise_file.split('_')[3]}": innse})
        data_dict[run_number] = run_noise_data

# Assuming extract_noise, extract_gain, extract_vt50 are defined elsewhere
# and noise_data_dict, gain_data_dict, vt50_data_dict are already defined

# Process noise data
process_files(noise_files_dict, runs_directory, extract_noise, noise_data_dict)

# Process gain data
process_files(noise_files_dict, runs_directory, extract_gain, gain_data_dict)

# Process vt50 data
process_files(noise_files_dict, runs_directory, extract_vt50, vt50_data_dict)

x_values = [] 
for i in range(1,1281): 
    x_values.append(i) 


def get_graphs(dict, Title):
    for run_number, data_lists in dict.items():  
        for noise in data_lists:
 
    
            fig = go.Figure()
        
            for i, y_values in enumerate(noise):
                fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers',
                          name = f'Dat{i+1}'))
        
            fig.update_layout(title=f'{Title} {run_number}',
                          xaxis_title='Channel Number',
                          yaxis_title='Electron Count')
            
            dict[run_number] = fig   
            #fig.show()
        
plot_gain_dict = {} 

for run_number, data_lists in gain_data_dict.items(): 
     
    for noise in data_lists: 
        #print(noise.keys())
         
        fig = go.Figure()
        
        for i, y_values in enumerate(noise):
            #print(y_values, noise[y_values])
            
            fig.add_trace(go.Scatter(x=x_values, y=noise[y_values], mode='lines', marker=dict(color='green'), 
                          name = f'Dat{i+1}'))
        
        fig.update_layout(title=f'Gain  {run_number}_{list(noise.keys())[0]}',
                          xaxis_title='Channel Number',
                          yaxis_title='Electron Count')
        #fig.show()
        plot_gain_dict[f"{run_number}_{list(noise.keys())[0]}"] = fig 



plot_noise_dict = {} 

for run_number, data_lists in noise_data_dict.items(): 
     
    for noise in data_lists: 
        #print(noise.keys())
         
        fig = go.Figure()
        
        for i, y_values in enumerate(noise):
            #print(y_values, noise[y_values])
            
            fig.add_trace(go.Scatter(x=x_values, y=noise[y_values], mode='lines', marker=dict(color='rgb(242,183,1)'),
                          name = f'Dat{i+1}'))
        
        fig.update_layout(title=f'Noise {run_number}_{list(noise.keys())[0]}',  #filename can be put in arguments, {filename} but dic
                          xaxis_title='Channel Number',
                          yaxis_title='Electron Count')
        #fig.show()
        plot_noise_dict[f"{run_number}_{list(noise.keys())[0]}"] = fig 

plot_vt50_dict = {} 

for run_number, data_lists in vt50_data_dict.items(): 
     
    for noise in data_lists: 
        #print(noise.keys())
         
        fig = go.Figure()
        
        for i, y_values in enumerate(noise):
            #print(y_values, noise[y_values])
            
            fig.add_trace(go.Scatter(x=x_values, y=noise[y_values], mode='lines', marker=dict(color='rgb(242,183,1)'),
                          name = f'Dat{i+1}'))
        
        fig.update_layout(title=f'VT50 {run_number}_{list(noise.keys())[0]}',  #filename can be put in arguments, {filename} but dic
                          xaxis_title='Channel Number',
                          yaxis_title='Voltage [mV]')
        #fig.show()
        plot_noise_dict[f"{run_number}_{list(noise.keys())[0]}"] = fig 



def plot_data_dicts(data_dict, x_values, plot_type, xaxis_title='Channel Number', yaxis_title='Electron Count', marker_color='green'):
    plot_dict = {}
    
    for run_number, data_lists in data_dict.items():
        for noise in data_lists:
            fig = go.Figure()

            for i, y_values in enumerate(noise.values()):
                fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', marker=dict(color=marker_color), 
                                          name = f'Dat{i+1}'))

            fig.update_layout(title=f'{plot_type} {run_number}_{list(noise.keys())[0]}',
                              xaxis_title=xaxis_title,
                              yaxis_title=yaxis_title)

            plot_dict[f"{run_number}_{list(noise.keys())[0]}"] = fig

    return plot_dict

# Plot gain data with customizations
plot_gain_dict = plot_data_dicts(gain_data_dict, x_values, "Gain", marker_color='blue')

# Plot noise data with customizations
plot_noise_dict = plot_data_dicts(noise_data_dict, x_values, "Noise", marker_color='red')

# Plot VT50 data with customizations
plot_vt50_dict = plot_data_dicts(vt50_data_dict, x_values, "VT50", yaxis_title='Voltage [mV]', marker_color='green')


pickle.dump(plot_noise_dict, open('data/noise_graphs.pkl','wb'))
pickle.dump(plot_gain_dict, open('data/gain_graphs.pkl','wb'))
pickle.dump(plot_vt50_dict, open('data/vt50_graphs.pkl','wb'))

pickle.dump(noise_data_dict, open('data/noise_data_dict.pkl','wb'))
pickle.dump(gain_data_dict, open('data/gain_data_dict.pkl','wb'))
pickle.dump(vt50_data_dict, open('data/vt50_data_dict.pkl','wb'))
