# HP 3245A Universal Source

This is a Universal Source can generate DC, Sin Waves, Square Waveform, Ramp, or arbitrary waveform in voltage and current.  
All amplitude values are considered as Peak-to-Peak values.
## Configure the communication

Because the instrument is old device use HP-IB an old version of GP-IB for this reason have different commands and communication termination must be configured for it to work correctly.  
Basically you have to adjust the termination in *\n*.

## HP3245A.py

This example show you how to configure the communication and query some configuration to the instrument.

## ACV_HP3245A.py

This example show you how to generate a voltage sine wave.

## ACI_HP3245A.py

This example show you how to generate a current sine wave.

## SQV_HP3245A.py

This example show you how to generate a voltage square wave.

## Useful Links

- [Datasheet](https://www.testequipmenthq.com/datasheets/Agilent-3245A-Datasheet.pdf)
- [Operating and Programming Manual](https://xdevs.com/doc/HP_Agilent_Keysight/HP%203245A%20Operating%20%26%20Programming.pdf)
- [Command Reference Manual](https://xdevs.com/doc/HP_Agilent_Keysight/HP%203245A%20Command%20Reference.pdf)