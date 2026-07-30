# Smart Room Light Control (ESP32)

An energy-saving IoT project that automatically controls a room's light based on real conditions: door status, motion, and ambient light level.

Built as a graduation project for the **IoT Training at NTI (National Telecommunication Institute)**.

## How It Works

The light turns **ON** only when all three conditions are true at the same time:
1. Door is **open**
2. Motion is **detected** (PIR sensor)
3. Room is **dark** (LDR light sensor)

All sensor states are published over **MQTT** in real time, and a **Node-RED** dashboard allows live monitoring plus manual override (ON / OFF / AUTO).

## Hardware

| Component | Pin |
|---|---|
| ESP32 Board | — |
| Door Switch | GPIO 12 |
| PIR Motion Sensor | GPIO 14 |
| LED / Relay (Light) | GPIO 27 |
| LDR (Light Sensor) | GPIO 34 |
| DHT22 (Temperature & Humidity) | GPIO 15 |

## Tech Stack

- ESP32 (MicroPython)
- MQTT (HiveMQ public broker)
- Node-RED (dashboard + control)

## Files

- `main.py` — MicroPython code for the ESP32
- `diagram.json` — Wokwi wiring diagram
- `wokwi-project.txt` — Wokwi project reference

## Try It Live

Run the simulation directly in your browser (no hardware needed):
🔗 https://wokwi.com/projects/470887190300809217

## Demo

📹 Watch the demo video: [https://drive.google.com/drive/folders/1w8aDpwH1bfOUDaJhla3SZpZnf0tyz1MZ?usp=sharing]

## MQTT Topics

| Topic | Direction | Values |
|---|---|---|
| `home/door` | ESP32 → Node-RED | OPEN / CLOSED |
| `home/motion` | ESP32 → Node-RED | DETECTED / CLEAR |
| `home/light` | ESP32 → Node-RED | light level (number) |
| `home/temperature` | ESP32 → Node-RED | temperature |
| `home/humidity` | ESP32 → Node-RED | humidity |
| `home/led/state` | ESP32 → Node-RED | ON / OFF |
| `home/led/cmd` | Node-RED → ESP32 | ON / OFF / AUTO |
