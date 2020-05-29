FROM mapitman/python-arm:latest

RUN apk add --update --no-cache gcc python3-dev linux-headers musl-dev && pip3 install unicornhathd && apk del gcc python3-dev linux-headers musl-dev

WORKDIR /app
COPY DejaVuSans-Bold.ttf /app
COPY ticker.py /app
COPY requirements /app
COPY settings.yml /app

ENTRYPOINT ["python3", "/app/ticker.py"]
