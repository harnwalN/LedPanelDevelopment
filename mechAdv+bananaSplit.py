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

def shake(line):
    # line.x=29 only works at sleep(0.017)
    # the shake is hard-coded into this
    line.x = line.x - 1
    line_width = line.bounding_box[2]-64
    if line.x < -line_width:
        line.x = 29

def scroll(line):
    line.x = line.x - 1
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width

class MechAdv:
    def __init__(self):
        f = displayio.Group()
        display.show(f)

        bitWidth = 64
        bitLength = 32
        self.bitmap1 = displayio.Bitmap(bitWidth, bitLength, 7)

        # Working border
        i = 0
        while i < bitWidth:
            self.bitmap1[i, 0] = (i % 4)+1
            self.bitmap1[i, 1] = (i % 4)+1
            self.bitmap1[i, 31] = (i % 4)+1
            self.bitmap1[i, 30] = (i % 4)+1
            i = i+1

        # Palette
        self.palette1 = displayio.Palette(color_count=7)
        self.palette1[0] = 0x000000  # black
        self.palette1[1] = 0xFFFF00  # yellow
        self.palette1[2] = 0xFFFF00  # yellow again
        self.palette1[3] = 0x326fa8  # blue
        self.palette1[4] = 0x326fa8  # blue
        self.palette1[5] = 0xFFFF00  # yellow again
        self.palette1[6] = 0xFFFF00  # yellow again

        # TileGrid
        self.tilegrid1 = displayio.TileGrid(
            bitmap=self.bitmap1, pixel_shader=self.palette1, width=64, height=32, default_tile=0)

        # lines
        self.line1 = adafruit_display_text.label.Label(
            font=terminalio.FONT,
            color=0x0066FF,
            text="6328 Mechanical Advantage Littleton Robotics")
        self.line1.x = display.width
        self.line1.y = 8

        self.line2 = adafruit_display_text.label.Label(
            font=terminalio.FONT,
            color=0xFBFF00,
            text="Patriot Beverages, Deployed Resources, Bruce & Sue Bonner, NASA, Workers Credit Union, UML ARC, ZOLL, Rockwell Automation, Gene Haas Foundation, ETM Manufacturing, The Mighty Oak Fund, Intuitive Foundation, Millipore Sigma, PTC, Lilly Pulitzer, Tuck & Tuck Architects, Rotary Club of Littleton, Gore Foundation, Brett & Katie Bonner, Trina & Brian Miller, Michelle & Christopher Tuck, MBA Team, Headwall, Table Talk Pies, Burroughs Foundation, Couper Foundation, Bryan Newman, The Quan/Luh Family")
        self.line2.x = display.width
        self.line2.y = 23

        # add to group
        f.append(self.tilegrid1)
        f.append(self.line1)
        f.append(self.line2)

    def PaletteSwap(self, palette):
        oldPalette1 = palette[1]
        oldPalette2 = palette[2]
        oldPalette3 = palette[3]
        oldPalette4 = palette[4]

        palette[1] = oldPalette3
        palette[2] = oldPalette4
        palette[3] = oldPalette1
        palette[4] = oldPalette2
        display.refresh(minimum_frames_per_second=minFrameRate)

    def run(self):
        for x in range(len(self.line2.text)*6):
            self.PaletteSwap(self.palette1)
            scroll(self.line1)
            scroll(self.line2)
            sleep(0.0001)
            display.refresh(minimum_frames_per_second=minFrameRate)
        time.sleep(2)

class BananaSplit:
    def __init__(self):
        self.line1 = adafruit_display_text.label.Label(
            font=terminalio.FONT,
            # background_color=0x000000,
            color=0x0066FF,
            padding_bottom=0,
            padding_left=0,
            padding_right=0,
            padding_top=0,
            background_tight=True,
            line_spacing=1.6,
            text="BANANA\nSPLIT")
        self.line1.x = display.width
        self.line1.y = 4

        # Setup the file as the bitmap data source
        self.bitmap = displayio.OnDiskBitmap("/betterBanana1.bmp")

        # Create a TileGrid to hold the bitmap
        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.bitmap.pixel_shader)

        # Create a Group to hold the TileGrid
        self.group = displayio.Group()

        # Add the TileGrid to the Group

        self.group.append(self.tile_grid)
        self.group.append(self.line1)

        # Add the Group to the Display

    def run(self):
        display.show(self.group)
        for x in range(150):
            shake(self.line1)
            sleep(0.017)
            display.refresh(minimum_frames_per_second=minFrameRate)


while True:
    bs = BananaSplit()
    bs.run()

    time.sleep(2)

    ma = MechAdv()
    ma.run()
