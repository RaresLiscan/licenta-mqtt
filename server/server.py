from flask import Flask, render_template, request
from flask_socketio import SocketIO

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
