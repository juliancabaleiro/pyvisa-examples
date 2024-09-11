"""
How take measurements and the statistic with R&S RTO 2044
with a complet configuration and using the High definition mode

Input
-----
AC 1 Vrms; frec 50 Hz
"""
import pyvisa
import time
import numpy as np
import pandas as pd

rm = pyvisa.ResourceManager()
RTO2044 = rm.open_resource('USB0::0x0AAD::0x0197::1329.7002k44-300157::INSTR')
RTO2044.write("*RST")
print("ID: ",RTO2044.query("*IDN?"))

#user parameters
rto_scale = 0.4 #V
t_scale = 5e-3 #s
att = 1 #0.1 o 1
trgL = 0 #nivel de trigger

#Start message
com="'"
start_msj=com[0]+"Start the measurement and statistic test"+com[0]

#display configuration
RTO2044.write("DISPlay:DIAGram:LABels ON") #enable axis labels
RTO2044.write("DISPlay:DIAGram:FINegrid OFF") #ruler scale in middle crosshair disabled
RTO2044.write("DISPlay:DIAGram:CROSshair OFF") #middle crosshair disabled
RTO2044.write("DISPlay:EXTended:PORDialogs ON") #if second screen is connected enable show the result boxes there
RTO2044.write("DISPlay:EXTended:POSDialogs ON") #if second screen is connected enable show the dialog boxes there

#Mensajes en el remote control
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
#Probe manual attenuation
#RTO2044.write("PROBe1:SETup:ATTenuation:MODE MANual") #Set manual configuration of the probe
#RTO2044.write("PROBe1:SETup:ATTenuation:UNIT V") #unit of the probe
#RTO2044.write("PROBe1:SETup:ATTenuation:MANual 1000") #manual attenuation

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

#defines and list to save the data
pk_l=[]
amp_l=[]
std_pk_l=[]
std_amp_l=[]
rms_pk_l=[]
rms_amp_l=[]
mean_l=[]
mean_std_l=[]

#start measurement
RTO2044.write("RUNContinous") # start continuous acquisition (RUNSingle,STOP)

try:
  #loop test
  for i in range(5):
    # Source configuration (if requerid)

    time.sleep(20) #settling time
    #mmeasure
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

  print("pk",len(pk_l))
  print("amplitud",len(amp_l))
  print("std_pk",len(std_pk_l))
  print("std_amp",len(std_amp_l))
  print("rms_pk",len(rms_pk_l))
  print("rms_amp",len(rms_amp_l))
  print("mean",len(mean_l))
  print("mean_std",len(mean_std_l))

  #save the data in some file extension
  
except Exception as e:
  #output secuence
  print(e)

