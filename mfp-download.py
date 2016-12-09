#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Michał "czesiek" Czyżewski <czesiek@hackerspace.pl>
#
# Distributed under terms of the MIT license.

"""
Downloads all tracks from musicforprogramming.net
"""

import inflect
import urllib2
from bs4 import BeautifulSoup
import os

# via https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def download_file(file_name, download_url):
    download_block_size = 8192

    download_handle = urllib2.urlopen(download_url)
    download_info = download_handle.info()
    file_size = int(download_info.getheaders("Content-Length")[0])
    file_size_downloaded = 0

    file_handle = open(file_name, "wb")
    while True:
        buf = download_handle.read(download_block_size)
        if not buf:
            break
        file_size_downloaded += len(buf)
        file_handle.write(buf)
        percent_downloaded = "{:.2%}".format(file_size_downloaded * 1.0 / file_size)
        status = "{:>7} ({})".format(percent_downloaded, sizeof_fmt(file_size_downloaded))
        status = "{:<30}".format(status) + chr(13)  # chr(13) is CR
        print status,
    file_handle.close()

    print("Download of {} complete ({} total)".format(file_name, sizeof_fmt(file_size)))

def main():
    no_episodes = 38
    base_url = "http://musicforprogramming.net/?"

    p = inflect.engine()
    for i in range(1, no_episodes+1):
        words = p.number_to_words(i).replace("-", "")
        url = base_url + words

        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "lxml")
        audio_url = soup.find(id="player")['src']
        file_name = audio_url.split("/")[-1]

        if os.path.isfile(file_name):
            print("({}/{}) {} is already here".format(i, no_episodes, file_name))
            continue

        print("({}/{}) Downloading {}\n → {}".format(i, no_episodes, audio_url, file_name))
        download_file(file_name, audio_url)

if __name__ == "__main__":
    main()
