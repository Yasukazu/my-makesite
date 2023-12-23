# Open local terminal's localhost:8080 if running in VS Code terminal of remote host
from bottle import route, run

@route('/')
def myhome():

    return "<h1>It's my home page</h1>"

run(host='localhost', port=8080)