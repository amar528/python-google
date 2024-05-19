#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""


def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    # +++your code here+++
    output = []
    f = open(filename, 'rt', encoding='utf-8')
    text = f.read()

    year_match = extract_year(text)
    if year_match:
        output.append(year_match.group(1))

    rank_name_tuples = []
    for rank_and_name_tuple in extract_ranks_and_names(text):
        rank_name_tuples.append((rank_and_name_tuple[0], rank_and_name_tuple[1]))
        rank_name_tuples.append((rank_and_name_tuple[0], rank_and_name_tuple[2]))

    sorted_rank_name_tuples = sorted(rank_name_tuples, key=extract_name)

    for rank_and_name_tuple in sorted_rank_name_tuples:
        output.append(' ')
        output.append(rank_and_name_tuple[0])
        output.append(' ')
        output.append(rank_and_name_tuple[1])

    return output


def extract_year(text):
    #  <h2>Popularity in 2008</h2>
    year_regex = r'Popularity in (\d+)'
    return re.search(year_regex, text)


def extract_ranks_and_names(text):
    #  <tr align="right"><td>2</td><td>Michael</td><td>Isabella</td>
    # </tr>
    names_and_ranks_regex = r'<tr align="right"><td>(\d+)<\/td><td>(\w+)<\/td><td>(\w+)<\/td>'

    return re.findall(names_and_ranks_regex, text)


def extract_name(rank_name_tuple):
    return rank_name_tuple[1]


def write_summary(summary_filename, name_data):
    f = open(summary_filename, 'at', encoding='utf-8')
    f.writelines(name_data)
    f.write('\n')
    f.close()


def clear_summary_file(summary_filename):
    f = open(summary_filename, 'wt', encoding='utf-8')
    f.close()


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    summary_filename = ""
    if args[0] == '--summaryfile':
        summary = True
        del args[0]
        summary_filename = args[0]
        del args[0]
        clear_summary_file(summary_filename)

    # +++your code here+++
    # For each filename, get the names, then either print the text output
    # or write it to a summary file

    for file_name in args:
        name_data = extract_names(file_name)
        if summary:
            write_summary(summary_filename, name_data)
        else:
            print(name_data)
            print('')


if __name__ == '__main__':
    main()
