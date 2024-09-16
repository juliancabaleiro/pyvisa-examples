"""
AC caracterization of the specific probe using a RTO 2044 oscilloscope and FLuke 5500 calibrator
and save the data in .xlsx file

Notes:
------
- You can implement and algorithm to change time scale based on frecuency, but I am interested in
knowing the frecuency response in a specific configuration
"""
import pyvisa
import time
import os
import numpy as np
import pandas as pd

rm = pyvisa.ResourceManager()
RTO2044 = rm.open_resource('USB0::0x0AAD::0x0197::1329.7002k44-300157::INSTR')
F5500 = rm.open_resource('GPIB0::2::INSTR')
RTO2044.write("*RST")
F5500.write("*RST")

print("ID: ",RTO2044.query("*IDN?"))
print("ID: ",F5500.query("*IDN?"))

#test values
AC_rms=5
AC_frec=[50,60,100,500,1000,2000,5000,6000,8000,10000]

#user parameters
rto_scale = 0.2 #V
t_scale = 5e-3 #s
att = 1 #0.1 o 1
trgL = 0 #nivel de trigger
path=r"F5500_AC.xlsx" #path for data file

#Fluke 5500 configuration
F5500.write("EARTH OPEN") #OPEN
F5500.write("LOWS TIED") #OPEN
F5500.write("DC_OFFSET 0 V")
#F5500.write("LIMIT 750 V, -750 V")

#Start message
com="'"
start_msj=com[0]+"Start AC measurement "+com[0]

#display configuration
RTO2044.write("DISPlay:DIAGram:LABels ON") #enable axis labels
RTO2044.write("DISPlay:DIAGram:FINegrid OFF") #ruler scale in middle crosshair disabled
RTO2044.write("DISPlay:DIAGram:CROSshair OFF") #middle crosshair disabled
RTO2044.write("DISPlay:EXTended:PORDialogs ON") #if second screen is connected enable show the result boxes there
RTO2044.write("DISPlay:EXTended:POSDialogs ON") #if second screen is connected enable show the dialog boxes there

#Message in remote control
RTO2044.write(":SYSTem:DISPlay:UPDate ON") 
RTO2044.write(":SYSTem:DISPlay:MESSage:STATe ON") #Enable to show the message in remote control
RTO2044.write(":SYSTem:DISPlay:MESSage:TEXT "+start_msj) #load the start message
RTO2044.write(":SYSTem:DISPlay:UPDate OFF") #remote screen ON to show the message

time.sleep(5)

#waveforms
RTO2044.write(":SYSTem:DISPlay:UPDate ON") 
RTO2044.write(":CHANnel4:STATe 1") #CH 4 ON
RTO2044.write(":DISPlay:DIAGram:GRID ON") #screen grid ON
RTO2044.write(":DISPlay:DIAGram:TITLe ON") #enable tabs titles
RTO2044.write(":DISPlay:SIGBar ON") #show the rigth lateral bar
RTO2044.write("DISPlay:PERSistence:INFinite OFF") #persistance mode off
RTO2044.write("LAYout:SIGNal:ASSign Diagram1,C4W1") #add the first waveform from channel 4 at the diagram1

#General acquisition configuration
RTO2044.write("DISPlay:CLR") #clear the values in display
RTO2044.write("ACQuire:POINts:AUTO RESolution") #Fix the resolution
RTO2044.write("ACQuire:POINts:AADJust ON") #prevent undersampling
RTO2044.write("TIMebase:REFerence 0") #select the reference point for rescaling the time scale
RTO2044.write("TIMebase:ROLL:ENABle OFF") #Roll mode disable
RTO2044.write("ACQuire:INTerpolate SINC") #interpolation technique
RTO2044.write("CHANnel4:WAVeform1:STATe ON") #Activate waveform 1 del canal 1
RTO2044.write("CHANnel4:WAVeform1:TYPE SAMPle")# Decimation technique always applies some (HRESolution != Hdefinition)
RTO2044.write("CHANnel4:WAVeform1:ARIThmetics OFF") #disabble aritmetics acquisition (take some waveform to calculate the showed waveform)
RTO2044.write("ACQuire:SEGMented:MAX OFF") #turn off the segmentation
RTO2044.write("CHANnel4:POSition 0") # veritcal position of the channel
RTO2044.write("CHANnel4:OFFSet 0") #offset to make a offset correction
RTO2044.write("CHANnel4:BANDwidth FULL") #bandwith of the channel, differents acquisition modes can modify this value
RTO2044.write("CHANnel4:IMPedance 1e+6") #impedance of the channel (only for power calculation and mearuments software adjust)

