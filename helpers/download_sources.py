#!/usr/bin/env python
"""
A simple script downloading sources from specfiles
"""
import os
import sys
import rpm
import optparse
import subprocess

parser = optparse.OptionParser()
parser.add_option('-d', '--directory', help='Target directory', default='/tmp/sources')

options, args = parser.parse_args()

if not os.path.isdir(options.directory):
    os.makedirs(options.directory)

for specfile in args:
    try:
        spec = rpm.spec(specfile)
    except ValueError as e:
        print(str(e))
    sources = spec.sources
    for source in sources:
        filename_or_url = source[0]
        if '://' not in filename_or_url:
            continue
        command = ('wget', '-q', '-P', options.directory, '-c', filename_or_url) 
        print(' '.join(command))
        subprocess.call(command)
