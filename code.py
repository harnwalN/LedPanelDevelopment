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


# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Put each line of text into a Group, then show that group.
f = displayio.Group()
display.show(f)

bitWidth = 64
bitLength = 32
bitmap1 = displayio.Bitmap(bitWidth, bitLength, 6)

"""cornerLength = 2

c = 0

#Working Corner stuff (only for corner length 2) Only use if the left and right borders are also being used
#Might have to fix top and bottom border (borderLength) logic if using this

while c<cornerLength:
    bitmap1[0, c] = (c%cornerLength)+1
    bitmap1[1, c] = (c%cornerLength+1)+1

    bitmap1[0, bitLength - cornerLength + c] = (c%cornerLength)+1
    bitmap1[1, bitLength - cornerLength + c] = (c%cornerLength+1)+1

    bitmap1[bitWidth-2, c] = (c%cornerLength)+1
    bitmap1[bitWidth-1, c] = (c%cornerLength+1)+1

    bitmap1[bitWidth-2, bitLength - cornerLength + c] = (c%cornerLength)+1
    bitmap1[bitWidth-1, bitLength - cornerLength + c] = (c%cornerLength+1)+1

    c=c+1

#testing better corner logic
while c<cornerLength:
    bitmap1[c, c] = (c%cornerLength)
    c=c+1"""


# Working border
i = 0
while i < bitWidth:
    bitmap1[i, 0] = (i % 4)+1
    bitmap1[i, 1] = (i % 4)+1
    bitmap1[i, 31] = (i % 4)+1
    bitmap1[i, 30] = (i % 4)+1
    i = i+1

h = 0
"""while h<bitLength-4:
    bitmap1[0, h+2] = (h%2)+1
    bitmap1[1, h+2] = (h%2)+1
    bitmap1[63, h+2] = (h%2)+2
    bitmap1[62, h+2] = (h%2)+2
    h=h+1"""

palette1 = displayio.Palette(color_count=7)
palette1[0] = 0x000000  # black
palette1[1] = 0xFFFF00  # yellow
palette1[2] = 0xFFFF00  # yellow again
palette1[3] = 0x326fa8  # blue
palette1[4] = 0x326fa8  # blue
palette1[5] = 0xFFFF00  # yellow again
palette1[6] = 0xFFFF00  # yellow again

tilegrid1 = displayio.TileGrid(
    bitmap=bitmap1, pixel_shader=palette1, width=64, height=32, default_tile=0)


line1 = adafruit_display_text.label.Label(
    font=terminalio.FONT,
    color=0x0066FF,
    text="6328 Mechanical Advantage Littleton Robotics")
line1.x = display.width
line1.y = 8

line2 = adafruit_display_text.label.Label(
    font=terminalio.FONT,
    color=0xFBFF00,
    text="Patriot Beverages, Deployed Resources, Bruce & Sue Bonner, NASA, Workers Credit Union, UML ARC, ZOLL, Rockwell Automation, ETM Manufacturing, The Mighty Oak Fund, Intuitive Foundation, Millipore Sigma, PTC, Lilly Pulitzer, Tuck & Tuck Architects, Rotary Club of Littleton, Gore Foundation, Brett & Katie Bonner, Trina & Brian Miller, Michelle & Christopher Tuck, MBA Team, Headwall, Gene Haas Foundation, Table Talk Pies, Burroughs Foundation, Couper Foundation, Bryan Newman, The Quan/Luh Family")
line2.x = display.width
line2.y = 23

f.append(tilegrid1)
f.append(line1)
f.append(line2)


def scroll(line):
    line.x = line.x - 1
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width


def PaletteSwap(palette):
    oldPalette1 = palette[1]
    oldPalette2 = palette[2]
    oldPalette3 = palette[3]
    oldPalette4 = palette[4]

    palette[1] = oldPalette3
    palette[2] = oldPalette4
    palette[3] = oldPalette1
    palette[4] = oldPalette2
    display.refresh()


# You can add more effects in this loop. For instance, maybe you want to set the
# color of each label to a different value.
while True:
    PaletteSwap(palette1)
    scroll(line1)
    scroll(line2)
    sleep(0.0001)
    display.refresh(minimum_frames_per_second=0)  # Write your code here :-)
