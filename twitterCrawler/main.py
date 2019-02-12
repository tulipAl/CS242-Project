from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import MySQLdb
import time
import json
import sys

ckey = "YyUi54vOJ5GsfQbVvxAeSiL35"
csecret = "ODSZaNg4OGqXYYjSBaMiwqDKhKrHsDaLrctaxqm2n754PpAndM"
atoken = "527831126-2j4HHl57mrhVErE4o9EqKAG4EmYzYPIDXQjvPArg"
asecret = "BulKS8mipUEifCTEw96MzsoI429S7i49SDUK2AIi3hydc"


count = int(sys.argv[1])
out_file = sys.argv[2]
print sys.argv

class listener(StreamListener):
    i = 0
    def on_data(self, data):
        all_data = json.loads(data)
        dictfilt = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])

        # print all_data
        if ('coordinates' in all_data) and (all_data['coordinates'] != None) :
            print all_data['coordinates']

            want_keys = ('text', 'timestamp_ms', 'coordinates', 'user', 'entities')
            wanted_data = dictfilt(all_data, want_keys)

            if self.i == 0:
                with open(out_file, 'a') as f:
                    f.write("["+json.dumps(wanted_data, indent=2))
            elif self.i < count:
                with open(out_file, 'a') as f:
                    f.write("," + json.dumps(wanted_data, indent=2))
            else:
                with open(out_file, 'a') as f:
                    f.write("]")
                return False
            self.i += 1
        return True

    def on_error(self, status):
        print status


GEOBOX_WORLD = [-180,-90,180,90]

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(locations = GEOBOX_WORLD)


