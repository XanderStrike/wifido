wifido
======

Wifi quality sniffer for Westmont College.

Purpose
=======

Overall Goal
------------

* Create heat map of the campus
* Identify WAP Locations
* Identify sources of interferance?

**Detailed**

* Input Requirements
* Output Requirements
* Displays

Hardware
--------

* Raspberry Pi
  * Librarycounter
  * db & web interface
  * wifido
* Power sources
  * Golf cart batteries
  * DC-DC voltage regulator
  * Power output splitter RPi/GPS
* Bluetooth
  * dongle
* Wireless
* GPS
  * Dual xgps 150A
* Enclosure
  * Inside roof?
* Speakers?

Software
--------

* OS
  * Raspbian
* System Drivers
  * GPSD
  * bluez?
  * ntp
* User-executable software
* API
* Outside data sources
* Internal Data Sources

Responsibilities/Assignments
----------------------------

**Alex** - Lirarycounter Upload API

**Lewis** - iwlist script

**Nolan** - Google maps heat map API

**Adam** - gpsd to xgpsd, lat, lon, altitude, speed, direction

**Danial** - Data digestion & transmission

**Johnny** - LED/Sound output, (cricket)

Open Questions
--------------

When to send data?

* when cart is stopped and connected to charger
* at night?
* regular intervals
* when new AP detected

Data Representation

* store in sqlite3
* transfer in JSON

Acquisition speed

* Function of cart's speed 
