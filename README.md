# CERBERUS-WIFI v3.0

## WiFi Deauth & Device Control Framework

Advanced WiFi security testing framework for device discovery and access control assessment.

## Features

- WiFi device discovery and tracking
- MAC address vendor identification
- Device type detection (iPhone, Android, Windows, Mac, Linux, IoT, etc.)
- Access point detection and monitoring
- Deauthentication attack (kick devices off network)
- Device banning with continuous deauth
- DNS and DHCP hostname tracking
- Real-time device monitoring
- Channel hopping for full coverage

## Installation

```bash
cd CERBERUS-WIFI
pip install -r requirements.txt
sudo python3 cerberus_wifi.py -i wlan0
