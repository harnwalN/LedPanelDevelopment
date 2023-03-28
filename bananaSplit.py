# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# This example implements a simple two line scroller using
# Adafruit_CircuitPython_Display_Text. Each line has its own color
# and it is possible to modify the example to use other fonts and non-standard
# characters.

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

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()
# This next call creates the RGB Matrix object itself. It has the given width
# and height. bit_depth can range from 1 to 6; higher numbers allow more color
# shades to be displayed, but increase memory usage and slow down your Python
# code. If you just want to show primary colors plus black and white, use 1.
# Otherwise, try 3, 4 and 5 to see which effect you like best.
#
# These lines are for the Feather M4 Express. If you're using a different board,
# check the guide to find the pins and wiring diagrams for your board.
# If you have a matrix with a different width or height, change that too.
# If you have a 16x32 display, try with just a single line of text.

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.A5, board.A1, board.A0, board.A4, board.D11],
    addr_pins=[board.D10, board.D5, board.D13, board.D9],
    clock_pin=board.D12, latch_pin=board.RX, output_enable_pin=board.TX)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

#For testing purposes only
line1 = adafruit_display_text.label.Label(
    font=terminalio.FONT,
    #background_color=0x000000,
    color=0x0066FF,
    padding_bottom=0,
    padding_left=0,
    padding_right=0,
    padding_top=0,
    background_tight=True,
    line_spacing=1.6,
    text="BANANA\nSPLIT")
line1.x = display.width
line1.y = 4


def shake(line):
    # line.x=29 only works at sleep(0.017)
    line.x = line.x - 1
    line_width = line.bounding_box[2]-64
    if line.x < -line_width:
        line.x = 29

def scroll(line):
    line.x = line.x - 1
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width

"""
# Not working yet
def rotate(Bitmap, W, L):
    w=0
    l=0
    while l<L:
        while w<W:
            Bitmap[w, l] = Bitmap[-((math.cos(math.degrees(90))*w)-(math.sin(math.degrees(90))*l)), (math.sin(math.degrees(90))*w) + (math.cos(math.degrees(90))*l)]
            w=w+1
        w=0
        l=l+1
"""
# Setup the file as the bitmap data source


bitmap = displayio.OnDiskBitmap("/betterBanana1.bmp")

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

# Create a Group to hold the TileGrid


group = displayio.Group()


# Add the TileGrid to the Group

group.append(tile_grid)
group.append(line1)

# Add the Group to the Display
display.show(group)

# Loop forever so you can enjoy your image
while True:
    shake(line1)
    sleep(0.017)
    display.refresh(minimum_frames_per_second=0)  # Write your code here :-)