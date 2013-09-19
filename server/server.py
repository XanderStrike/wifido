#server.py
# Serves information for the api and the web page

from lib.bottle import hook, response, route, run, template, static_file
import sqlite3 as lite
import sys
import time
import json

@route('/')
def hello():
  return "Hello world!"

run(host='0.0.0.0', port=3030)
