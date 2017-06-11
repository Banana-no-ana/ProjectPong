"""
This script runs the bitters application using a development server.
"""

from os import environ
from pong import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '62379'))
    except ValueError:
        PORT = 62379
    #app.debug = True
    app.run(HOST, PORT)
