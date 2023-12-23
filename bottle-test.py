from bottle import route, run

@route('/')
def myhome():

    return "It's my home page"

run(host='localhost', port=8008)