#!/usr/bin/env python3

import colorsys
import time
import sys
import getopt
from sys import exit
import signal
import os

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

import unicornhathd


def sig_handler(signum, frame):
    unicornhathd.off()
    sys.exit(0)

def run_ticker(bg_color, text):
    FONT = ("DejaVuSans-Bold.ttf", 10)
    unicornhathd.rotation(90)
    unicornhathd.brightness(0.6)
    width, height = unicornhathd.get_shape()
    text_x = width
    text_y = 2
    font_file, font_size = FONT
    font = ImageFont.truetype(font_file, font_size)
    text_width, text_height = width, 0
    w, h = font.getsize(text)
    text_width += w + width
    text_height = max(text_height, h)
    text_width += width + text_x + 1

    image = Image.new('RGB', (text_width, max(16, text_height)), color)
    draw = ImageDraw.Draw(image)
    offset_left = 0
    draw.text((text_x + offset_left, text_y), text, fill="white", font=font)
    offset_left += font.getsize(text)[0] + width
    while True:
        for scroll in range(text_width - width):
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x + scroll, y))
                    r, g, b = [int(n) for n in pixel]
                    unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

            unicornhathd.show()
            time.sleep(0.01)

signal.signal(signal.SIGTERM, sig_handler)

try:
    opts, args = getopt.getopt(sys.argv[1:], "c:", ["color"])
    color = "black"

    for opt, arg in opts:
        if opt in ("-c", "--color"):
            color = arg

    text = args[0]
    run_ticker(color, text)

except getopt.GetoptError:
    print("display-text.py -c <hex color|color name> <text>")
    sys.exit(2)
except KeyboardInterrupt:
    unicornhathd.off()

finally:
    unicornhathd.off()
