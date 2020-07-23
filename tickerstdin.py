#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import sys
import yaml
from os import system
import re


with open("settings.yml", "r") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


broker = config["mqtt"]["broker"]
port = config["mqtt"]["port"]
ttl = config["mqtt"]["ttl"]

text = sys.stdin.readlines()[0].rstrip()
m = re.search("\S*", text)
text = m.group(0)

message = {}
message["bg_color"] = "navy"
message["text"] = text
payload = json.dumps(message)
client = mqtt.Client()
client.connect(broker, port, ttl)
client.publish("/ticker1", payload)
print(text)
