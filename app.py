'''
Sample app that run `pip install` in various directories to measure package download performance.
'''
import os, subprocess, shutil
from flask import Flask, Response


app = Flask(__name__)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PIP_ROOT_DIR = '/tmp/pip'
REQSET_DIR = os.path.join(APP_DIR, 'reqsets')
REQSET_EXT = '.txt'


def isreqset(filename):
	return os.path.isfile(os.path.join(REQSET_DIR, filename)) and filename.endswith(REQSET_EXT)


def get_reqset_path(basename):
	return os.path.join(REQSET_DIR, basename + REQSET_EXT)


@app.route('/')
def index():
	body = 'Navigate to /pipinstall/<reqset> to test download and installation times.\n\n'
	body += 'Possible requirement sets:\n'
	body += '\n'.join([' - ' + os.path.basename(name) for name in os.listdir(REQSET_DIR) if isreqset(name)])
	return Response(body, mimetype='text/plain')


def reset_dir(path):
	shutil.rmtree(path, ignore_errors=True)
	os.makedirs(path)


@app.route('/pipinstall/<reqset>')
def runpip(reqset):
	reset_dir(PIP_ROOT_DIR)
	reqs_path = get_reqset_path(reqset)
	pip_output = subprocess.check_output(['pip', 'install', '-r', reqs_path, '--root', PIP_ROOT_DIR])
	return Response(pip_output, mimetype='text/plain')
