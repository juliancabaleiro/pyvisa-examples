"""
DC voltage measurement with Fluke 8558

Connection
----------
Voltage Input [Fluke 5500]: 5 Vrms 10 Hz
"""

import pyvisa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

rm=pyvisa.ResourceManager()
F8558_address="USB0::0x0F7E::0x8009::624282630::INSTR"
F8558=rm.open_resource(F8558_address)
F8558.timeout = 110000

print("ID: ",F8558.query("*IDN?"))

#Fluke 8558 configuratrion
F8558.write("*RST")
F8558.write("INIT:CONT OFF") #stop trigger
F8558.write("DISPlay ON")

#channel 
F8558.write("ROUT:TERM FRON") #FROM or REAR
F8558.write("ROUT:INP:GUAR OFF") # ON or OFF
#Volt
F8558.write("SENS:FUNC \"VOLTage:DC\"")
F8558.write("SENSe:VOLTage:DC:IMPedance 1M")
F8558.write("SENSe:VOLTage:DC:RANGe 10")
F8558.write("SENSe:VOLTage:DC:RESolution 1E-7") #1e-7 1e-3
F8558.write("SENSe:VOLTage:DC:NPLC MIN")
F8558.write("SENSe:VOLTage:DC:APERture:MODE AUTO")

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
       title='DC Voltage with Fluke 8558A')
ax.grid()
fig.savefig(r"F8558\files\data.png")

plt.show()

"""
Output
------
ID:  FLUKE,8558A,624282630,1.31

Configure the voltage source and press enter:

time:  104.5171549320221
Data shape:  (10,)
Data type:  <class 'numpy.ndarray'>
Data point type:  <class 'numpy.float64'>
Data:  [4.9999059 4.9999056 4.9999068 4.9999068 4.9999066 4.9999065 4.9999058
 4.9999064 4.999906  4.9999056]

"""

