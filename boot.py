import utime
import connect2wifi as wifi
from umqtt.robust import MQTTClient  # more reliable
from machine import Pin, SoftI2C
import bme280

# MQTT Config
MQTT_BROKER = ''      # Raspberry pi IP
CLIENT_ID = '' 			  # Unique ID for your device
MQTT_TOPIC = ''       # MQTT topic to publish data

# Connect WiFi
wifi.do_connect()

# Sensor setup
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
sensor = bme280.BME280(i2c=i2c)

# Setup MQTT client with keepalive
client = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=30)
client.connect()
print("Connected to MQTT Broker")

# MQTT Discovery
def publish_discovery():
    temp_config_topic = 'homeassistant/sensor/esp32_temperature/config'
    temp_config_payload = '''{
      "name": "Room Temperature",
      "state_topic": "sensor/temperature",
      "unit_of_measurement": "°C",
      "value_template": "{{ value_json.temperature }}",
      "unique_id": "esp32_temp_sensor2",
      "device_class": "temperature"
    }'''
    client.publish(temp_config_topic, temp_config_payload, retain=True)

    hum_config_topic = 'homeassistant/sensor/esp32_humidity/config'
    hum_config_payload = '''{
      "name": "Room Humidity",
      "state_topic": "sensor/temperature",
      "unit_of_measurement": "%",
      "value_template": "{{ value_json.humidity }}",
      "unique_id": "esp32_hum_sensor2",
      "device_class": "humidity"
    }'''
    client.publish(hum_config_topic, hum_config_payload, retain=True)

publish_discovery()

# Main loop
while True:
    try:
        # Read sensor
        temp = float(sensor.temperature[:-2])
        hum = float(sensor.humidity[:-2])
        message = f'{{"temperature": {temp}, "humidity": {hum}}}'
        print("Publishing:", message)

        # Send to broker
        client.publish(MQTT_TOPIC, message, retain=True)

    except Exception as e:
        print("MQTT error:", e)
        try:
            client.disconnect()
        except:
            pass
        utime.sleep(5)
        client = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=30)
        client.connect()
        publish_discovery()

    utime.sleep(60)  # Leitura e postagem a cada 60s
