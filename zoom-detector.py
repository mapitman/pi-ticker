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
        except (ProcessLookupError, PermissionError, psutil.NoSuchProcess) as e:
            print(f"Caught {e}")
            continue
    return isProcessFound    

def publish_message(message):
    payload = json.dumps(message)
    client = mqtt.Client()
    client.connect(broker, port, ttl)
    client.publish("/ticker1", payload)

signal.signal(signal.SIGTERM, sig_handler)

try:
    firstRun = True
    previouslyFoundZoomMeeting = False
    print("Monitoring for Zoom meeting...")
    while True:
        isMeetingInProgress = isZoomMeetingProcessRunning()
        if (firstRun or not previouslyFoundZoomMeeting) and isMeetingInProgress:
            firstRun = False
            previouslyFoundZoomMeeting = True
            message = {}
            message["bg_color"] = "red"
            message["text"] = on_a_call
            publish_message(message)
        elif (firstRun or previouslyFoundZoomMeeting) and not isMeetingInProgress:
            firstRun = False
            previouslyFoundZoomMeeting = False
            message = {}
            message["bg_color"] = "navy"
            message["text"] = working
            publish_message(message)

        time.sleep(10)

except KeyboardInterrupt:
        clearTicker()
        sys.exit()    