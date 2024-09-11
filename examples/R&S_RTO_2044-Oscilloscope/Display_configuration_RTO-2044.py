"""
Test display functionalities does not make any measurements.
Create figures, put labels in plots, show the remote screen with messages.

I recommend put update on before any use, and after exit
If the communication with the instrument is not continuous the screen change automatically
"""

import pyvisa
import time
import random
import os

rm = pyvisa.ResourceManager()
RTO2044_address='USB0::0x0AAD::0x0197::1329.7002k44-300157::INSTR'
RTO2044 = rm.open_resource(RTO2044_address)
print("ID: ",RTO2044.query("*IDN?"))

#General configuration
RTO2044.write("*RST")
print("Data type:",RTO2044.query("FORMat:DATA?"))
print("endianess: ",RTO2044.query("FORMat:BORDer?"))
print("Oscilloscope date: ",RTO2044.query(":SYSTem:DATE?"))
# To change the time in the osciloscopio
#hora=time.localtime()
#RTO2044.write(":SYSTem:TIME " +str(hora.tm_hour)+","+str(hora.tm_min)+","+str(hora.tm_sec))
print("Oscilloscope Time: ",RTO2044.query(":SYSTem:TIME?"))

# Message on the full screen only showed when the display update is off
RTO2044.write(":SYSTem:DISPlay:UPDate OFF")
print("Message enable?: ",RTO2044.query(":SYSTem:DISPlay:MESSage:STATe?"))
RTO2044.write(":SYSTem:DISPlay:MESSage:STATe ON") #Enable the message
RTO2044.write(":SYSTem:DISPlay:MESSage:TEXT 'Start Display configuration'") # Max 45 caracters in one line
RTO2044.write(":SYSTem:DISPlay:UPDate OFF") # when the display is turned off the messages is displayed
time.sleep(2) #pause to show the message

#mesurement layout confuguration
RTO2044.write(":SYSTem:DISPlay:UPDate ON") #remove the black remote screen
RTO2044.write(":CHANnel1:STATe 1") #turn on or off the channel waveform
RTO2044.write(":CHANnel2:STATe 1")
RTO2044.write(":CHANnel3:STATe 1")
RTO2044.write(":CHANnel4:STATe 1")
#hay que arrancar dando un refenrencia desde Diagram1 que es por defecto
#el ON es para poner izquierdao derecha/ arriba abajo
#en caso del tab queda prendido el utltimo tab que se pone o se puede elegir con SHOW
# Add graphs or tabs windows with asigned waveforms, the position always be referred to another figure/diagram/layout
RTO2044.write(":LAYout:ADD 'Diagram1',VERtical,OFF,C1W1,'grafico2'") #always start using Diagram1 as reference
RTO2044.write(":LAYout:ADD 'grafico2',VERtical,ON,C2W1,'grafico3'") #create grafico3 below grafico2
RTO2044.write(":LAYout:ADD 'grafico3',HORizontal,ON,C3W1,'grafico4'") #left
RTO2044.write(":LAYout:ADD 'grafico4',HORizontal,OFF,C4W1,'grafico5'") #rigth
RTO2044.write(":LAYout:ADD 'grafico2',TAB,ON,M1,'grafico6'") #the last tab configures is showed,
                                                             #if not use the comand LAYout:SHOW to show a specfict tab

#some function like assign, zoom, etc cannot be used if the figure is not shown
RTO2044.write(":LAYout:SHOW 'grafico2'") #select grafico2 how the tab showed
RTO2044.write("LAYout:SIGNal:ASSign 'grafico2',C1W1") # shows C1W1 waveform in the graph
time.sleep(1)
RTO2044.write(":LAYout:SIGNal:UNAssign M1") #move the selected (assign) signal to the icon menu (rigth lateral bar)
time.sleep(1)
#RTO2044.write(":LAYout:ZOOM:ADD 'grafico2',VERT,OFF,-10e-9,10e-9,-0.05,0.04,'zoom1'") #create a new diagram/figure by zooming in on another one
#RTO2044.write(":LAYout:REMove 'zoom1'") #remove the figure/diagrama but leave the gap empty

