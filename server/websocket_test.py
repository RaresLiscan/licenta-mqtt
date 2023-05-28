from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
from flask_mqtt import Mqtt

thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config["SECRET_KEY"] = "donsky!"
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
humidity_topic = "cd906955-d4ab-4db7-b281-54f1043e32e2-humidity"
temperature_topic = "2f84be5e-8861-42dd-9392-a0d8e0795713-temperature"
socketio = SocketIO(app, cors_allowed_origins="*")

latest_temperature_data = 0
latest_humidtity_data = 0

mqtt_client = Mqtt(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        mqtt_client.subscribe(humidity_topic)  # subscribe topic
        mqtt_client.subscribe(temperature_topic)
    else:
        print("Bad connection. Code:", rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(topic=message.topic, payload=message.payload.decode())
    mqtt_latest_data = message.payload.decode()
    print("received mqtt data: " + mqtt_latest_data)

    if message.topic == humidity_topic:
        latest_humidtity_data = mqtt_latest_data
        socketio.emit(
            "updateHumidity",
            {"value": latest_humidtity_data, "date": get_current_datetime()},
        )
    elif message.topic == temperature_topic:
        latest_temperature_data = mqtt_latest_data
        socketio.emit(
            "updateTemperature",
            {"value": latest_temperature_data, "date": get_current_datetime()},
        )
    print("Received message on topic: {topic} with payload: {payload}".format(**data))


def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")


def background_thread():
    print("Generating random sensor values")
    while True:
        socketio.sleep(1)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def connect():
    global thread
    print("Client connected")

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


"""
Decorator for disconnect
"""


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected", request.sid)


if __name__ == "__main__":
    socketio.run(app)
