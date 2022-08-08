#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import sys
import yaml
from os import system

with open("settings.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


broker = config["mqtt"]["broker"]
port = config["mqtt"]["port"]
ttl = config["mqtt"]["ttl"]

on_a_call = "On a Call..."
working = "Working..."
free = "Free..."
stop = "Clear the ticker"
holiday = "Happy Valentine's Day!!!"


while True:
    system("clear")
    print(f"1: {on_a_call}")
    print(f"2: {working}")
    print(f"3: {free}")
    print(f"4: {holiday}")
    print(f"C: {stop}")
    print("Q: Quit")
    print()
    print("Or type a custom message")
    print()
    user_input = input("Select a message to send: ")

    message = {}

    if user_input == "1":
        message["bg_color"] = "red"
        message["text"] = on_a_call
    elif user_input == "2":
        message["bg_color"] = "navy"
        message["text"] = working
    elif user_input == "3":
        message["bg_color"] = "green"
        message["text"] = free
    elif user_input == "4":
        message["bg_color"] = "red"
        message["text"] = holiday
    elif user_input == "c" or user_input == "C":
        message["command"] = "stop"
    elif user_input == "q" or user_input == "Q":
        sys.exit(0)
    else:
        message["bg_color"] = "cornflowerblue"
        message["text"] = user_input

    payload = json.dumps(message)
    client = mqtt.Client()
    client.connect(broker, port, ttl)
    client.publish("/ticker1", payload)
    print()
    print()
