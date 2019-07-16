import os, subprocess, shutil
from os import path
from flask import Response
from typing import NamedTuple


DEFAULT_OUTPUT_ENCODING = 'utf-8'
REQSET_EXT = '.txt'


def res(content, status=None):
	return Response(content, status=status, mimetype='text/plain')


def get_available_reqsets(reqset_dir):
	return [path.splitext(name)[0] for name in os.listdir(reqset_dir) if path.isdir(path.join(reqset_dir, name))]


def reset_dir(path):
	shutil.rmtree(path, ignore_errors=True)
	os.makedirs(path)


class RunResult(NamedTuple):
	returncode: int
	output: str


def run(cmd, workdir=None):
	try:
		output = subprocess.check_output(['/bin/bash', '-c', cmd], stderr=subprocess.STDOUT, shell=False, cwd=workdir)
		return RunResult(0, str(output, DEFAULT_OUTPUT_ENCODING))
	except subprocess.CalledProcessError as exc:
		try:
			return RunResult(exc.returncode, str(exc.output, DEFAULT_OUTPUT_ENCODING))
		except:
			return RunResult(None, None)


def cmd_exists(cmd):
	return run('which ' + cmd).returncode == 0
