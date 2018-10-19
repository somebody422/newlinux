#!/usr/bin/python3

import os, os.path
import sys

python_symlink_path = '/usr/bin/python'
python2_symlink_path = '/usr/bin/python2'
python3_symlink_path = '/usr/bin/python3'

if not ( os.path.exists(python2_symlink_path) and os.path.exists(python3_symlink_path) ):
	print("Error: cannot find python2 and python3")
	sys.exit(-1)

if not os.path.exists(python_symlink_path):
	print("Cannot find existing python symlink")

current_python = os.readlink(python_symlink_path)

if os.path.basename(current_python) == 'python3':
	new_python = python2_symlink_path
elif os.path.basename(current_python) == 'python2':
	new_python = python3_symlink_path
else:
	print("Error: current python symlink pointing to unknown location")
	sys.exit(-1)

os.remove(python_symlink_path)
os.symlink(new_python, python_symlink_path)