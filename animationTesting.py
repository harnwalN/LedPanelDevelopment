import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from time import sleep
from rainbowio import colorwheel
import math
import time

minFrameRate = -1

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.A5, board.A1, board.A0, board.A4, board.D11],
    addr_pins=[board.D10, board.D5, board.D13, board.D9],
    clock_pin=board.D12, latch_pin=board.RX, output_enable_pin=board.TX)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

class Banana1:
    def __init__(self):
        self.f = displayio.Group()
        display.show(self.f)

        self.bitmap = displayio.OnDiskBitmap("/betterBanana1.bmp")
        # TileGrid
        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.bitmap.pixel_shader)

        # add to group
        self.f.append(self.tile_grid)
    def run(self):
        display.show(self.f)

class Banana2:
    def __init__(self):
        self.bitmap = displayio.OnDiskBitmap("/betterBanana2.bmp")

        # Create a TileGrid to hold the bitmap

        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.bitmap.pixel_shader)

        # Create a Group to hold the TileGrid
        self.group = displayio.Group()

        # Add the TileGrid to the Group

        self.group.append(self.tile_grid)
    def run(self):
        display.show(self.group)


while True:
    b1 = Banana1()
    b1.run()

    time.sleep(2)

    b2 = Banana2()
    b2.run()
    
    time.sleep(2)
