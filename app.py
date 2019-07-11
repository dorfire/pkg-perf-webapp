'''
Sample app that run `pip install` in various directories to measure package download performance.
'''
import os
from flask import Flask, Response


app = Flask(__name__)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
REQSET_DIR = os.path.join(APP_DIR, 'reqsets')
REQSET_EXT = '.txt'


def isreqset(filename):
	return os.path.isfile(os.path.join(REQSET_DIR, filename)) and filename.endswith(REQSET_EXT)


@app.route('/')
def index():
	body = 'Navigate to /pipinstall/<reqset> to test download and installation times.\n\n'
	body += 'Possible requirement sets:\n'
	body += '\n'.join([' - ' + name for name in os.listdir(REQSET_DIR) if isreqset(name)])
	return Response(body, mimetype='text/plain')
