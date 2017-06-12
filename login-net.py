#Import urlencode() in this package to encode post data
import urllib
import time
#Import http relevant functions
from urllib2 import Request, urlopen, URLError, HTTPError
username = 'your username'
password = 'your password'
data ={'action':'login','username':username,'password':password,'ac_id':'1','user_ip':'','nas_ip':'','user_mac':'','save_me':'1','ajax':'1'}
data = urllib.urlencode(data)
try:
    while (true):
        print "connecting..."
    	req = Request("http://10.6.8.2:901/include/auth_action.php")
    	response = urlopen(req,data, timeout = 10)
    	content = response.read()
    	response.close()
    	time.sleep(30)
except URLError, e:
    if hasattr(e, 'reason'):
        info = '[ERROR] Failed to reach the server.\nReason: ' + str(e.reason)
    elif hasattr(e, 'code'):
        info = '[ERROR] The server couldn\'t fullfill the request.\nError code: ' +str(e.code)