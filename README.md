# url_pinger

URL-pinger is a handy tool to get the http-response status and/or code from a URL.

## Example

~~~
$ ./url_pinger.py 'https://uk.news.yahoo.com/most-popular/'
{"http_response": 200, "http_response_description": "OK", "http_response_time": 795, "timestamp": 1436200470098}
~~~
The response-time is in milliseconds, while the timestamp is in [Unix Epoch Time](https://en.wikipedia.org/wiki/Unix_time) in milliseconds.

## Error-Codes

An error is reflected to an http-response-like error-code, under the `http_response` key/field as below:

- 408: DNS resolution error
- 410: Request timeout

## TODOs

Features & changes to possibly implement in the future:

- Add support for plain http protocol.
- Use one argument for all extra JSON fields, instead of `--system` & `--environment`.

Or maybe not...
