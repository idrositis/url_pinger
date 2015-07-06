#/usr/bin/env/python
#
# HttpStatus Class
#
import json

class HttpStatus(dict):
  def __init__(self, http_response, http_response_description, http_response_time, timestamp):
    # Custom
    self['http_response'] = int(http_response)
    self['http_response_description'] = http_response_description
    self['http_response_time'] = int(http_response_time)
    self['timestamp'] = long(timestamp)

  def to_json(self):
    return json.dumps(self, sort_keys=True)

  def set_sys(self, system):
    self['sys'] = system

  def set_env(self, env='prod'):
    self['env'] = env

  def set_sessions(self, session_number):
    self['sessions'] = int(session_number)

# Possibly use this to add key-values 
# http://stackoverflow.com/questions/1098549/proper-way-to-use-kwargs-in-python
#  def add_key_values(self, **kwargs):
#    for k in kwargs.keys():
#      self.__setattr__(k, kwargs[k])
