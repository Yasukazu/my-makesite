# Open local terminal's localhost:8080 if running in VS Code terminal of remote host
"""python bottle-test.py 
Bottle v0.12.25 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.

127.0.0.1 - - [24/Dec/2023 07:47:45] "GET / HTTP/1.1" 200 26"""
from bottle import route, run

@route('/')
def myhome():

    return "<h1>It's my home page</h1>"

run(host='localhost', port=8080)