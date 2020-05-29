# pi-ticker

I started this project because I've been working from home for the past 2 months and there
really is no end in sight with the pandemic happening. I'm working in my basement and the
rest of my family can't always tell when I'm on a Zoom call. I wanted a way to let them know
when I am on a call or just working and I had a [Raspberry Pi](https://www.raspberrypi.org/) with
a [Unicorn HAT HD](https://shop.pimoroni.com/products/unicorn-hat-hd) from an earlier project.

The display is updated by a script that subscribes to an MQTT topic. The MQTT messages can be triggered in various ways.
I have a script below which detects when you are in a Zoom call. There's also a menu driven client.

**ticker.py** - a headless service that subscribes to an MQTT topic and displays messages on a Unicorn HAT HD.

**ticker-client.py** - a client application that sends messages to an MQTT topic which are then displayed by the ticker service.

**zoom-detector.py** - script to detect when a zoom meeting is in progress. It looks for a `CptHost` process and sets the
ticker message accordingly.

**settings.yml** - used by the scripts above. Add your MQTT server address.

This service requires an MQTT server like [Mosquitto](http://mosquitto.org/). You can run it on the Raspberry Pi itself or on another computer you have on your network.


![Demo](demo.gif)

There are various ways to make the ticker.py script run when the Pi boots up. Systemd, Docker, auto-login and run the script in the `.bashrc`. 
My preference is to use Docker. I've added a Makefile with build and deploy rules. You'll need to set an environment variable named `TICKER_HOST`
that will be used to ssh to the Raspberry Pi you've already setup with Docker.