#Verticual axis
RTO2044.write("CHANnel1:STATe OFF") #Disable the channel 1
RTO2044.write("CHANnel2:STATe OFF") #Disable the channel 2
RTO2044.write("CHANnel3:STATe OFF") #Disable the channel 3
RTO2044.write("CHANnel4:STATe ON")  #Enable the channel 4
RTO2044.write("CHANnel4:COUPling DCLimit") #Set 1 Mohm impedance in the channel
RTO2044.write("CHANnel4:GND OFF") #connect the signal to the ground
RTO2044.write("CHANnel4:SCALe "+str(rto_scale)) # virtical division

#Time base
RTO2044.write("TIMebase:SCALe "+str(t_scale)) #time scale; scale*10=Total time acquisition
RTO2044.write("ACQuire:SRATe 100e+6") #set sampling freuncy
RTO2044.write("ACQuire:SRReal 100e+6") #ADC sampling frencuency [10 GHz or 20 GHz]

#External attenuation (allow correct a custom attenuator)
RTO2044.write("CHANnel4:EATScale LIN") #attenuation mode
RTO2044.write("CHANnel4:EATTenuation "+str(att)) #attenuation factor

#HD- High Definition mode
RTO2044.write("HDEFinition:STATe ON") #Activate the High Definition mode in all the channels
RTO2044.write("HDEFinition:BWIDth 100e+6") #Fix the BW only defined values for this mode.For example 14 bits 100 MHz

#Trigger
RTO2044.write("TRIGger1:SOURce:SELect CHAN4") #Trigger source 
RTO2044.write("TRIGger1:TYPE EDGE") #Trigger type
RTO2044.write("TRIGger1:LEVel1:VALue "+str(trgL)) #trigger level
RTO2044.write("DISPlay:TRIGger:LINes ON") # Only vertical trigger line enable
RTO2044.write("TRIGger1:EDGE:SLOPe POS") # Positive edge trigger
RTO2044.write("TRIGger1:EVENt:BEEP NOACtion") #Disable beep trigger sound

#measures
RTO2044.write("MEASurement2:ENABle OFF") #disable others measurements groups
RTO2044.write("MEASurement3:ENABle OFF")
RTO2044.write("MEASurement4:ENABle OFF")
RTO2044.write("MEASurement5:ENABle OFF")
RTO2044.write("MEASurement6:ENABle OFF")
RTO2044.write("MEASurement7:ENABle OFF")
RTO2044.write("MEASurement8:ENABle OFF")
RTO2044.write("MEASurement9:ENABle OFF")
RTO2044.write("MEASurement10:ENABle OFF")
RTO2044.write("MEASurement1:ENABle ON") #enable measurement group 1
RTO2044.write("MEASurement1:SOURce C4W1") #signal source to add measurement
RTO2044.write("MEASurement1:CATegory AMPTime") #measure category
RTO2044.write("MEASurement1:MAIN PDELta") # add principal measurement, peak to peak
RTO2044.write("MEASurement1:ADDitional AMPLitude,ON") # add additional measurement parameter amplitude
RTO2044.write("MEASurement1:ADDitional MEAN,ON") # add additional measurement parameter mean
RTO2044.write("MEASurement1:ARNames ON") # Enable prefix to identify the measurements 
RTO2044.write("MEASurement1:STATistics:ENABle ON") # Enable statistic over the measurements
RTO2044.write("MEASurement1:CLEar") # clean the statistic history

