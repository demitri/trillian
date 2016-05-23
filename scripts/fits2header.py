#!/usr/bin/env python

"""

This script requires Python 3.2+.
Ref: http://stackoverflow.com/questions/12517451/python-automatically-creating-directories-with-file-output
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import re
import os
import sys
import json
import gzip
import fnmatch
import argparse
from trillian.utlities import extract_FITS_header

parser = argparse.ArgumentParser(description="A script to extract headers from FITS files.")
parser.add_argument("-d", "--directory",
					help="root directory to search for FITS files",
					dest="source_directory",
					default=".")
parser.add_argument("-r", "--recursive",
					help="search source directory recursively",
					action="store_true")
parser.add_argument("-o", "--output",
					help="output directory",
					dest="output_directory",
					default=".")
parser.add_argument("-z", "--gzip",
					help="include '.gz' FITS files if found",
					dest="gzip",
					default=True)
parser.add_argument("-c", "--compress",
					help="gzip output files (individually)",
					dest="compress",
					action="store_true")

args = parser.parse_args()

source_dir = args.source_directory
#if args.output_directory is None:
#	output_dir = "."
#else:
output_dir = args.output_directory

def is_fits_file(filepath, allow_gz=False):
	'''
	Check if this is a FITS file. Not robust - only checks for extension.
	'''
	if re.search(r'\.fits$', filepath, re.IGNORECASE) or re.search(r'\.fts$', filepath, re.IGNORECASE):
		return True
	if allow_gz and (re.search(r'\.fits$', filepath, re.IGNORECASE) or re.search(r'\.fts$', filepathx, re.IGNORECASE)):
		return True
	return False
	
if args.recursive:
	for root, subdirs, files in os.walk(source_dir):
		# root: current path
		# subdirs: list of directories in current path
		# files: list of files in current path
		
		relative_directory = root.lstrip(source_dir)
		
		for filename in files:
			if is_fits_file(filename) == False:
				continue
				
			d = extract_FITS_header(os.path.join(root, filename))
			
			output_file = os.path.join(output_dir, relative_directory, filename.rstrip(".gz")+".thdr")
			
			# create directories if needed
			os.makedirs(os.path.dirname(output_file), exist_ok=True)
			
			if (args.compress):
				with gzip.open(output_file+".gz", "wb") as out:
					out.write(bytes(json.dumps(d), 'UTF-8'))
			else:
				with open(output_file, 'w') as out:
					out.write(json.dumps(d))

else:
	for filename in os.listdir(source_dir):
		if is_fits_file(filename) == False:
			continue
			
		d = extract_FITS_header(os.path.join(source_dir, filename))
		
		output_file = os.path.join(output_dir, filename.rstrip(".gz")+".thdr")
		
		if (args.compress):
			with gzip.open(output_file, "wb") as out:
				out.write(bytes(json.dumps(d), 'UTF-8'))
		else:
			with open(output_file, 'w') as out:
				out.write(json.dumps(d))


