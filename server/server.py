#server.py
# Serves information for the api and the web page

from lib.bottle import hook, response, route, run, template, static_file, request
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
  return static_file("index.html", root='./static/')

# POST data api
@route('/api/data', method='POST')
def import_data():
  data = request.forms.get('data')
  objects = json.loads(data)
  cur = con.cursor()
  for row in objects:
    values = [
              str(row['time']),
              '"' + row['mac'] + '"',
              '"' + row['essid'] + '"',
              str(row['strength']),
              str(row['lat']),
              str(row['long']),
              str(row['alt'])
             ]
    cur.execute("insert into wifis values(" + ','.join(values) + ")")
  con.commit()
  return "success" 

# interval API, takes integer times for start and end, and a mac address
@route('/api/i')
@route('/api/i/:start')
@route('/api/i/:start/:end')
@route('/api/i/:start/:end/:mac')
def interval(start="0", end=str(time.time()), mac=''):
  cur = con.cursor()
  if (mac == ''):
    cur.execute("SELECT * FROM wifis WHERE time>" + start + " AND time<" + end)
  else:
    cur.execute("SELECT * FROM wifis WHERE time>" + start + " AND time<" + end + " AND mac=\"" + mac + "\"")
  return json.dumps(cur.fetchall())


# serve static files
@route('/static/:filename')
def static(filename):
  return static_file(filename, root='./static/')

run(host='0.0.0.0', port=3030)