#define auxiliar variables
data = {
        "frec":AC_frec,
        "pk":[],
        "amplitud":[],
        "rms_pk":[],
        "rms_amp":[],
        "std_pk":[],
        "std_amp":[],
        "mean":[],
        "mean_std":[]
}
pk_l=[]
amp_l=[]
std_pk_l=[]
std_amp_l=[]
rms_pk_l=[]
rms_amp_l=[]
mean_l=[]
mean_std_l=[]

try:
  #Measure loop
  for i in AC_frec:

    #Calibator set point
    print("Frecuency: ", i)
    F5500.write("OUT "+str(AC_rms)+" V, "+str(i)+" Hz") 
    F5500.write("*CLS") #Sometimes disable the output and generatea error code for safetly
    time.sleep(5) #Time to change the internal circuit (if requerid)
    F5500.write("OPER") #Enable the output
    time.sleep(15) #Settling time in the load

    #measure
    RTO2044.write("MEASurement1:CLEar") # clean statistics history
    time.sleep(5) #time to trigger the needed waveform

    pk_l.append(RTO2044.query("MEASurement1:RESult:AVG? PDELta")) #take averge of the positive peak
    amp_l.append(RTO2044.query("MEASurement1:RESult:AVG? AMPLitude")) #take the average of the amplitud parameter 
    std_pk_l.append(RTO2044.query("MEASurement1:RESult:STDDev? PDELta")) #take the STD pf the positive peak 
    std_amp_l.append(RTO2044.query("MEASurement1:RESult:STDDev? AMPLitude"))
    rms_pk_l.append(RTO2044.query("MEASurement1:RESult:RMS? PDELta")) #take the positive peak RMS
    rms_amp_l.append(RTO2044.query("MEASurement1:RESult:RMS? AMPLitude"))
    mean_l.append(RTO2044.query("MEASurement1:RESult:AVG? MEAN")) #take form the mean parameter the average statistic
    mean_std_l.append(RTO2044.query("MEASurement1:RESult:STDDev? MEAN"))

  #Using the query function all the values ​​stored in the list are of type str

  #save the data in a file
  data["pk"]=np.array(pk_l,dtype=float)
  data["amplitud"]=np.array(amp_l,dtype=float)
  data["std_pk"]=np.array(std_pk_l,dtype=float)
  data["std_amp"]=np.array(std_amp_l,dtype=float)
  data["rms_pk"]=np.array(rms_pk_l,dtype=float)
  data["rms_amp"]=np.array(rms_amp_l,dtype=float)
  data["mean"]=np.array(mean_l,dtype=float)
  data["mean_std"]=np.array(mean_std_l,dtype=float)

  #check the dimention for convert in dataframe
  print("pk len: ",len(data["pk"]))
  print("amplitud len: ",len(data["amplitud"]))
  print("std_pk len: ",len(data["std_pk"]))
  print("std_amp len: ",len(data["std_amp"]))
  print("rms_pk len: ",len(data["rms_pk"]))
  print("rms_amp len: ",len(data["rms_amp"]))
  print("mean len: ",len(data["mean"]))
  print("mean_std len: ",len(data["mean_std"]))

  df = pd.DataFrame(data)
  print(df)
  df.to_excel(path,index=False,
              columns=["frec",
                        "pk",
                        "amplitud",
                        "std_pk",
                        "std_amp",
                        "mean",
                        "mean_std"
                        ])
  
  #Output secuence
  F5500.write("STBY")
  F5500.write("OUT 0 V, 0 Hz")
except Exception as error:
  print("Error ocurred, Output secuence")
  print("The error is: ",error)
  #Output secuence
  F5500.write("STBY")
  F5500.write("OUT 0 V, 0 Hz") 

"""
Output:
-------

"""