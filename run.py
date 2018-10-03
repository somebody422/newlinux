#!/usr/bin/python3

"""
Whenever I set up a new machine with linux, there is some basic config stuff I always have to do: some config changing, repository adding, package installing, ect ect. Hopefully this script will provide a way to do this which is both convenient and configurable

"""


import os
import sys
import subprocess


newlinux_header = "#!#!# start newlinux additions #!#!#\n"
newlinux_footer = "#!#!# end newlinux additions #!#!#\n"

apt_add_additional_repositories = [

]

apt_install_packages = [
	'sudo apt-get install python',
	'sudo apt-get install tree'
]

def main():
	runCommands(apt_install_packages)

	runCommand('mkdir ~/bin')

        appendFile('./bashrc_additions.txt', '~/.bashrc')



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


def insert_additions(old_file_path, additions_file_path):
	if not os.path.exists(old_file_path):
		print("ERROR: insert_additions given bad old file: {0}".format(old_file_path))
		return
	elif not os.path.exists(additions_file_path):
		print("ERROR: insert_additions given bad additions file: {0}".format(additions_file_path))
		return
	
	additions_file = open(additions_file_path)
	additions = additions_file.read()
	additions_file.close()

	old_file = open(old_file_path, 'r')
	# Okay, if the file is too big we will have problems. Rework this if necessary..
	old_file_contents = old_file.read()
	header_index = old_file_contents.find(newlinux_header)
	if header_index == -1:
		# Header was not in the file, so we can just append on the additions
		old_file.close()
		old_file = open(oldfile_path, 'a')
		old_file.write(newlinux_header)
		old_file.write(additions)
		old_file.write(newlinux_footer)
		old_file.close()
	else
		# Header has been found starting at index header_index
		# Instead of trying to add to the middle of the file, just copy contents to a new one
		new_file = open(old_file_path + '.tmp', 'w')
		new_file.append(
	

if __name__ == '__main__':
	main()
