from flask import Flask, request, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)

app.config["MQTT_BROKER_URL"] = "test.mosquitto.org"
app.config["MQTT_BROKER_PORT"] = 1883
app.config[
    "MQTT_USERNAME"
] = ""  # Set this item when you need to verify username and password
app.config[
    "MQTT_PASSWORD"
] = ""  # Set this item when you need to verify username and password
app.config["MQTT_KEEPALIVE"] = 5  # Set KeepAlive time in seconds
app.config["MQTT_TLS_ENABLED"] = False  # If your server supports TLS, set it True
topic = "esp32/test"
topic2 = "ceva"

mqtt_client = Mqtt(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        mqtt_client.subscribe(topic)  # subscribe topic
        mqtt_client.subscribe(topic2)
    else:
        print("Bad connection. Code:", rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(topic=message.topic, payload=message.payload.decode())
    print("Received message on topic: {topic} with payload: {payload}".format(**data))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
