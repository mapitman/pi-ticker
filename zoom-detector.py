#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import sys
import yaml
from os import system
import psutil
import time
from sys import exit
import signal

with open("settings.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


broker = config["mqtt"]["broker"]
port = config["mqtt"]["port"]
ttl = config["mqtt"]["ttl"]

on_a_call = "On a Call"
working = "Working"

def clearTicker():
    message = {}
    message["command"] = "stop"
    payload = json.dumps(message)
    client = mqtt.Client()
    client.connect(broker, port, ttl)
    client.publish("/ticker1", payload)

def sig_handler(signum, frame):
    clearTicker()
    sys.exit(0)

def isZoomMeetingProcessRunning():
    isProcessFound = False
    for proc in psutil.process_iter():
        try:
            if proc.name().lower().startswith("cpthost"):
                isProcessFound = True
                break
        except ProcessLookupError:
            continue
    return isProcessFound    

signal.signal(signal.SIGTERM, sig_handler)

try:
    while True:
        isMeetingInProgress = isZoomMeetingProcessRunning()
        message = {}
        if isMeetingInProgress:
            message["bg_color"] = "red"
            message["text"] = on_a_call
        else:
            message["bg_color"] = "navy"
            message["text"] = working

        print(f"Zoom meeting in progress? {isMeetingInProgress}")
        payload = json.dumps(message)
        client = mqtt.Client()
        client.connect(broker, port, ttl)
        client.publish("/ticker1", payload)
        time.sleep(10)

except KeyboardInterrupt:
        clearTicker()
        sys.exit()    