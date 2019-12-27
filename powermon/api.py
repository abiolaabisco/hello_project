import json
import urllib2

url = "http://api.powermonitoring.com/1/statues/user_timeline.json?screen_name=python"
data=json.load(urllib2.urlopen(url))
print data
