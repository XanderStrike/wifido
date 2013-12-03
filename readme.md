wifido
======

Wifido is a simple wifi sniffer built for Operating Systems. It uses a Sniffer, a Raspberry Pi attached to a golf cart which does the actual sniffing, and a Server, a machine with a static ip and an always on internet connection. The sniffer reports what it finds every night at 10pm via SCP to the server, and the server hosts a web interface that makes the data visible.

setup
-----

**server**

* Clone the repo
* Install sqlite3 (`apt-get install sqlite3`)
* CD to `server/db` and run `./dbsetup.sh`
* `cd ..`
* Run `python server.py` as a superuser

**sniffer**

* Clone the repo
* `apt-get install python python-gps mpg321`
* `pip install twython`
* CD to `sniffer/db` and run `./dbsetup.sh`
* `cd ..`
* Get or create auth.json in `sniffer/` with app_key, app_secret, oauth_token, and oauth_token_secret
* Run `python wifido.py` as a superuser

usage
-----

See the readmes for each folder to learn how to use them.
