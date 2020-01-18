FROM python:3.7-alpine3.10

LABEL Description="MQTT to InfluxDB very simple bridge"

#RUN apk update && apk --no-cache add build-base git libtool autoconf automake cmake pkgconf linux-headers mosquitto-clients

RUN echo "Installing required python packages"
RUN pip3 install influxdb paho-mqtt tzlocal
RUN echo "Copying script..."
COPY src/python/p1p2-mqtt-to-influxdb.py /app/p1p2-mqtt-to-influxdb.py
RUN echo "Done."

CMD ["python3", "/app/p1p2-mqtt-to-influxdb.py"]
