import numpy as np
from scipy.stats import ttest_ind
from scipy import stats
import plotly.graph_objs as go 
from plotly.subplots import make_subplots
import pandas as pd
from scipy.stats import f_oneway
import plotly.express as px
import pickle

gain_data_dict = pickle.load(open('data/gain_data_dict.pkl','rb'))
noise_data_dict = pickle.load(open('data/noise_data_dict.pkl','rb'))
vt50_data_dict = pickle.load(open('data/vt50_data_dict.pkl','rb'))

len_14 =  (len(gain_data_dict.get('Run_14')))

x_p=[]
y_t=[]


def get_t_value(run_name,pole):
    if len_14 > 1:
            #data=gain_data_dict.get(run_name)
            data=gain_data_dict.get(run_name)
            
            data_dict={}
            for d in data:
                data_dict.update(d)

            df=pd.DataFrame.from_dict(data_dict)
            df=df[sorted(df.columns,key=lambda x: int(x.split('_')[1]))]
            values=[x for x in df.columns if x.startswith('3X')] if pole=="x" else [x for x in df.columns if x.startswith('3Y')]
            reference_key=values[0]
            reference_value=df[reference_key].dropna(axis=0).values
            print("RF: ", np.mean(reference_value))
            print("RF: ",np.std(reference_value))
            #print(reference_key,reference_value)
            #print(values, type(values))
            compare_columns=values[1:]
            #print(df[compare_columns])
            time, p_value = [], []
            for i, col in enumerate(compare_columns):
                print(i, " ", np.mean(df[col].dropna(axis=0).values))
                print(i, " ", np.std(df[col].dropna(axis=0).values))
                #print(df[col].dropna(axis=0).values)
                t_statistic, p_value_tt = stats.ttest_ind(reference_value, df[col].dropna(axis=0).values)
                print(i, p_value_tt)
                #t_stat_one_way,  p_value_one = f_oneway(reference_value, df[col].dropna(axis=0).values)
                time.append((i+1)*20)
                p_value.append(p_value_tt)
            symnmtrical_values=[]
            
            for p in p_value:
                if p>0.05:
                    symnmtrical_values.append(0.06)
                elif p<0.05:
                    symnmtrical_values.append(0.04)
                else:
                    symnmtrical_values.append(0.05)
            data_p=pd.DataFrame.from_dict({
                'p_value':p_value,
                'time':time,
                'semetrical_values':symnmtrical_values
            })

            fig = px.bar(data_p,x='time',y="semetrical_values",hover_name='p_value')
            fig.add_hline(y = 0.05, line_dash = 'dash', line_color = 'red', annotation_text = 'Significance Threshold')
            
            #fig.show()
            #print(time, p_value)
            return fig, 
            #return time, p_value 
            
get_t_value('Run_14','x')
get_t_value('Run_14','y')
