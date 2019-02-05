from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import MySQLdb
import time
import json

#                        server       MySQL username	MySQL pass  Database name.
#conn = MySQLdb.connect("mysql.server", "beginneraccount", "cookies", "beginneraccount$tutorial")

#c = conn.cursor()

# consumer key, consumer secret, access token, access secret.


ckey = "YyUi54vOJ5GsfQbVvxAeSiL35"
csecret = "ODSZaNg4OGqXYYjSBaMiwqDKhKrHsDaLrctaxqm2n754PpAndM"
atoken = "527831126-2j4HHl57mrhVErE4o9EqKAG4EmYzYPIDXQjvPArg"
asecret = "BulKS8mipUEifCTEw96MzsoI429S7i49SDUK2AIi3hydc"


class listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)
        dictfilt = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])

        # print all_data
        if ('coordinates' in all_data) and (all_data['coordinates'] != None) :
            print all_data['coordinates']

            want_keys = ('text', 'timestamp_ms', 'coordinates', 'user', 'entities')
            wanted_data = dictfilt(all_data, want_keys)
            # print str(wanted_data)
            with open('data.json', 'a') as tf:
                json.dump(wanted_data, tf)
        return True

    def on_error(self, status):
        print status


GEOBOX_WORLD = [-180,-90,180,90]

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(locations = GEOBOX_WORLD)