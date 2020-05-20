FROM mapitman/raspberrypi3-python:latest

WORKDIR /app

COPY DejaVuSans-Bold.ttf /app
COPY ticker.py /app
COPY requirements /app
COPY settings.yml /app

RUN pip3 install -r requirements
RUN pip3 install unicornhathd


ENTRYPOINT ["python3", "/app/ticker.py"]
