#!/usr/bin/env python3

import colorsys
import time
import sys
import getopt
from sys import exit
import signal
import os
import paho.mqtt.client as mqtt
import json
import yaml

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

import unicornhathd


def sig_handler(signum, frame):
    run_ticker("red", "Shutting down")
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
    text_height = max(text_height, h)
    text_width = 2 * width + w

    image = Image.new('RGB', (text_width, max(16, text_height)), bg_color)
    draw = ImageDraw.Draw(image)
    offset_left = 0
    draw.text((text_x + offset_left, text_y), text, fill="white", font=font)
    offset_left += font.getsize(text)[0] + width
    for scroll in range(text_width - width):
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x + scroll, y))
                r, g, b = [int(n) for n in pixel]
                unicornhathd.set_pixel(width - 1 - x, y, r, g, b)
        time.sleep(0.01)
        unicornhathd.show()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("/ticker1")

def on_message(client, userdata, msg):
    global RUN_DISPLAY
    global TEXT
    global BG_COLOR
    payload = json.loads(msg.payload.decode())
    if "command" in payload:
        command = payload["command"]
    else:
        command = "go"
    if command == "stop":
        RUN_DISPLAY = False
    else:
        TEXT = payload["text"]
        BG_COLOR = payload["bg_color"]
        RUN_DISPLAY = True
    print(msg.payload.decode())

signal.signal(signal.SIGTERM, sig_handler)

try:
    RUN_DISPLAY = False
    BG_COLOR = "purple"
    TEXT = ""

    with open("settings.yml", "r") as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    broker = config["mqtt"]["broker"]
    port = config["mqtt"]["port"]
    ttl = config["mqtt"]["ttl"]

    run_ticker("green", "Starting up")

    client = mqtt.Client()
    client.connect(broker, port, ttl)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()

    while True:
        if RUN_DISPLAY:
            run_ticker(BG_COLOR, TEXT)
        else:
            unicornhathd.off()
        # time.sleep(0.5)

except KeyboardInterrupt:
    unicornhathd.off()

finally:
    unicornhathd.off()
