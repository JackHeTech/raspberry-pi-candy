
import time
import sys
import os 

EMULATE_HX711=False
referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()

# setup stuff... 
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.reset()
hx.tare()

WINDOW_SIZE = 10

weights = []

# find rolling average of WINDOW_SIZE
def calculateRollingAverage(weights):
    return sum(weights) / len(weights)

INPUT_PIN_NUMBER = 5


while True:
    try:
        current_weight = hx.get_weight(INPUT_PIN_NUMBER)
        print(current_weight)
        if len(weights) < WINDOW_SIZE: 
            weights.append(current_weight)
        else: 
            rolling_average = calculateRollingAverage(weights) 
            if abs(current_weight - rolling_average) > 24000: 
                os.system("espeak -a 200 -v en-e3 \"Please take only one piece of candy\" --stdout | aplay")
            elif 8000 <= abs(current_weight - rolling_average) <= 12000: 
                os.system("espeak -a 200 -v en-e3 \"Thank you for only taking one piece of candy\" --stdout | aplay")
            # adjust the window
            weights.append(current_weight) 
            weights.pop(0)

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
