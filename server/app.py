from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from services.mqtt_service import handle_message

app = Flask(__name__)
app.config["SECRET_KEY"] = "licenta-mqtt"
app.config["MQTT_BROKER_URL"] = "test.mosquitto.org"
app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_KEEPALIVE"] = 5  # Set KeepAlive time in seconds
humidity_topic = "cd906955-d4ab-4db7-b281-54f1043e32e2-humidity"
temperature_topic = "2f84be5e-8861-42dd-9392-a0d8e0795713-temperature"
socketio = SocketIO(app, cors_allowed_origins="*")
mqtt_client = Mqtt(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        mqtt_client.subscribe(humidity_topic)
        mqtt_client.subscribe(temperature_topic)
    else:
        print("Bad connection. Code:", rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    handle_message(message, socketio)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app)
