#!/usr/bin/python3

"""
Whenever I set up a new machine with linux, there is some basic config stuff I always have to do: some config changing, repository adding, package installing, ect ect. Hopefully this script will provide a way to do this which is both convenient and configurable

"""


import os
import sys
import subprocess


newlinux_header = "#!#!# start newlinux additions #!#!#"
newlinux_footer = "#!#!# end newlinux additions #!#!#"

apt_add_additional_repositories = [

]

apt_install_packages = [
	'sudo apt-get install python',
	'sudo apt-get install tree',
]

file_additions = [
	(os.path.expanduser('~/.bashrc'), 'additions/bashrc_additions.txt'),
]

def main():
	#runCommands(apt_install_packages)
	#runCommand('mkdir ~/bin')
	#appendFile('./bashrc_additions.txt', '~/.bashrc')
	#insert_additions('./testfile', 'testfile_additions.txt')
	for file_addition in file_additions:
		insert_additions(file_addition[0], file_addition[1])


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
def appendFile(from_filepath, to_filepath):
	from_file = open(from_filepath, 'r')
	to_file = open(to_filepath, 'a')
	#to_file.write(os.linsep) # TODO: do i want this?
	for line in from_file:
		to_file.write(line)

# Create a 'newlinux' section at the end of target text file if it doesn't exist already. Copy the contents of the additions file into that section
# If a newlinux section already exists, this will replace its contents
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
		print("Couldn't find header. adding it at the end")
		# Header was not in the file, so we can just append on the additions
		old_file.close()
		old_file = open(old_file_path, 'a')
		old_file.write('\n\n'+newlinux_header+'\n')
		old_file.write(additions)
		old_file.write('\n'+newlinux_footer+'\n\n')
		old_file.close()
	else:
		footer_index = old_file_contents.find(newlinux_footer)
		if footer_index == -1:
			print("ERROR: Found header but not footer!")
			return
		elif footer_index < header_index:
			print("ERROR: Footer found before header??")
			return

		print("Found the newlinux section at {0}:{1}! Replacing contents..".format(header_index, footer_index))

		#print("Start of current header: \"{0}\"".format(old_file_contents[header_index:header_index+8]))
		#print("Start of section after footer: \"{0}\"".format(old_file_contents[footer_index+len(newlinux_footer):footer_index+len(newlinux_footer)+8]))
		# Header has been found starting at index header_index
		# Instead of trying to add to the middle of the file, just copy contents to a new one
		post_footer_index = footer_index+len(newlinux_footer)
		#todo: check for existing file?
		new_file = open(old_file_path + '.tmp', 'w')
		new_file.write(old_file_contents[:header_index])
		new_file.write(newlinux_header+'\n')
		new_file.write(additions)
		new_file.write('\n'+newlinux_footer)
		new_file.write(old_file_contents[post_footer_index:])
		new_file.close()
		runCommand('mv {0} {0}.old'.format(old_file_path))
		runCommand('mv {0}.tmp {0}'.format(old_file_path))

	

if __name__ == '__main__':
	main()
