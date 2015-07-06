#!/usr/bin/env python2.7
# usage: url_pinger.py [-h] [-t TIMEOUT] [-v] [-s SYS] [-e ENV] URL
#
# Utility to HTTP ping the given URL.
# e.g. url_pinger.py 'https://uk.news.yahoo.com/most-popular/'
#
# positional arguments:
#  URL                   URL to ping
#
# optional arguments:
#  -h, --help            show this help message and exit
#  -t TIMEOUT, --timeout TIMEOUT
#                        Request timeout in seconds (default: 8)
#  -v, --verbose         Increase output verbosity
#  -s SYS, --system SYS  Reference application (app1|app2|...|appN)
#  -e ENV, --environment ENV
#                        Reference environment (dev|prod|test)
#
# Versions:
# - 2.1/2015.04: Enable specific data-retrieval for specific systems/apps
#                e.g. NO of sessions for CAS status page
# - 2.0/2015.04: Add system & environment on the json return
# - 1.0/2015.04: Initial happy version
#
# TODOs:
# - return either json or "200 OK <response_time>"
#
from modules.commonlib import get_utc_time_in_ms
from modules.commonlib import warning_msg
from modules.commonlib import error_msg
from modules.commonlib import debug_msg
from modules.commonlib import info_msg
from modules.commonlib import silence_stderr

from modules.httpstatus import HttpStatus
from modules.connection import Connection

import argparse
from argparse import RawTextHelpFormatter
import os

timeout_default = 8   # Default timeout
system          = ""  # cas|app1|app2|...|appN
environment     = ""  # test|dev|prod


if __name__ == '__main__':

  # argparse
  program_description = "\
  HTTP-ping the given URL for the response-code and response-time.\n\
  The response-time is measured in Unix Epoch-time in milliseconds.\n\
  e.g. {} 'https://uk.news.yahoo.com/most-popular/'".format(os.path.basename(__file__))

  parser = argparse.ArgumentParser(description=program_description, formatter_class=RawTextHelpFormatter)
  parser.add_argument('url', type=str, metavar='URL',
                      help='URL to ping')

  parser.add_argument('-t', '--timeout', type=int, default=timeout_default,
                      help="Request timeout in seconds (default: {})".format(timeout_default))
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='Increase output verbosity')
  parser.add_argument('-s', '--system', type=str, metavar='SYS',
                      help='Reference application (cas|app1|app2|...|appN)')
  parser.add_argument('-e', '--environment', type=str, metavar='ENV',
                      help='Reference environment (dev|prod|test)')

  # Read arguments
  args = parser.parse_args()
  url = args.url
  timeout = args.timeout
  if args.system:
    system = args.system
  if args.environment:
    environment = args.environment

  # No verbosity by default
  if (not args.verbose):
    silence_stderr()

  debug_msg("Using TIMEOUT={} seconds{}".format(timeout, " (default)" if (timeout == timeout_default) else ""))
  debug_msg("Pinging URL '{}'...".format(url))

  if (system == 'cas'):
    conn = Connection(url, timeout, 'CASStatusPage')
  else:
    conn = Connection(url, timeout, 'HttpStatusOnly')

  response = conn.status()

  # Possibly append sys & env
  if system:
    response.set_sys(system)
  if environment:
    response.set_env(environment)

  print response.to_json()
