server
------

This directory contains the scripts and libraries that will be used on the server side of things. This is the stationary pi that maintains the authoritative database, has a stable connection, and serves the web interface.

We will likely be using librarycounter for this.

api
---

These routes are part of the API, all data is returned in JSON form.

`/api/data` (method POST) - data to be committed to the database as the data attribute in JSON form. I.e. `curl --data "data=<json data here>" librarycounter:3030/api/data`

`/api/i/<start>/<end>/<mac>` - Interval api, returns all data ocurring between start and end times (unix integer time) with given mac address. Attributes may be left off the end of the query, `/api/i` returns all data, `/api/i/1379633831` returns all data from that time on, etc.