#**some DISPlay commands it has to be used before the LAYout commands**
RTO2044.write(":DISPlay:DIAGram:GRID ON") #turn on the grid
RTO2044.write(":DISPlay:DIAGram:TITLe ON") #Remove the flap with the names of the diagramas in the layout
RTO2044.write(":DISPlay:SIGBar ON") # Turn ON or OFF the rigth information bar
#Agrega un comentario en los graficos, los ubico en forma relativa
# Add a comment in diagrams, Iplace them in relative way
RTO2044.write(":DISPlay:SIGNal:LABel:ADD 'messange',C1W1,'CH 1',REL,25,25") # message is the label ID; CH 1 is the label text
RTO2044.write(":DISPlay:SIGNal:LABel:ADD 'messange2',C2W1,'CH 2',REL,25,25")
RTO2044.write(":DISPlay:SIGNal:LABel:ADD 'messange3',C3W1,'CH 3',REL,25,25")
RTO2044.write(":DISPlay:SIGNal:LABel:ADD 'messange4',C4W1,'CH 4',REL,25,25")
#cambia el texto dle label
RTO2044.write(":DISPlay:SIGNal:LABel:TEXT 'messange',C1W1,'Hello world'") #change the menssage text
RTO2044.write(":DISPlay:SIGNal:LABel:HORIzontal:RELative:POSition 'messange',C1W1,0") #change position of the text
RTO2044.write(":SYSTem:DISPlay:UPDate ON")
# I recommend put update on before any use, and after exit
# If the communication with the instrument is not continuous the screen change automatically
time.sleep(2)

# start text position change show
for i in range(5):
  ver=random.randint(5,95)
  hor=random.randint(5,95)
  RTO2044.write(":DISPlay:SIGNal:LABel:VERTical:RELative:POSition 'messange',C1W1,"+str(ver))
  RTO2044.write(":DISPlay:SIGNal:LABel:HORIzontal:RELative:POSition 'messange',C1W1,"+str(hor))
  RTO2044.write(":DISPlay:SIGNal:LABel:VERTical:RELative:POSition 'messange2',C2W1,"+str(ver))
  RTO2044.write(":DISPlay:SIGNal:LABel:HORIzontal:RELative:POSition 'messange2',C2W1,"+str(hor))
  RTO2044.write(":DISPlay:SIGNal:LABel:VERTical:RELative:POSition 'messange3',C3W1,"+str(ver))
  RTO2044.write(":DISPlay:SIGNal:LABel:HORIzontal:RELative:POSition 'messange3',C3W1,"+str(hor))
  RTO2044.write(":DISPlay:SIGNal:LABel:VERTical:RELative:POSition 'messange4',C4W1,"+str(ver))
  RTO2044.write(":DISPlay:SIGNal:LABel:HORIzontal:RELative:POSition 'messange4',C4W1,"+str(hor))
  RTO2044.write(":SYSTem:DISPlay:UPDate ON")
  time.sleep(2)

#remove the labels
RTO2044.write(":DISPlay:SIGNal:LABel:REMove 'messange',C1W1")
RTO2044.write(":DISPlay:SIGNal:LABel:REMove 'messange2',C2W1")
RTO2044.write(":DISPlay:SIGNal:LABel:REMove 'messange3',C3W1")
RTO2044.write(":DISPlay:SIGNal:LABel:REMove 'messange4',C4W1")

#Cursor style selection
RTO2044.write("CURSor1:STYLe 'LRHombus'")
RTO2044.write("DISPlay:RESultboxes:CUPosition 'PREV'")

#print(RTO2044.query("MEASurement1:RESult:LABorder?"))

RTO2044.write("DISPlay:CLR") #delete all results, measuremente, long-term, waveforms, etc
RTO2044.write("DISPlay:PERSistence:INFinite OFF") #ON or OFF persistence mode, remain on the screen all the points, can use timer
RTO2044.write("DISPlay:INTensity *RST") # change the strength of the waveforms

RTO2044.write("*RST") #reset the instrument

#calibration info
#print("Calibration date: ",RTO2044.query("CALibration:DATE?"))
#print("Calibration time: ",RTO2044.query("CALibration:TIME?"))
print("Calibration result: ",RTO2044.query("CALibration:RESult?"))
print("Calibration state: ",RTO2044.query("DIAGnostic:SERVice:STST:STATe?"))

