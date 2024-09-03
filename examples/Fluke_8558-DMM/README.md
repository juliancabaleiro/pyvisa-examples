# Fluke 8558 -8 1/2 digit's Digital Multimeter

This high precision digital multimeter has one channel with which it can measure DC voltage, AC voltage, DC current, AC current, resistance, frequency, temperature.   
Especially this instrument has the **Digitize** mode with which it allows to digitalize arbitrary voltage or current waveforms.

## Configure the communication

The instrument was configured for USB communication. This instrument can be configured in **High Speed mode**, this allows with some additionally configuration to transfer the data in binary form to achieve better communication times.  
For 1 MHz sampling frequency, 1 s acquisition time:
| Mode    | Data transfer time |
| -------- | ------- |  
| Normal mode      | 42.45384502410889 s   |  
| High speed mode  | 4.463783025741577 s   |

## DIGV_q_F8558.py 

Simple acquisition Fluke 8558A in voltage Digitize mode using query method

![Alt-Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/DIGV_q_F8558.png)

## DIGV_F8558.py

Simple acquisition Fluke 8558A in voltage Digitize mode using query_ascii_values method

## DIGV_High_speed_F8558.py

Simple acquisition Fluke 8558A in voltage Digitize mode with high speed transfer data.

![Alt-Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/DIGV_High_speed_F8558.png)


## DIGI_F8558.py

Simple acquisition Fluke 8558A in current Digitize mode using query_ascii_values method

![Alt-Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/DIGI_F8558.png)

## DIGI_High_speed_F8558.py

Simple acquisition Fluke 8558A in current Digitize mode with high speed transfer data.


## Useful Links

- [Product Specifications](https://s3.amazonaws.com/download.flukecal.com/pub/literature/8558A___pseng0700.pdf)
- [Operator Manual](https://s3.amazonaws.com/download.flukecal.com/pub/literature/8588a____omeng0000_0.pdf)
- [Remote Programmer's Manual](https://s3.amazonaws.com/download.flukecal.com/pub/literature/8588A___rpeng0000_0.pdf)