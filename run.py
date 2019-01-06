#!/usr/bin/python3

"""
Whenever I set up a new machine with linux, there is some basic config stuff I always have to do: some config changing, repository adding, package installing, ect ect. Hopefully this script will provide a way to do this which is both convenient and configurable

"""


import os
import sys
import subprocess



newlinux_header = "===== start newlinux additions ====="
newlinux_footer = "===== end newlinux additions ====="

package_install_prefix = {
	'apt': 'sudo apt install -yqq',
	'pacman': 'sudo pacman -S',
}

extra_packages = [
	'tree',
	'git',
	'vim',
]

# Will run first, in order of the list
# Shouldn't be moving anything from the resources directory here, unless there is a need to move something early in the process
run_these_first = [
	'mkdir ~/bin',
]


# Something in the resources folder which should be copied to the host system
class Resource:
	def __init__(self, resource_name, destination, default_mode, is_text_file=False, comment_type=''):
		self.resource_name = resource_name
		self.resource_path = os.path.join('./resources/', self.resource_name)
		self.destination = destination
		if default_mode not in ('copy', 'addition', 'append'):
			raise ValueError("Unrecognized default_mode in Resource constructor: \"" + default_mode + "\"")
		self.default_mode = default_mode
		self.is_text_file = is_text_file
		# comment_type is only relevant if we are using additions
		self.comment_type = comment_type

resources = [
	Resource("vimrc.txt", "~/.vimrc", "copy", is_text_file=True, comment_type='\"'),
	Resource("bashrc.txt", "~/.bashrc", "copy", is_text_file=True, comment_type='#'),
]


def main():
	## Set up config ##
	package_manager_input = input("What is your package manager?  ")
	try:
		pm_prefix = package_install_prefix[package_manager_input]
	except KeyError:
		print("Don't know that package manager :(")
		sys.exit(1)
	use_additions_input = input("Use \'newlinux\' addition sections? (y/n, default n)  ")
	use_additions = use_additions_input in ('y', 'yes', 'Y', 'Yes', 'YES')

	# todo: a more interactive menu: can configure mode for each resource. Starts with default mode
	mode = input("Which mode for copying resources? (copy, add, append)  ");
	if mode not in ('copy', 'add', 'append'):
		print("Don't recognize that mode")
		sys.exit(2)


	
	print("\nInstalling extra packages:")
	for package in extra_packages:
		os.system(pm_prefix + ' ' + package)

	print("\nCopying resources:")
	for r in resources:
		if use_additions and r.is_text_file:
			insert_additions(r.resource_path, r.destination, comment_type=r.comment_type)
		elif mode == 'copy':
			os.system('cp ' + r.resource_path + ' ' + r.destination)
		elif mode == 'append':
			os.system('cat ' + r.resource_path + ' >> ' + r.destination)

	#for file_addition in file_additions:
	#	insert_additions(file_addition[0], file_addition[1], comment_type=file_addition[2])


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
def insert_additions(old_file_path, additions_file_path, comment_type=''):
	if not os.path.exists(additions_file_path):
		print("ERROR: insert_additions given bad additions file: {0}".format(additions_file_path))
		return

	header = comment_type + newlinux_header
	footer = comment_type + newlinux_footer
	
	additions_file = open(additions_file_path)
	additions = additions_file.read()
	additions_file.close()

	# create new_contents
	if os.path.exists(old_file_path):
		old_file = open(old_file_path, 'r')
		# We will have problems if the file is to big. Rework this if necessary
		new_contents = old_file.read()
		old_file.close()

		header_index = new_contents.find(header)
		if header_index == -1:
			# Header was not in the file, so append it
			new_contents += '\n\n' + newlinux_header + '\n' + additions + '\n' + newlinux_footer + '\n\n'
		else:
			# again, not sure if this will work with very long files
			footer_index = new_contents.find(footer)
			if footer_index == -1:
				print("ERROR: found header but not footer")
				return
			elif footer_index < header_index:
				print("ERROR: found footer.. before header? exiting??")
				return

			print("Found newlinux section at {0}:{1}".format(header_index, footer_index))
			new_contents = new_contents[:header_index] + header + '\n' + additions + '\n' + footer + new_contents[footer_index+len(footer):]

	else: #old_file does not exist
		new_contents = '\n' + header + '\n' + additions + '\n' + footer

	if os.path.exists(old_file_path):
		os.rename(old_file_path, old_file_path + '.old')
	new_file = open(old_file_path, 'w')
	new_file.write(new_contents)
	new_file.close()
	



if __name__ == '__main__':
	main()

