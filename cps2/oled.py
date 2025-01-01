import board
import busio
from cps2.oled.oled_driver import OledDriver

i2c = busio.I2C(board.SCL, board.SDA)
oled = OledDriver(i2c)
oled.display_text("Test Message")
