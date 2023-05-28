#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

#define DHTPIN 22
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// WiFi
const char *ssid = "Rares S20";       // Enter your WiFi name
const char *password = "coadaluilee"; // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "test.mosquitto.org";
const char *humidity_topic = "cd906955-d4ab-4db7-b281-54f1043e32e2-humidity";
const char *temperature_topic = "2f84be5e-8861-42dd-9392-a0d8e0795713-temperature";
const char *mqtt_username = "";
const char *mqtt_password = "";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(mqtt_broker, mqtt_port, espClient);

void setup()
{
    // Set software serial baud to 115200;
    Serial.begin(115200);
    dht.begin();
    // connecting to a WiFi network
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.println("Connecting to WiFi..");
    }
    Serial.print("Connected to the WiFi network");
    Serial.println(WiFi.localIP());
    // connecting to a mqtt broker
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);
    while (!client.connected())
    {
        String client_id = "esp32-client-";
        client_id += String(WiFi.macAddress());
        Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
        if (client.connect(client_id.c_str(), mqtt_username, mqtt_password))
        {
            Serial.println("Public emqx mqtt broker connected");
        }
        else
        {
            Serial.print("failed with state ");
            Serial.print(client.state());
            delay(2000);
        }
    }
    // publish and subscribe
//    client.publish(topic, "Hi EMQX I'm ESP32 ^^");
//    client.subscribe(topic);
}

void callback(char *topic, byte *payload, unsigned int length)
{
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    for (int i = 0; i < length; i++)
    {
        Serial.print((char)payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");
}

void loop()
{
//    client.loop();
    float hum = dht.readHumidity();
    float temp = dht.readTemperature();
    Serial.println(hum);
    Serial.println(temp);
    
    if (!isnan(hum) && !isnan(temp)) {
      char message[10];
      sprintf(message, "%02f", hum);
      client.publish(humidity_topic, message);

      sprintf(message, "%02f", temp);
      client.publish(temperature_topic, message);
    }
    delay(1000);
}
