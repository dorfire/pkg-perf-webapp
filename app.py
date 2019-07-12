'''
Sample app that run `pip install` in various directories to measure package download performance.
'''
import os, subprocess, shutil
from os import path
from time import sleep
from flask import Flask, Response


app = Flask(__name__) # Debug enabled through env var FLASK_DEBUG=1
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
	body += '\n'.join([' - ' + path.splitext(name)[0] for name in os.listdir(REQSET_DIR) if isreqset(name)]) + '\n\n'
	
	body += 'Environment:\n'
	body += ' - {} = "{}"\n'.format('FLASK_DEBUG', os.environ.get('FLASK_DEBUG'))
	body += ' - {} = "{}"\n'.format('APP_DIR', APP_DIR)
	body += ' - {} = "{}"\n'.format('REQSET_DIR', REQSET_DIR)
	
	return res(body)


@app.route('/sleep/<int:secs>')
def test_timeout(secs):
	sleep(secs)
	return res('Slept {} seconds'.format(secs))


def reset_dir(path):
	shutil.rmtree(path, ignore_errors=True)
	os.makedirs(path)


def run(cmd):
	return str(subprocess.check_output(['/bin/bash', '-c', cmd], stderr=subprocess.STDOUT, shell=False), 'utf-8')


@app.route('/pipinstall/<reqset>')
def time_pip(reqset):
	body = ''

	try:
		reset_dir(PIP_ROOT_DIR)
		body += 'Reset directory "{}"\n'.format(PIP_ROOT_DIR)
	except Exception as exc:
		body += 'Could not reset pip root directory "{}":\n{}\n'.format(PIP_ROOT_DIR, exc)

	try:
		reqs_path = get_reqset_path(reqset)
		body += run('time pip install -r {} --target {} --ignore-installed --no-cache-dir'.format(reqs_path, PIP_ROOT_DIR))
	except Exception as exc:
		body += 'Could not time pip:\n{}'.format(exc)

	return res(body)
