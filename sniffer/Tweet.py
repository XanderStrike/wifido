from twython import Twython
from datetime import date, datetime, timedelta

tweet_frequency = 87 # seconds
whitelist = ["Westmont_Encrypted", "Westmont_Open", ""]
last_tweeted = datetime.now()
last_rogue_essid = ""

def bark(essid, json_data):
    if (essid not in whitelist):
        global_ready = (datatime.now() - last_tweeted).total_seconds() >= tweet_frequency
        if (global_ready and last_rogue_essid != essid):
            last_tweeted = datetime.now()
            last_rogue_essid = essid
            twitter = Twython(json_data["app_key"], json_data["app_secret"], json_data["oauth_token"], json_data["oauth_token_secret"])
            twitter.update_status(status=text)
