#!/bin/bash

sqlite3 db.sqlite3 'create table wifis(time integer, mac text, essid text, strength real, lat real, long real, alt real);'
