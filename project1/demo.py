import urllib.request
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
import tkinter as tk
from tkinter.ttk import Combobox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.ttk import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure


def handler():
    display_date = var.get()
    print(display_date)

    temp_dummy_df = temp_dataframe[temp_dataframe['Date']==display_date]
    temp_dummy_df = temp_dummy_df.drop(['Date'],axis=1)
    print(temp_dummy_df)

    pulse_dummy_df = pulse_dataframe[pulse_dataframe['Date']==display_date]
    pulse_dummy_df = pulse_dummy_df.drop(['Date'],axis=1)
    print(pulse_dummy_df)

    #Temp plot
    plt.ion()
    figure3 = plt.Figure(figsize=(10,10), dpi=100)
    ax3 = figure3.add_subplot(1,1,1)
    ax3.plot(temp_dummy_df['Time'],temp_dummy_df['Temperature'], color = 'g',marker='o')
    #ax3.scatter(temp_dummy_df['Time'],temp_dummy_df['Temperature'], color = 'g',marker='o')
    scatter3 = FigureCanvasTkAgg(figure3, top) 
    scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Temperature')
    ax3.set_title(display_date)


    #Pulse plot
    figure4 = plt.Figure(figsize=(10,10), dpi=100)
    ax4 = figure4.add_subplot(1,1,1)
    ax4.plot(pulse_dummy_df['Time'],pulse_dummy_df['Pulse'], color = 'g',marker='o')
    #ax3.scatter(temp_dummy_df['Time'],temp_dummy_df['Temperature'], color = 'g',marker='o')
    scatter4 = FigureCanvasTkAgg(figure4, top) 
    scatter4.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Pulse')
    ax4.set_title(display_date)


pulse_dataframe = pd.DataFrame(columns=['Date','Time','Pulse'])
temp_dataframe = pd.DataFrame(columns=['Date','Time','Temperature'])

TS1 = urllib.request.urlopen("https://api.thingspeak.com/channels/978846/fields/1.json?api_key=ZWU1L11PMBTW0POX")
res1 = TS1.read()
data1 = json.loads(res1)
for i in range(0,len(data1['feeds'])):
    if(data1['feeds'][i]['field1']!='' and data1['feeds'][i]['field1'] is not None):
        pulse_dataframe = pulse_dataframe.append({'Date':data1['feeds'][i]['created_at'].split('T')[0],'Time':data1['feeds'][i]['created_at'].split('T')[1][:-1],'Pulse':data1['feeds'][i]['field1']},ignore_index=True)
        
    else:
        pass
               
TS1.close()

TS2 = urllib.request.urlopen("https://api.thingspeak.com/channels/978846/fields/2.json?api_key=ZWU1L11PMBTW0POX")
res2 = TS2.read()
data2 = json.loads(res2)
for i in range(0,len(data1['feeds'])):
    if(data2['feeds'][i]['field2']!='' and data2['feeds'][i]['field2'] is not None):
        temp_dataframe = temp_dataframe.append({'Date':data2['feeds'][i]['created_at'].split('T')[0],'Time':data2['feeds'][i]['created_at'].split('T')[1][:-1],'Temperature':data2['feeds'][i]['field2']},ignore_index=True)
        
    else:
        pass
               
TS2.close()


top = Tk()
top.geometry('2000x2000') 

grouped = temp_dataframe.groupby('Date')
dates = list(grouped.groups.keys())

scrollbar = Scrollbar(top)
scrollbar.pack(side=RIGHT,fill=Y)


var = StringVar()
cb=Combobox(top,values=dates,textvariable=var)
cb.pack()
index1 = 0
index2 = 0

fig,ax = plt.subplots(4,2)
for j in dates:
    x = pulse_dataframe[pulse_dataframe['Date']==j]['Time']
    y = pulse_dataframe[pulse_dataframe['Date']==j]['Pulse']
    ax[index1][index2].plot(x,y)
    
    x = temp_dataframe[temp_dataframe['Date']==j]['Time']
    y = temp_dataframe[temp_dataframe['Date']==j]['Temperature']
    ax[index1][index2+1].plot(x,y)
    index1+=1

top.mainloop()
