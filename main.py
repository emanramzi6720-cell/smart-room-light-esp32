import network
import time
from machine import Pin, ADC
import dht
from umqtt.simple import MQTTClient

# ---------------- WIFI ----------------

SSID = "Wokwi-GUEST"
PASSWORD = ""

# ---------------- MQTT ----------------

BROKER = "broker.hivemq.com"
PORT = 1883

CLIENT_ID = "ESP32_ROOM"

TOPIC_DOOR = b"home/door"
TOPIC_MOTION = b"home/motion"
TOPIC_LED_CMD = b"home/led/cmd"
TOPIC_LED_STATE = b"home/led/state"
TOPIC_LIGHT = b"home/light"
TOPIC_TEMP = b"home/temperature"
TOPIC_HUM  = b"home/humidity"

# ---------------- PINS ----------------

DOOR_PIN = 12
PIR_PIN = 14
LED_PIN = 27

# ---------------- DEVICES ----------------

door = Pin(DOOR_PIN, Pin.IN, Pin.PULL_UP)

pir = Pin(PIR_PIN, Pin.IN)

led = Pin(LED_PIN, Pin.OUT)

auto_mode = True

# ---------------- LDR ----------------

LDR_PIN = 34

ldr = ADC(Pin(LDR_PIN))
ldr.atten(ADC.ATTN_11DB)
ldr.width(ADC.WIDTH_12BIT)

# ---------------- DHT22 ----------------

DHT_PIN = 15

dht_sensor = dht.DHT22(Pin(DHT_PIN))

# ---------------- WIFI ----------------

def wifi_connect():

    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)

    if not wlan.isconnected():

        print("Connecting WiFi...")

        wlan.connect(SSID, PASSWORD)

        while not wlan.isconnected():

            time.sleep(0.5)

    print("Connected")
    print(wlan.ifconfig())


# ---------------- LED ----------------

def set_led(state):

    led.value(state)

    client.publish(
        TOPIC_LED_STATE,
        b"ON" if state else b"OFF",
        retain=True
    )

    print("LED =", "ON" if state else "OFF")


# ---------------- MQTT CALLBACK ----------------

def mqtt_callback(topic, msg):

    global auto_mode

    print(topic, msg)

    if topic == TOPIC_LED_CMD:

        if msg == b"ON":

            auto_mode = False
            set_led(True)

        elif msg == b"OFF":

            auto_mode = False
            set_led(False)

        elif msg == b"AUTO":

            auto_mode = True


# ---------------- START ----------------

wifi_connect()

client = MQTTClient(CLIENT_ID, BROKER, PORT)

client.set_callback(mqtt_callback)

client.connect()

client.subscribe(TOPIC_LED_CMD)

print("MQTT Connected")

lastDoor = None
lastMotion = None
lastLight = None
lastTemp = None
lastHum = None
ledState = False

# ---------------- LOOP ----------------

while True:

    try:

        client.check_msg()

        # لأننا مستخدمين Pull-Up
        # المفتوح = 0

        doorOpened = (door.value() == 0)

        motion = (pir.value() == 1)

        light = ldr.read()

        dht_sensor.measure()

        temperature = dht_sensor.temperature()

        humidity = dht_sensor.humidity()

        print(
            "Door:", doorOpened,
            " Motion:", motion,
            " Light:", light,
            " Temp:", temperature,
            " Hum:", humidity,
            " Auto:", auto_mode
        )

        if doorOpened != lastDoor:

            client.publish(
                TOPIC_DOOR,
                b"OPEN" if doorOpened else b"CLOSED",
                retain=True
            )

            lastDoor = doorOpened

        if motion != lastMotion:

            client.publish(
                TOPIC_MOTION,
                b"DETECTED" if motion else b"CLEAR",
                retain=True
            )

            lastMotion = motion
        
        # -------- Publish Light --------

        if lastLight is None or abs(light - lastLight) > 50:

            client.publish(
                TOPIC_LIGHT,
                str(light)
            )

            lastLight = light

        # -------- Publish Temperature --------

        if temperature != lastTemp:

            client.publish(
                TOPIC_TEMP,
                str(temperature)
            )

            lastTemp = temperature


        # -------- Publish Humidity --------

        if humidity != lastHum:

                client.publish(
                    TOPIC_HUM,
                    str(humidity)
                )

                lastHum = humidity

        if auto_mode:

            dark = light > 2000

            newState = doorOpened and motion and dark

            if newState != ledState:

                set_led(newState)

                ledState = newState

        time.sleep(0.2)

    except Exception as e:

        print(e)

        time.sleep(2)