# Video converter to an video that can be displayed on 16x16 matrix
It uses MAX7219 LED display drivers to create 16x16 matrix from 8x8 matrices
Connections is through serial port and unit needs to be connected all the time for it to work
Unit used for the project is Arduino Leonardo

## How to use
Send to your Arduino .ino file from this repo
After that run main.py with Python 3.10 passing 2 args:
- --port - serial port through which your unit is connected
- --input - video that should be taken as a input
- optional --output - you can give the place where output file will be saved(it's used for the openCV library)
