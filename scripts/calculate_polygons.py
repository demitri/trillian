#!/usr/bin/env python

'''
This script finds FITS files in the database and calculates their polygon on the sky,
saving the result back to the database.
'''

import sys
import argparse

import sqlalchemy
from sqlalchemy import func

from trillian.database.connections import LocalhostConnection as db
from trillian.database.connections import RemoteTunnelConnection as db
from trillian.database.trilliandb.FileModelClasses import FitsHDU
from trillian.database.trilliandb.TrillianModelClasses import Footprint

def processFilesWithoutPolygons(count=400):
	'''
	This function goes to the database, get 'count' images that don't have polygons, and calculates them.
	'''
	db.engine.dispose() # close all connections for a multiprocessing environment
	session = db.Session()
	
	image_hdus = session.query(FitsHDU)\
						.outerjoin(Footprint)\
						.filter(Footprint.sky_polygon==None)\
						.limit(count)\
						.all()
	raise Exception("")
	
	for image in images:
		
		raise Exception("")
		sys.exit(1)
	

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="A script to extract headers from FITS files.")
	parser.add_argument("-s", "--source",
					dest="source",
					help="Trillian short name identifier for this data source",
					default=None,
					required=True)

	# Print help if no arguments are provided
	#if len(sys.argv) < 2:
	#	parser.print_help()
	#	parser.exit(1)

	args = parser.parse_args()

	processFilesWithoutPolygons(count=10)
	


# Set up session
session = db.Session()



#session.commit()
db.engine.dispose()
sys.exit(0)
