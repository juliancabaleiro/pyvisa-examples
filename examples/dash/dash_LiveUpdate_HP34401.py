"""
Simple live update using dash and PyVISA for AC measurement from HP34401.
The objective is obtain a fluid live update.
Use a subprocess to control the instrument and communicate with dash
usign shared array.

"""

import pyvisa
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import plotly.graph_objs as go
from collections import deque
from multiprocessing import Process, Array
import time 
from numpy.ctypeslib import as_ctypes
import numpy as np
import logging

#dash app declaration
app = dash.Dash(__name__)
#layout
app.layout = html.Div([
    html.H1("Live Update PyVISA HP-34401 AC values",
               style={'textAlign': 'center'}),
    dcc.Graph(id='live-graph',
              animate=False),
    dcc.Interval(id='graph-update',
                 interval=1*500),
])

#Callback
@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    """
    Read the data from shared array, build the figure and
    send it to the app
    """
    #read the from sahred array
    X=dataB
    Y=dataA

    data = go.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),
                                                xaxis_title="Samples [#]",
                                                yaxis_title="Voltage RMS [V]",)}

def run(dataA,dataB,window_l,address):
    """
    Suprocess function, Communicate with the instrument
    adcquire the data and put it in a shared array
    """
    X = deque(maxlen=window_l)
    Y = deque(maxlen=window_l)

    for i in range(window_l):
       X.append(0) 
       Y.append(1.7651)
       
    #Initialize the instrument
    rm = pyvisa.ResourceManager()
    HP34401=rm.open_resource(address)
    #Simple configuration of the instrument
    HP34401.write("*CLS")
    HP34401.write("*RST")
    HP34401.write("SYSTem:BEEPer:STATe OFF")
    #trigger
    HP34401.write("TRIGger:SOURce IMMediate") 
    HP34401.write("SENse:FUNCtion 'VOLTage:AC'") 
    HP34401.write("SENse:PERiod:APERture 1")
    HP34401.write("SENSe:DETector:BANDwidth 20")

    HP34401.write("DISPlay ON")
    HP34401.write("DISPlay:TEXT 'Empezar_med'")
    time.sleep(1)
    HP34401.write("DISPlay:TEXT:CLEar")
    HP34401.write("DISPlay ON")
    print(HP34401.query("ROUTe:TERMinals?"))

    while(1):
        X.append(X[-1]+1)
        dataB[:] = X
        #measure
        try:
             aux=HP34401.query("READ?")
        except Exception as e:
            print(e)

        Y.append(float(aux))
        dataA[:] = Y

        time.sleep(1)


if __name__ == '__main__':
    #User constants
    window_l=15
    HP_address="GPIB0::14::INSTR"

    datos_t=np.ones((window_l,))
    ctype = as_ctypes(datos_t)
    dataA  = Array(ctype._type_, datos_t, lock=False)
    dataB  = Array(ctype._type_, datos_t, lock=False)
    process1 = Process(target=run,     
                       args=(dataA,dataB,window_l,HP_address))
    #start the subproces
    process1.start()
    #To avoid unecessary prints
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    #Start dash app
    app.run_server(debug=False)

"""
Output
------

Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'dash_LiveUpdate_HP34401'
 * Debug mode: off
REAR
"""