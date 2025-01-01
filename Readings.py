import board
import busio
import time
import adafruit_dht
from digitalio import DigitalInOut, Direction
from adafruit_ht16k33 import segments
import adafruit_ws2812b
import adafruit_temt6000

# Setup DHT22 sensor
dht22 = adafruit_dht.DHT22(board.D2)

# Setup WS2812B
led = adafruit_ws2812b.WS2812B(board.D3, 1)

# Setup TEMT6000
temt6000 = adafruit_temt6000.TEMT6000(board.A0)

# Setup HC-SR04 ultrasonic sensor
trig = DigitalInOut(board.D4)
echo = DigitalInOut(board.D5)
trig.direction = Direction.OUTPUT
echo.direction = Direction.INPUT

# Setup FeatherWing OLED
i2c = busio.I2C(board.SCL, board.SDA)
display = segments.Segment(i2c)

def get_distance():
    trig.value = True
    time.sleep(0.00001)
    trig.value = False
    start_time = time.time()
    while echo.value == 0:
        start_time = time.time()
    while echo.value == 1:
        stop_time = time.time()
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Speed of sound = 34300 cm/s
    return distance

def main():
    while True:
        try:
            # Read temperature and humidity
            temperature = dht22.temperature
            humidity = dht22.humidity
            
            # Get water level
            distance = get_distance()
            
            # Read ambient light
            light_level = temt6000.light
            
            # Display data on OLED
            display.print(f"T: {temperature} H: {humidity} D: {distance:.1f} L: {light_level:.2f}")
            
            # Control LED based on water level
            if distance < 10:  # If water level is low
                led[0] = (255, 0, 0)  # Red
            else:
                led[0] = (0, 255, 0)  # Green
            
            time.sleep(2)

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2)

if __name__ == "__main__":
    main()
