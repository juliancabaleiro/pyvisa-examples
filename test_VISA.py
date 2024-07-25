"""
This code list all the instruments connected and try to
communicate with them
"""
import pyvisa

rm=pyvisa.ResourceManager()
a=rm.list_resources()

for i in a:
    try:
        b=rm.open_resource(i)
        print("\nThe resource: ",i)
        print(b.query("*IDN?"))
    except:
        print("Could not be opened:",i)

"""
Output
------

The resource:  USB0::0x0AAD::0x0197::1329.7002k44-300157::INSTR
Rohde&Schwarz,RTO,1329.7002k44/300157,3.60.1.0


The resource:  GPIB0::14::INSTR
HEWLETT-PACKARD,34401A,0,10-5-2

"""