from utils.date_utils import get_current_datetime
from database.measurements import add_data

humidity_topic = "cd906955-d4ab-4db7-b281-54f1043e32e2-humidity"
temperature_topic = "2f84be5e-8861-42dd-9392-a0d8e0795713-temperature"

DEFAULT_HUMIDITY = -200
DEFAULT_TEMPERATURE = -200

latest_humidtity_data = DEFAULT_HUMIDITY
latest_temperature_data = DEFAULT_TEMPERATURE

def handle_message(message, socketio):
    mqtt_latest_data = message.payload.decode()

    global latest_humidtity_data
    global latest_temperature_data

    if (message.topic == humidity_topic):
        latest_humidtity_data = mqtt_latest_data
        socketio.emit(
            "updateHumidity",
            {"value": latest_humidtity_data, "date": get_current_datetime()},
        )
    elif (message.topic == temperature_topic):
        latest_temperature_data = mqtt_latest_data
        
        socketio.emit(
            "updateTemperature",
            {"value": latest_temperature_data, "date": get_current_datetime()},
        )

    if ((latest_humidtity_data != DEFAULT_HUMIDITY) and (latest_temperature_data != DEFAULT_TEMPERATURE)):
        add_data(latest_humidtity_data, latest_temperature_data)
        print("called")
        latest_temperature_data = DEFAULT_TEMPERATURE
        latest_humidtity_data = DEFAULT_TEMPERATURE
        
    