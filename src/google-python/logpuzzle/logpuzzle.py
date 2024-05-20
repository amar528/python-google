#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
import encodings.utf_8
# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
from urllib.error import HTTPError
from urllib.request import urlopen

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def extract_urls(file_text):
    url_regex = r'GET\s+(.+)\s+HTTP'
    matches = re.findall(url_regex, file_text)

    if matches:
        return matches
    else:
        print('Error: failed to extract URL data')
        sys.exit(1)


def sort_url(_url):
    #  Test to see if the URL matches the form word-word.
    #  If it does, sort by the second word. Otherwise, use the whole URL as the sort key
    second_part_regex = r'\w+-(\w+)[.]'
    _match = re.search(second_part_regex, _url)

    if _match:
        return _match.group(1)
    else:
        return _url


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    f = open(filename, 'rt', encoding='utf-8')
    file_text = f.read()
    f.close()
    extracted_urls = extract_urls(file_text)

    _idx = filename.index('_')
    _idx += 1
    _host = filename[_idx:]
    print(f'Host: {_host}')

    urls = []
    for _url in extracted_urls:
        item = 'http://' + _host + _url
        if item not in urls:
            urls.append(item)

    return sorted(urls, key=sort_url)


def add_to_index_html(dest_dir, local_names):
    f = open(os.path.join(dest_dir, 'index.html'), 'at', encoding='utf-8')

    f.write('<html><body>')

    for local_name in local_names:
        anchor_tag = f'<img src=\'{local_name}\'/>'
        f.write(anchor_tag)

    f.write('\n')
    f.write('</body></html>')

    f.flush()
    f.close()


def add_to_index_html(dest_dir, local_names):
    f = open(os.path.join(dest_dir, 'index.html'), 'at', encoding='utf-8')

    f.write('<html><body>')

    for local_name in local_names:
        anchor_tag = f'<img src=\'{local_name}\'/>'
        f.write(anchor_tag)

    f.write('\n')
    f.write('</body></html>')

    f.flush()
    f.close()


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    count = 0
    local_names = []

    #  TODO this is a good case for concurrency, rather than serial requests
    for _url in img_urls:
        try:
            suffix = _url[-4:]
            local_name = f'img{count}'
            if '.' in suffix:
                local_name += f'{suffix}'

            save_path = os.path.join(dest_dir, local_name)

            print(f'Downloading {_url} ...')
            path, headers = urllib.request.urlretrieve(_url, save_path)
            print(f'... saved to {save_path}')

            #  images are supported, otherwise we'll delete the file
            # TODO it would be better to perform a HEAD here and perform this assertion prior to downloading
            if headers.get_content_type() in ['image/jpeg', 'image/png', 'image/gif']:
                local_names.append(local_name)
                count += 1
            else:
                os.remove(save_path)

        except HTTPError as err:
            print(f'Error retrieving {_url} : {err}')
        count += 1

    add_to_index_html(dest_dir, local_names)


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
