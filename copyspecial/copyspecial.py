#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""


# +++your code here+++
# Write functions and modify main() to call them

def get_special_paths(start_dir):
    output_paths = []

    #  special filename is __w__ where w is a word
    file_names = os.listdir(start_dir)

    file_regex = r'__(\w+)__'
    for file_name in file_names:
        if re.search(file_regex, file_name):
            print('Match {0}'.format(file_name))
            output_paths.append(os.path.abspath(file_name))
        else:
            print('No Match {0}'.format(file_name))

    return output_paths


def to_dir(to_directory_name, matching_files):
    if not os.path.exists(to_directory_name):
        print('Creating directory ' + to_directory_name)
        os.mkdir(to_directory_name)

    for file_to_copy in matching_files:
        shutil.copy(file_to_copy, to_directory_name)
        print(f'Copied {file_to_copy} to {to_directory_name}')


def to_zip(dest_zip_filename, matching_files):
    print(f'Zipping files {matching_files} to zip file {dest_zip_filename}')

    file_names = []
    for matching_file in matching_files:
        file_names.append(os.path.basename(matching_file))

    command_files = ''
    for command_file in file_names:
        command_files += command_file
        command_files += ' '

    command_to_execute = f'tar -cvzf {dest_zip_filename} {command_files}'
    print(f'Command to execute: {command_to_execute}')

    (status, output) = subprocess.getstatusoutput(command_to_execute)
    if status:  ## Error case, print the command's output to stderr and exit
        sys.stderr.write(output)
        sys.exit(status)
    print(output)  ## Otherwise do something with the command's output


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print('usage: [--todir dir][--tozip zipfile] dir [dir ...]')
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if not args:  # A zero length array evaluates to "False".
        print('error: must specify one or more dirs')
        sys.exit(1)

    # +++your code here+++
    # Call your functions
    matching_files = get_and_check_files(args)

    if todir:
        to_dir(todir, matching_files)
    elif tozip:
        to_zip(tozip, matching_files)
    else:
        print_files(matching_files)


def print_files(matching_files):
    print('Matches:')
    for matching in matching_files:
        print(matching)


def get_and_check_files(args):
    matching_files = []
    for directory in args:
        matches_for_directory = get_special_paths(directory)
        if len(set(matching_files).intersection(matches_for_directory)) > 0:
            print('Error: duplicate filenames found')
            sys.exit(-1)

        matching_files.extend(matches_for_directory)
    return matching_files


if __name__ == '__main__':
    main()
