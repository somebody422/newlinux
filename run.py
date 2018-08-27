#!/usr/bin/python

"""
Whenever I set up a new machine with linux, there is some basic config stuff I always have to do: some config changing, repository adding, package installing, ect ect. Hopefully this script will provide a way to do this which is both convenient and configurable

"""


import os
import sys
import subprocess


apt_add_additional_repositories = [

]

apt_install_packages = [
	'sudo apt-get install python',
	'sudo apt-get install tree'
]

def main():
	runCommands(apt_install_packages)



def runCommands(commands, exit_on_fail=False):
	for command in commands:
		exit_code = runCommand(command)
		if exit_on_fail and exit_code != 0:
			return

# Runs the given text as a command, then returns the error code
def runCommand(args):
	completed_process = subprocess.run(args.split())
	return completed_process.returncode

# Copy all text from one file to another
def appendFile(from_file, to_file):
	pass


if __name__ == '__main__':
	main()
