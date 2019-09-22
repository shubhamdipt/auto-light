# auto-light
Script for switching light on off automatically using raspberry pi and smart tuya switch.

## Requirements
* Arduino light sensor
* Tuya smart plug
* Raspberry pi
* Python3

## Set up

Create a config.ini file about tuya smart plug with following contents.

````
[TUYA]
username = <username>
password = <password>
location = EU
device = <device_id>
````

## Usage

    python main.py
    
    
### Wiring

Raspberry Pi -> Light Sensor Module

3.3v P1 -> VCC (V)

GND P6 -> GND (G)

GPIO4 P7 -> SIGNAL (S)