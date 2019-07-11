'''
Sample app that run `pip install` in various directories to measure package download performance.
'''
import os, subprocess, shutil
from os import path
from time import sleep
from flask import Flask, Response


app = Flask(__name__)
APP_DIR = path.dirname(path.abspath(__file__))
PIP_ROOT_DIR = '/tmp/pip'
REQSET_DIR = path.join(APP_DIR, 'reqsets')
REQSET_EXT = '.txt'

def res(body):
	return Response(body, mimetype='text/plain')


def isreqset(filename):
	return path.isfile(path.join(REQSET_DIR, filename)) and filename.endswith(REQSET_EXT)


def get_reqset_path(basename):
	return path.join(REQSET_DIR, basename + REQSET_EXT)


@app.route('/')
def index():
	body = 'Navigate to /pipinstall/<reqset> to test download and installation times.\n\n'
	body += 'Available requirement sets:\n'
	body += '\n'.join([' - ' + path.splitext(name)[0] for name in os.listdir(REQSET_DIR) if isreqset(name)])
	return res(body)

@app.route('/timeout/<int:secs>')
def test_timeout(secs):
	sleep(secs)
	return res('Slept')


def reset_dir(path):
	shutil.rmtree(path, ignore_errors=True)
	os.makedirs(path)


@app.route('/pipinstall/<reqset>')
def runpip(reqset):
	reset_dir(PIP_ROOT_DIR)
	reqs_path = get_reqset_path(reqset)
	pip_output = subprocess.check_output(['pip', 'install', '-r', reqs_path, '--root', PIP_ROOT_DIR])
	return res(pip_output)
