import logging
from decimal import Decimal

import paho.mqtt.subscribe as subscribe
from influxdb import InfluxDBClient
from paho.mqtt.client import Client
from paho.mqtt.client import MQTTMessage

MQTT_HOST = "192.168.66.2"
INFLUXDB_HOST = "192.168.66.2"
INFLUXDB_DBNAME = "HASS"
TOPICS = ["P1P2/P/T/Flow",
          "P1P2/P/T/TempDHW",
          "P1P2/P/T/TempOut1",
          "P1P2/P/T/TempLWT",
          "P1P2/P/T/TempMWT",
          "P1P2/P/T/TempRWT",
          "P1P2/P/T/P1",
          "P1P2/P/T/P2",
          "P1P2/P/T/TempRoom2",
          "P1P2/P/M/ConsElecHeating",
          "P1P2/P/M/HeatProduced1",
          "P1P2/P/M/Heatproduced2",
          "P1P2/P/P/Gas",
          "P1P2/P/P/Compressor"
          ]
CLIENT_ID = "P1P2-to-influxdb"

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger("mqtt_dumper")
log.setLevel(logging.DEBUG)


def on_message(client: Client, userdata, message: MQTTMessage):
    msg = float(message.payload.decode())
    topic = message.topic
    log.debug("Sending to influx: %s %s", topic, msg)
    send_to_influxdb(topic, msg)


def send_to_influxdb(topic, value):
    json_body = [
        {
            'measurement': 'P1P2',
            'tags': {
                'topic': topic
            },
            'fields': {
                'value': value
            }
        }
    ]
    try:
        result = influxdb_client.write_points(json_body)
        log.debug("  Sent.")
    except Exception as e:
        print(e)


influxdb_client = InfluxDBClient(host=INFLUXDB_HOST, port=8086, timeout=10, username=None, password=None, database=INFLUXDB_DBNAME)
log.info("Connected to InfluxDB.")
subscribe.callback(callback=on_message, topics=TOPICS, hostname=MQTT_HOST, client_id=CLIENT_ID, clean_session=True)
influxdb_client.close();
log.info("Quit.")
