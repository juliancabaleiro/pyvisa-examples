"""
DC linearity using Fluke 5500 and Fluke 8558A
and save the data in .xlsx
"""

import pyvisa
import time
import os
import numpy as np
import pandas as pd

file_name = os.path.basename(__file__)

rm = pyvisa.ResourceManager()
F8558_address="USB0::0x0F7E::0x8009::624282630::INSTR"
F8558=rm.open_resource(F8558_address)
F5500 = rm.open_resource('GPIB0::2::INSTR')
print("Calibrator: ",F5500.query("*IDN?"))
print("DMM: ",F8558.query("*IDN?"))

#Test Values

DC_values=[5,10,20,50,100,150,200,250,300,350,400,450,500,550,600,650,700]
DC_values=DC_values[::-1] #invert the order to safetly use autorange in DMM

#Fluke 5500 calibrator configuration
F5500.write("*RST")
F5500.write("EARTH OPEN") #OPEN or TIED
F5500.write("LOWS OPEN") #OPEN or TIED
F5500.write("DC_OFFSET 0 V")
F5500.write("LIMIT 750 V, -750 V")

#Fluke 8558A DMM configuration
F8558.write("*RST")
F8558.write("INIT:CONT OFF") #stop trigger
F8558.write("DISPlay ON")
F8558.timeout = 50000

#channel 
F8558.write("ROUT:TERM FRON") #FROM or REAR
F8558.write("ROUT:INP:GUAR OFF") # ON or OFF
#Volt
F8558.write("SENS:FUNC \"VOLTage:DC\"")
F8558.write("SENSe:VOLTage:DC:IMPedance 1M")
F8558.write("SENSe:VOLTage:DC:RESolution 1e-7") #1e-7 1e-3
F8558.write("SENSe:VOLTage:DC:NPLC MIN")
F8558.write("SENSe:VOLTage:DC:APERture:MODE AUTO")
F8558.write("SENSe:VOLTage:DC:RANGe:AUTO:STATe ON")

#trigger
F8558.write("TRIGger:SOURce TIMer")
F8558.write("TRIGger:TIMer 0.5") #timer time or trigger time
F8558.write("TRIGger:COUNt 10") #trigger counts or #samples
F8558.write("TRIGger:DELay:AUTO OFF")
F8558.write("TRIGGER:DELay 0")

v_mean=np.array([])
v_std=np.array([])
aux=np.array([])

#Measure loop
try:
  for i in DC_values:
    print("DC value: ", i)
    #Calibrator Configuration
    F5500.write("OUT "+str(i)+" V") 
    F5500.write("*CLS")
    time.sleep(5) #To change the board if required
    F5500.write("OPER")
    time.sleep(15) #To stabilize the value
    #Measure secuence
    aux=F8558.query_ascii_values("READ?", container=np.array) #numpy.ndarray
    #save the data
    v_mean=np.append(v_mean,np.mean(aux))
    v_std=np.append(v_std,np.std(aux))

  #Output secuence
  F5500.write("STBY") #In high current output is recomended lower the current slowly
  F5500.write("OUT 0 V, 0 Hz")
  F8558.write("SENSe:VOLTage:DC:RANGe 1000")

  #data management
  data_d={"nominal_value[V]":DC_values,
        "mean[V]":v_mean,
        "std[V]":v_std}

  data_df=pd.DataFrame(data_d)
  print(data_df)
  barra="\9"
  path=r"caracterisation\data"+barra[0]+file_name[:-3]+".xlsx"
  data_df.to_excel(path,index=False)
    
except Exception as error:
  print("Error ocurred, Output secuence")
  print("The error is: ",error)

  #Calibrator output secuence
  F5500.write("STBY") #In high current output is recomended lower the current slowly
  F5500.write("OUT 0 V, 0 Hz") 
  #multimeter output secuence
  F8558.write("SENSe:VOLTage:DC:RANGe 1000")

"""
Output
------

DMM:  FLUKE,8558A,624282630,1.31

DC value:  700
DC value:  650
DC value:  600
DC value:  550
DC value:  500
DC value:  450
DC value:  400
DC value:  350
DC value:  300
DC value:  250
DC value:  200
DC value:  150
DC value:  100
DC value:  50
DC value:  20
DC value:  10
DC value:  5
    nominal_value[V]     mean[V]    std[V]
0                700  699.995570  0.000300
1                650  649.996340  0.000080
2                600  599.996510  0.000137
3                550  549.996660  0.000092
4                500  499.996690  0.000070
5                450  449.996870  0.000100
6                400  399.997010  0.000104
7                350  349.997150  0.000092
8                300  299.998110  0.000070
9                250  249.998160  0.000049
10               200  199.998270  0.000046
11               150  149.998162  0.000023
12               100   99.998582  0.000026
13                50   49.999077  0.000021
14                20   19.999035  0.000005
15                10    9.999807  0.000002
16                 5    4.999908  0.000001
"""