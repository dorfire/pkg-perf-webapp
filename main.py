'''
Sample app that run `pip install`/`npm install` in various directories,
to measure package download performance.
'''
from os import path
from time import sleep
from flask import Flask, request; app = Flask(__name__)
from utils import *


APP_DIR = path.dirname(path.abspath(__file__))
PIP_REQSET_DIR = path.join(APP_DIR, 'pip_reqsets')
NPM_REQSET_DIR = path.join(APP_DIR, 'npm_reqsets')


@app.route('/')
def index():
	body = 'Navigate to /pip-install/<reqset> or /npm-install/<reqset> to test download and installation times.\n\n\n'
	
	body += 'Available pip requirement sets:\n'
	body += '\n'.join([' - ' + name for name in get_available_reqsets(PIP_REQSET_DIR)]) + '\n\n'
	
	body += 'Available npm requirement sets:\n'
	body += '\n'.join([' - ' + name for name in get_available_reqsets(NPM_REQSET_DIR)]) + '\n\n\n'
	
	body += 'Environment:\n'
	body += ' - {} = "{}"\n'.format('APP_DIR', APP_DIR)
	body += ' - {} = "{}"\n'.format('FLASK_DEBUG', os.environ.get('FLASK_DEBUG'))
	body += ' - {} = "{}"\n'.format('TIMEFORMAT', os.environ.get('TIMEFORMAT'))
	body += ' - {} = "{}"\n'.format('PIP_REQSET_DIR', PIP_REQSET_DIR)
	body += ' - {} = "{}"\n'.format('NPM_REQSET_DIR', NPM_REQSET_DIR)
	
	return res(body)


@app.route('/sleep/<int:secs>')
def test_timeout(secs):
	sleep(secs)
	return res('Slept {} seconds'.format(secs))


@app.route('/pip-install/<reqset>')
def time_pip(reqset):
	body = ''

	app_path = path.join(PIP_REQSET_DIR, reqset)
	pip_prefix = path.join(app_path, 'pip')

	if request.args.get('reset') == 'true':
		reset_dir(pip_prefix)
		body += 'Directory "{}" was reset\n'.format(pip_prefix)

	reqs_path = path.join(app_path, 'requirements.txt')
	pip_install_cmd = 'time pip install -r {} --target {} {}'.format(
		reqs_path, pip_prefix, '--ignore-installed --no-cache-dir' if request.args.get('nocache') == 'true' else '')
	body += run(pip_install_cmd).output

	return res(body)


@app.route('/npm-install/<reqset>')
def time_npm(reqset):
	body = ''

	# Install npm if needed
	if run('which npm').returncode != 0:
		install_npm_cmd = 'curl -sL https://deb.nodesource.com/setup_10.x | bash - && apt-get install -y nodejs'
		body += '{}:\n'.format(install_npm_cmd)
		body += run(install_npm_cmd).output + '\n\n'

	app_path = path.join(NPM_REQSET_DIR, reqset)
	node_modules_path = path.join(app_path, 'node_modules')

	if request.args.get('reset') == 'true':
		reset_dir(node_modules_path)
		body += 'Directory "{}" was reset\n'.format(node_modules_path)

	body += run('time npm install', app_path).output
	return res(body)


if __name__ == '__main__':
	app.run()
