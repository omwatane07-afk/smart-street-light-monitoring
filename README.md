\# 🚦 Smart Street Light Monitoring System



\*\*ASEP Project\*\* - Arduino IoT street light controller with live Python dashboard.



\## ✨ Features

\- \*\*LDR sensor\*\*: Day/Night detection  

\- \*\*8 IR sensors\*\*: Traffic detection (Sensor 0-7)

\- \*\*8 LEDs\*\*: Street lights (auto ON/OFF based on traffic + time)

\- \*\*Python Tkinter UI\*\*: Real-time monitoring dashboard

\- \*\*Serial logging\*\*: All data saved to `monitoring.txt`



\## 📁 Project Structure

firmware/testcode.ino # Arduino firmware

ui/UpdatedMonitoringUI-1.py # Live dashboard

data/monitoring\_sample.txt # Sample logs



text



\## 🚀 Quick Setup

Arduino IDE → firmware/testcode.ino → Upload



pip install pyserial



python ui/UpdatedMonitoringUI-1.py



text



\### Hardware Connections

LDR → Pin 12

IR Sensors → A0,A1,A2,A3,A4,A5,10,11

LEDs → Pins 2,3,4,5,6,7,8,9



text



\## 📡 Serial Protocol

LDR:DAY/NIGHT

IR\_STATE:0:1 # Sensor 0 detected

LED:3:ON # Light 3 ON



text



\## 📊 Sample Logs

2026-01-17 085604.384542 LDR:DAY

2026-01-17 085605.070952 IR\_STATE:0:1

2026-01-17 085627.536695 LED:0:ON

