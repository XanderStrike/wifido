from twython import Twython

def update_status(new_status, app_key, app_secret, oauth_token, oauth_token_secret):
    twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
    twitter.update_status(status=new_status)
