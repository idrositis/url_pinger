#!/usr/bin/env python2.7
#
# Connection wrapper class
#
# Versions:
# - 1.0/2015.06: Initial version
#
# Status Codes:
# - 408: Name or service not known
# - 409: scheme/protocol not supported
# - 410: unexpected error
#
# References:
# - Check HTTPS support
#   http://stackoverflow.com/questions/2146383/https-connection-python
#
# TODOs:
#
from commonlib import get_utc_time_in_ms
from commonlib import warning_msg
from commonlib import error_msg
from commonlib import debug_msg
from commonlib import info_msg
from commonlib import silence_stderr

from httpstatus import HttpStatus

import httplib
import os	# os.linesep
from urlparse import urlparse   # urllib.parse in Python3

try:
  import ssl
except ImportError:
  error_msg("No SSL support on this system!")
  exit(10)

timeout_default = 8


# For known connection types we can get more info
# e.g. no of sessions for CAS status pages
#class ConnectionDataType(Enum):
#  'HttpStatusOnly' = 1
#  'CASStatusPage'  = 2


class Connection():
  def __init__(self, url, timeout=timeout_default, data_type='HttpStatusOnly'):
    self.url       = str(url)
    self.timeout   = float(timeout)
    self.data_type = str(data_type)

    parsed_url = urlparse(url)

    self.scheme = parsed_url.scheme
    self.netloc = parsed_url.netloc
    self.path   = parsed_url.path
    debug_msg("scheme={}, netloc={}, path={}".format(self.scheme, self.netloc, self.path))


  def status(self):
    # START
    mseconds_before = get_utc_time_in_ms()

    # Default response parameters
    response_status = 410
    response_reason = "unexpected error"
    response_time   = 0
    response_timestamp = mseconds_before

    # Check for supported scheme
    if (self.scheme != 'https'):
      response_status = 409
      response_reason = "scheme/protocol %s not supported" % scheme
      debug_msg("%s: %s" %(type(e).__name__, response_reason) )

      # END
      response_time = get_utc_time_in_ms() - mseconds_before

      status = HttpStatus(response_status,
                          response_reason,
                          response_time,
                          mseconds_before)

    # Real connection
    try:
      conn = httplib.HTTPSConnection(self.netloc, timeout=self.timeout)
      conn.request("GET", self.path)
      res = conn.getresponse()

      # END
      response_time = get_utc_time_in_ms() - mseconds_before

      # Print Status
      debug_msg("res.status={}, res.reason={}, response_time={} mseconds, timestamp={}".format(res.status, res.reason, response_time, mseconds_before))

      response_status = res.status
      response_reason = res.reason

      status = HttpStatus(response_status,
                          response_reason,
                          response_time,
                          mseconds_before)


      # Possibly get some more data per application
      if (self.data_type == 'CASStatusPage'):
        # CAS Status page contains
        data = res.read()	# data: str
        data_lines = data.split(os.linesep)
        sessions_and_tickets = [int(s) for s in data_lines[4].split() if s.isdigit()]
        status.set_sessions(sessions_and_tickets[0])


    except Exception, e:
      # END
      response_time = get_utc_time_in_ms() - mseconds_before

      if ( type(e).__name__ == "gaierror" ):
        # Name or service not known
        response_status = 408

      response_reason = "%s" % str(e)

      debug_msg("%s: %s" %(type(e).__name__, response_reason) )

      status = HttpStatus(response_status,
                          response_reason,
                          response_time,
                          mseconds_before)

    return status
