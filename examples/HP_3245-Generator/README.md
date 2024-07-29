# HP 3245A Universal Source

This is a Universal Source can generate DC, Sin Waves, Square Waveform, Ramp, or arbitrary waveform in voltage and current.  
All amplitude values are considered as Peak-to-Peak values.
## Configure the communication

Because the instrument is old device use HP-IB an old version of GP-IB for this reason have different commands and communication termination must be configured for it to work correctly.  
Basically you have to adjust the termination in *\n*.

> **Danger**  
> If communication fails regardless of why the instrument remains in the last state, probably with the output on and in remote mode, having to restart it manually or reestablishing communication to turn off the output.  
For to avoid this, ever you need to contain the possible errors and use a safe exit sequence.

## Commands

This instrument have a lot of commands, it even has commands for: loop, if, math, subroutine, memory management, etc. with the aim of generation arbitrary waveforms in the instrument. In the following example I do all the calculation in Python and only load the values into the instrument memory.


## HP3245A.py

This example show you how to configure the communication and query some configuration to the instrument.

## ACV_HP3245A.py

This example show you how to generate a voltage sine wave.

## ACI_HP3245A.py

This example show you how to generate a current sine wave.

## 2CH_ACV_HP3245A.py

This example show you how to generate two sine wave.  One sine wave per channel and connect
CHA in rear panel, CHB in front pannel and open the channels separatly.

## SQV_HP3245A.py

This example show you how to generate a voltage square wave.

## ArbitraryWave_HP3245A.py

This example show you how to generate a **Arbitrary Waveform** in this case a double exponential like LI-FULL (Standard Lightning Waveform), belloe you can see the acquisiion with the oscilloscope.

![Alt-Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/arb-hp3245-Wfm.png)

## Useful Links

- [Datasheet](https://www.testequipmenthq.com/datasheets/Agilent-3245A-Datasheet.pdf)
- [Operating and Programming Manual](https://xdevs.com/doc/HP_Agilent_Keysight/HP%203245A%20Operating%20%26%20Programming.pdf)
- [Command Reference Manual](https://xdevs.com/doc/HP_Agilent_Keysight/HP%203245A%20Command%20Reference.pdf)