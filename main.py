from tuya.devices import TuyaSmartSwitch
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import configparser
import time

CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

LIGHT = GPIO.LOW
DARK = GPIO.HIGH

TIME_PERIOD = 60 * 5  # Every 5 minutes (should be less than 3600)
LIGHT_SENSOR_PIN = 4

CHECK_HOURS = [i for i in range(14, 23)]
MAX_AUTOMATIC_ON_PER_DAY = 1


def get_pin_status(pin):
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)


if __name__ == "__main__":

    try:
        device = TuyaSmartSwitch(
            username=CONFIG["TUYA"]["username"],
            password=CONFIG["TUYA"]["password"],
            location=CONFIG["TUYA"]["location"],
            device=CONFIG["TUYA"]["device"],
        )
        automatic_on_counts = 0
        reset_day = datetime.now() + timedelta(days=1)
        while True:
            time.sleep(TIME_PERIOD)
            current_time = datetime.now()

            if current_time.hour in CHECK_HOURS:
                if automatic_on_counts < MAX_AUTOMATIC_ON_PER_DAY:
                    device_status = device.get_status()
                    light_status = get_pin_status(pin=LIGHT_SENSOR_PIN)
                    if light_status == DARK and device_status is False:
                        print("Switching On.")
                        device.turn_on()
                        automatic_on_counts += 1
            if current_time.hour == 12 and current_time.day == reset_day.day:  # resets at 12
                automatic_on_counts = 0
                reset_day += timedelta(days=1)
    except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup()  # cleanup all GPI