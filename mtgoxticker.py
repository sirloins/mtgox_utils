#!/usr/bin/env python
# 
import os
import json
import sys
import time
import traceback
import urllib2

FULLTICKER = True     # If False then display only the weighted average price

class _BitcoinTicker():
  """ Retrieve ticker data (json format) from mtgox.com and convert it to plain html.
      The resulting ticker is similar to the one displayed on the Mt. Gox
      main page.
  """
  def main(self):
    try:
      print 'Content-type: text/html\n'
      handle = urllib2.urlopen('https://mtgox.com/api/1/BTCUSD/ticker')
      data = json.load(handle)
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
        spacer = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        if FULLTICKER:
          print 'Last price:%s%s High:%s%s Low:%s%s Volume:%s BTC%s Weighted Avg:%s USD'  % (
              last['display_short']
            , spacer
            , high['display_short']
            , spacer
            , low['display_short']
            , spacer
            , vol_display
            , spacer
            , vwap['display_short']
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
  app.main()