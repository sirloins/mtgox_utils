#!/usr/bin/env python
# 
import os
import json
import sys
import time
import traceback
from urllib import urlencode
import urllib2
from hashlib import sha512
from hmac import HMAC
import base64

FULLTICKER = True     # If False then display only the weighted average price
auth_key = 'YOUR.AUTH.KEY.FROM.MTGOX'
auth_secret = 'YOUR.AUTH.SECRET.FROM.MTGOX'

def get_nonce():
    return int(time.time()*100000)
 
def sign_data(secret, data):
    return base64.b64encode(str(HMAC(secret, data, sha512).digest()))
 
class requester:
    def __init__(self, auth_key, auth_secret):
        self.auth_key = auth_key
        self.auth_secret = base64.b64decode(auth_secret)
 
    def build_query(self, req={}):
        req["nonce"] = get_nonce()
        post_data = urlencode(req)
        headers = {}
        headers["User-Agent"] = "GoxApi"
        headers["Rest-Key"] = self.auth_key
        headers["Rest-Sign"] = sign_data(self.auth_secret, post_data)
        return (post_data, headers)
 
    def perform(self, path, args):
        data, headers = self.build_query(args)
        req = urllib2.Request("https://mtgox.com/api/1/"+path, data, headers)
        res = urllib2.urlopen(req, data)
        return json.load(res)

class _BitcoinTicker():
  """ Retrieve ticker data (json format) from mtgox.com and convert it to plain html.
      The resulting ticker is similar to the one displayed on the Mt. Gox
      main page.
  """
  def main(self, auth_key, auth_secret):
    try:
      print 'Content-type: text/html\n'
      reqr = requester(auth_key, auth_secret)
      args = {}
      data = reqr.perform('BTCUSD/ticker', args)
      if data['result'] == 'success':
        last = data['return']['last']
        high = data['return']['high']
        low = data['return']['low']
        vol = data['return']['vol']
        vwap = data['return']['vwap']
        # display only the integer portion of the volume number
        volparts = vol['display_short'].split('.')
        vol_display = vol['display_short']
        if len(volparts) > 1:
          vol_display = volparts[0]
        spacer = '&nbsp;&nbsp;&nbsp;&nbsp;'
        if FULLTICKER:
          print 'Last %s%s High %s%s Low %s%s Volume %s BTC%s Weighted Avg %s USD'  % (
              last['display_short'].replace('$','')
            , spacer
            , high['display_short'].replace('$','')
            , spacer
            , low['display_short'].replace('$','')
            , spacer
            , vol_display
            , spacer
            , vwap['display_short'].replace('$','')
          )
        else:
          print '1.00 BTC = %s %s (Weighted Average) as of %s %s' % (vwap['display_short'], vwap['currency'], time.strftime('%Y.%m.%d %H:%M:%S'), time.tzname)
      else:
        print '<font size=+2 color=#ff0000>%s</font>' % data['result']
    except:
      excName, excArgs, excTb = self.formatExceptionInfo()
      print 'Problem connecting to mtgox.com (%s). Please try again.' % excName    

  def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
      excArgs = exc.__dict__["args"]
    except KeyError:
      excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)

if __name__ == '__main__':
  app = _BitcoinTicker()
  app.main(auth_key, auth_secret)
