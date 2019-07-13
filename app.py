'''
Sample app that run `pip install` in various directories to measure package download performance.
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
	body = 'Navigate to /pip-install/<reqset> or /npm-install/<reqset> to test download and installation times.\n\n'
	
	body += 'Available pip requirement sets:\n'
	body += '\n'.join([' - ' + name for name in get_available_reqsets(PIP_REQSET_DIR)]) + '\n\n'
	
	body += 'Available npm requirement sets:\n'
	body += '\n'.join([' - ' + name for name in get_available_reqsets(NPM_REQSET_DIR)]) + '\n\n'
	
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


def time_pkg_install(root_dir, reqset, cmd_fmt, workdir=None):
	body = ''

	prefix = path.join(root_dir, reqset)
	os.chdir(prefix)

	if request.args.get('reset') == 'true':
		reset_dir(prefix)
		body += 'Directory "{}" was reset\n'.format(prefix)

	try:
		reqs_path = get_reqset_path(reqset)
		body += run('time ' + cmd_fmt.format(reqs_path, prefix), workdir)
	except Exception as exc:
		body += 'Could not time installation:\n{}'.format(exc)

	return res(body)


@app.route('/pip-install/<reqset>')
def time_pip(reqset):
	return time_pkg_install(PIP_ROOT_DIR, reqset, 'pip install -r {} --target {} --ignore-installed --no-cache-dir')


@app.route('/npm-install/<reqset>')
def time_npm(reqset):

	return time_pkg_install(NPM_ROOT_DIR, reqset, 'pip install -r {} --target {} --ignore-installed --no-cache-dir', )


	prefix = path.join(PIP_ROOT_DIR, reqset)

	if request.args.get('reset') == 'true':
		reset_dir(prefix)
		body += 'Reset directory "{}"\n'.format(prefix)

	try:
		reqs_path = get_reqset_path(reqset)
		body += run('time pip install -r {} --target {} --ignore-installed --no-cache-dir'.format(reqs_path, prefix))
	except Exception as exc:
		body += 'Could not time pip:\n{}'.format(exc)

	return res(body)


if __name__ == '__main__':
	app.run()
