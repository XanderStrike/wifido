#server.py
# Serves information for the api and the web page

from lib.bottle import hook, response, route, run, template, static_file
import sqlite3 as lite
import sys
import time
import json

con = lite.connect('db/data.sqlite3')

# allow any origin, reqired for API
@hook('after_request')
def enable_cors():
  response.headers['Access-Control-Allow-Origin'] = '*'

@route('/')
def hello():
  return "Hello world!"

# serve static files
@route('/static/:filename')
def static(filename):
  return static_file(filename, root='./static/')

run(host='0.0.0.0', port=3030)
