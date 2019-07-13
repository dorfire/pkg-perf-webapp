import os, subprocess, shutil
from os import path
from flask import Response


REQSET_EXT = '.txt'

def res(body):
	return Response(body, mimetype='text/plain')


def get_available_reqsets(reqset_dir):
	return [path.splitext(name)[0] for name in os.listdir(reqset_dir) if path.isdir(path.join(reqset_dir, name))]


def reset_dir(path):
	shutil.rmtree(path, ignore_errors=True)
	os.makedirs(path)


def run(cmd, workdir=None):
	return str(subprocess.check_output(['/bin/bash', '-c', cmd], stderr=subprocess.STDOUT, shell=False, cwd=workdir), 'utf-8')
