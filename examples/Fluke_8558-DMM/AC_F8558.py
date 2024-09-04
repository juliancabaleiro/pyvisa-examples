"""
AC voltage measurement with Fluke 8558 DMM

Connection
----------
Voltage Input [Fluke 5500]: 5 Vrms 10 Hz
"""

import pyvisa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

rm=pyvisa.ResourceManager()
F8558_address="USB0::0x0F7E::0x8009::624282630::INSTR"
F8558=rm.open_resource(F8558_address)
F8558.timeout = 50000

print("ID: ",F8558.query("*IDN?"))

#Fluke 8558 configuratrion
F8558.write("*RST")
F8558.write("INIT:CONT OFF") #stop trigger
F8558.write("DISPlay ON")

#channel 
F8558.write("ROUT:TERM FRON") #FROM or REAR
F8558.write("ROUT:INP:GUAR OFF") # ON or OFF
#Volt
F8558.write("SENS:FUNC \"VOLTage:AC\"")
F8558.write("SENSe:VOLTage:AC:BWIDth WIDE")
F8558.write("SENSe:VOLTage:AC:COUPling:SIGNal AC1M")
F8558.write("SENSe:VOLTage:AC:COUNter:COUPling AC")
F8558.write("SENSe:VOLTage:AC:RESolution MIN")
F8558.write("SENSe:VOLTage:AC:RANGe 10")

# Current source manually setup
print("Configure the voltage source and press enter: ")
input()

#trigger
F8558.write("TRIGger:SOURce TIMer")
F8558.write("TRIGger:TIMer 0.5") #timer time or trigger time
F8558.write("TRIGger:COUNt 10") #trigger counts or #samples
F8558.write("TRIGger:DELay:AUTO OFF")
F8558.write("TRIGGER:DELay 0")

#Read
start=time.time()
data=F8558.query_ascii_values("READ?", container=np.array) #numpy.ndarray
end=time.time()

print("time: ",end-start)
print("Data shape: ",data.shape)
print("Data type: ", type(data))
print("Data point type: ", type(data[0]))
print("Data: ",data)

#save in csv
df=pd.DataFrame(data)
df.to_csv(r"F8558\files\data.csv", header=False, index=False)

#Plot data
fig, ax = plt.subplots()
ax.plot(data,
        marker="o",
        linestyle='None')
ax.set(xlabel='Number of Samples',
       ylabel='Voltage [V]',
       title='AC Voltage with Fluke 8558A')
ax.grid()
fig.savefig(r"F8558\files\data.png")

plt.show()

"""
Output
------
ID:  FLUKE,8558A,624282630,1.31

Configure the voltage source and press enter:
time:  4.706568241119385
Data shape:  (10,)
Data type:  <class 'numpy.ndarray'>
Data point type:  <class 'numpy.float64'>
Data:  [5.000088 5.000009 5.000003 5.000028 5.000011 5.000024 5.000001 5.000033
 5.000025 5.000035]

"""

