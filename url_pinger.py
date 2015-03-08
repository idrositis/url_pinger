#!/usr/bin/env python
# URL pinger
# syntax: url_pinger.py <hostname> <path> <timeout>
#   e.g.: url_pinger.py uk.news.yahoo.com /most-popular/ 8
#
# References:
# - Check HTTPS support
#   http://stackoverflow.com/questions/2146383/https-connection-python
#
# TODOs:
# - create a connection class/object
#   e.g. url_to_test = new connection(url, timeout)
#   Connection object should use the appropriate http/https library call
#
# - add command-line arguments
#   e.g. url_pinger.py -u|--url 'https://example.url.com/some/path/index.html'
#                    [ -t|--timeout <connection_timeout> ]
#
import httplib
import sys

try:
  import ssl
except ImportError:
  print "[ERROR] No SSL support!"
  exit(10)

def check_connection():
  hostname = sys.argv[1]
  path = sys.argv[2]
  timeout = float(sys.argv[3])
  conn = httplib.HTTPSConnection(hostname, timeout=timeout)
  conn.request("HEAD", path)
#  conn = httplib.HTTPSConnection("uk.news.yahoo.com", timeout=8)
#  conn.request("HEAD", "/most-popular/")
  res = conn.getresponse()

  # Print Status
  # 200 OK
  print res.status, res.reason

  # Print Headers
  #print res.getheaders()
  return

if __name__ == '__main__': 
  check_connection()
