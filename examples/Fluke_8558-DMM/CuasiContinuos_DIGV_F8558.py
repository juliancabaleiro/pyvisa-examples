"""
Cuasi-Continuos acquisition with Fluke 8558 in digitize mode,
The objective is extract data periodically without missing points

Connection:
-----------
External trigger [HP-3245A]: 5 Vpk-pk; 2.5 Voffset; 1 Hz
Voltage Input [HP-3245A]: 5 Vpk-pk 0.5 Hz
This combination work's, but I change the trigger frecuency and investigate

Notes:
------
Voltage Input [HP-3245A]: 5 Vpk-pk 0.5 Hz
n_acquisition=10
Ext trg frec [Hz] | trg_tim [s] | trg_count [#] | python time [s] | Continuous acquisition
|--|--|--|--|--|
| 0.1 |1E-6 | 1E6 |9.97|NO |
| 0.5 |1E-6 | 1E6 |5.97| No|
| 0.8 |1E-6 | 1E6 |4.96 | Yes|
| 1 |1E-6 | 1E6 |4.95 | Yes|
| 2 |1E-6 | 1E6 |4.45 | No|
| 3 |1E-6 | 1E6 |4.6 | No|
| 0.5 |1E-3 | 1E3 |1.99 | Yes |
| 0.8 |1E-3 | 1E3 |1.99 | No |
| 1 |1E-3 | 1E3 |1.99 | Yes|
| 2 |1E-3 | 1E3 |1.49 | No|
"""

import pyvisa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

#user variables
n_acquisition=10
range_v=10
trg_tim= 1E-3
trg_count= 1E3

file_name = os.path.basename(__file__)

rm=pyvisa.ResourceManager()
F8558_address="USB0::0x0F7E::0x8009::624282630::INSTR"
F8558=rm.open_resource(F8558_address)
F8558.timeout = 100000

print("\nID: ",F8558.query("*IDN?"))

#Fluke 8558 configuratrion
F8558.write("*RST")
F8558.write("INIT:CONT OFF") #stop trigger
#High speed mode
F8558.write("DISP OFF")
print("DISP state: ",F8558.query("DISP?"))
F8558.write("CALCulate:SSTatistics:STATe OFF")
print("STATS: ",F8558.query("CALCulate:SSTatistics:STATe?"))
F8558.write("SYSTem:PRESet FAST") #no query command
F8558.write("FORMat:DATA PACKed,4") #no query command

#channel 
F8558.write("ROUT:TERM FRON") #FROM or REAR
F8558.write("ROUT:INP:GUAR OFF") # ON or OFF
#Volt
F8558.write("SENS:FUNC \"DIG:VOLT\"")
F8558.write("SENS:DIG:VOLT:COUP:SIGN DC10M")
F8558.write("SENS:DIG:VOLT:RANG "+str(range_v))
F8558.write("SENS:DIG:FILT 3MHZ")

#Aperture time <Tsampling
F8558.write("SENS:DIG:APER 7E-7") #7E-7

#Arm setup
F8558.write("ARM:LAY2:SOUR IMM")
F8558.write("ARM:LAY2:COUN 1") #count trigger 2
F8558.write("ARM:LAY2:DEL:AUTO OFF")
F8558.write("ARM:LAY2:DEL 0")
F8558.write("ARM:LAY1:SOUR EXT")
F8558.write("ARM:LAY1:COUN 1") #count trigger 1 Hasta 11
F8558.write("ARM:LAY1:DEL:AUTO OFF")
F8558.write("ARM:LAY1:DEL 0")

# #samples=count_tri1*Count_trig2
# Max samples: 5e6 with timestamp
# Max samples: 10e6 without timestamp

#trigger
F8558.write("TRIG:SOUR TIM")
F8558.write("TRIG:TIM "+str(trg_tim)) #frec sample in 
F8558.write("TRIG:COUN "+str(trg_count))
F8558.write("TRIG:DEL:AUTO OFF")
F8558.write("TRIG:DEL 0")
F8558.write("TRIG:HOLD OFF")

# scale factor query
scale_f=float(F8558.query("FORMat:DATA:SCALE?"))
print("Scale: ",scale_f)

#Launch trigger
F8558.write("INIT:CONT ON")
#Read
data=np.array([])
#Set continuous mode off in digitize
print("Conitnuous mode: ",F8558.query("INITiate:CONTinuous:STATe?"))

# Voltage source manually setup
print("Configure the voltage source and press enter: ")
#input()
print("Running")

#loop measurement
for j in range(n_acquisition): 
       print("Turn ",j)
       start = time.time()
       aux=F8558.query_binary_values("READ?",
                                       datatype="i",
                                       is_big_endian=True,
                                       container=np.ndarray)
       finish = time.time()
       data=np.append(data,aux)

l_data=len(data)
print("Time READ command: ",finish-start)
print("Data length: ",l_data)
print("Data type: ", type(data))
print("Data raw: ",data[:5])
data=data*scale_f
print("Data scaled: ",data[:5])

barra="\9"
path=r"files"+barra[0]+file_name[:-3]

#save in csv
df=pd.DataFrame(data)
df.to_csv(path+".csv", header=False, index=False)

#make time axis
ts=trg_tim
l_data=int(l_data)
t=np.linspace(0.0, l_data*ts, l_data, endpoint=False)

#Plot data
fig, ax = plt.subplots()
for i in range(n_acquisition):
    st=int(trg_count*i)
    fn=int(trg_count*(i+1))
    ax.plot(t[st:fn],data[st:fn],label="Read "+str(i))
#set the legend out of plot
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

ax.set(xlabel='Time [s]', ylabel='Voltage [V]',
       title='CuasiContinuous Voltage Digitize with High speed mode Fluke 8558A')
ax.grid()
fig.savefig(path+".png")
plt.show()

"""
Output
------

ID:  FLUKE,8558A,624282630,1.31

DISP state:  0

STATS:  0

Scale:  1.0124046414e-08
Conitnuous mode:  0

Configure the voltage source and press enter:

Running
Turn  0
Turn  1
Turn  2
Turn  3
Turn  4
Turn  5
Turn  6
Turn  7
Turn  8
Turn  9
Turn  10
Time READ command:  4.940692901611328
Data length:  16000000
Data type:  <class 'numpy.ndarray'>
Data raw:  [-2.27143680e+08 -2.27364864e+08 -2.27188736e+08 -2.27147776e+08
 -2.27176448e+08]
Data scaled:  [-2.29961316 -2.30185244 -2.30006931 -2.29965463 -2.2999449 ]

"""

