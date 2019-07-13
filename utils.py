import os, subprocess, shutil
from os import path
from flask import Response


REQSET_EXT = '.txt'

def res(body):
	return Response(body, mimetype='text/plain')


def isreqset(dirname: str, filename: str) -> bool:
	filepath = path.join(dirname, filename)
	return path.isdir(filepath) or (path.isfile(filepath) and filename.endswith(REQSET_EXT))


def get_reqset_path(dirname: str, basename: str):
	return path.join(dirname, basename + REQSET_EXT)


def get_available_reqsets(reqset_dir):
	return [path.splitext(name)[0] for name in os.listdir(reqset_dir) if isreqset(reqset_dir, name)]


def reset_dir(path):
	shutil.rmtree(path, ignore_errors=True)
	os.makedirs(path)


def run(cmd, workdir=None):
	return str(subprocess.check_output(['/bin/bash', '-c', cmd], stderr=subprocess.STDOUT, shell=False, cwd=workdir), 'utf-8')