print("Quantity of channels: ",RTO2044.query("DIAGnostic:SERVice:CHANnelcount?"))

# Channel configuration
RTO2044.write(":CHANnel1:STATe 1") #activate channel 1
RTO2044.write(":CHANnel2:STATe 1")
RTO2044.write("LAYout:SIGNal:ASSign Diagram1,C1W1") #Add the first waveform to the channel 1 in diagrama 1
RTO2044.write("LAYout:SIGNal:ASSign Diagram1,C2W1")
RTO2044.write("*WAI") #Some channel setup are asynchronous, this command is recommended

#acquisition modes
RTO2044.write("ACQuire:COUNt *RST") #1 number at waveforms to calculate the average waveform
RTO2044.write("*WAI")
RTO2044.write("RUNSingle") #start the defined cycles that were set with  previus command
RTO2044.write("*WAI")
RTO2044.write("RUNContinous") #start continuos adcqusition
RTO2044.write("*WAI")

#Horizontal configuration
RTO2044.write("TIMebase:SCALe 100E-6") #Time scale 0.1 or 100E-6 horizontal scale
#RTO2044.write("TIMebase:RANGe 0.2") #adjust total time in screen but always complies with scale*10=timebaserange 
#Fix the points in screen only in auto resolution mode
RTO2044.write("ACQuire:POINts:AUTO 'RESolution'") #Time resolution auto adjust
print("Start time resolution: ",RTO2044.query("ACQuire:RESolution?"))
print("Start maximun points: ",RTO2044.query("ACQuire:POINts:MAXimum?"))
RTO2044.write("ACQuire:POINts:MAXimum 1E6") #set limits for record length
print("Modified data points: ",RTO2044.query("ACQuire:POINts:MAXimum?"))
print("Modified time resolution: ",RTO2044.query("ACQuire:RESolution?"))
#Fixed time resolution
RTO2044.write("ACQuire:POINts:AADJust OFF") #resolution auto adjust disable
RTO2044.write("ACQuire:RESolution 1E-8") #set the time resolution (time between two points)

#ADC configuration
print("ADC RATE: ",RTO2044.query("ACQuire:POINts:ARATe?")) #ADC sample frencuency only two values thats depend the mode

print("SRATE before: ",RTO2044.query("ACQuire:SRATe?")) #sample rate
RTO2044.write("ACQuire:SRATe 1E6") # 1E6 <SRATE<1E11
RTO2044.write("*WAI")
print("SRATE after: ",RTO2044.query("ACQuire:SRATe?"))
print("Resolution Srate",RTO2044.query("ACQuire:RESolution?")) #SRate=1/Resolution

# overwrite each other
#RTO2044.write("TIMebase:SCALe 5") #Time per division
#RTO2044.write("TIMebase:RANGe 50") #Time of one acquisition scale*10
print("Total division on the screen: ",RTO2044.query("TIMebase:DIVisions?"))

RTO2044.write("ACQuire:INTerpolate SINX") #change interpolation/decimation 
print("SSreal: ",RTO2044.query("ACQuire:SRReal?")) #samples for decimation (only with interpolation activated)
#RTO2044.write("ACQuire:POINts:VALue 1000000") #If scale or resolution were set, it does not modify the value
print("#Waveform Points",RTO2044.query("ACQuire:POINts:VALue?"))

#Roll mode
RTO2044.write("TIMebase:ROLL:ENABle OFF")
print("Roll mode state: ",RTO2044.query("TIMebase:ROLL:STATe?"))

#Zero position
RTO2044.write("TIMebase:HORizontal:POSition 50E-6") #time distance between zero point of diagram
RTO2044.write("TIMebase:REFerence 1") #reference point on the screen position, in % of screen

RTO2044.write(":SYSTem:DISPlay:MESSage:TEXT 'End Display overview'")
RTO2044.write(":SYSTem:DISPlay:UPDate OFF")

time.sleep(5)
RTO2044.write("USRDefined:RST:ENABle OFF") #default configuration

"""
Output:
-------


"""
