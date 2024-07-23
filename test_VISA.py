import pyvisa

rm=pyvisa.ResourceManager()
a=rm.list_resources()

for i in a:
    try:
        b=rm.open_resource(i)
        print(b.query("*IDN?"))
    except:
        print("could not be opened:",i)

"""

"""