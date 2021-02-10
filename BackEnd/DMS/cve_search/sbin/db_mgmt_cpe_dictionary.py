#!/usr/bin/env python3
#
# Import script of nvd cpe (Common Platform Enumeration) definition
# into a collection used for human readable lookup of product name.
#
# Imported in cvedb in the collection named cpe.
#
# The format of the collection is the following
#
# { "_id" : ObjectId("50a2739eae24ac2274eae7c0"), "id" :
# "cpe:/a:1024cms:1024_cms:0.7", "title" : "1024cms.org 1024 CMS 0.7" }
#
# Software is free software released under the "GNU Affero General Public License v3.0"
#
# Copyright (c) 2012 		Wim Remes
# Copyright (c) 2012-2018  Alexandre Dulaunoy - a@foo.be
# Copyright (c) 2014-2018  Pieter-Jan Moreels - pieterjan.moreels@gmail.com

# Imports
import argparse
import os
import sys

runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

from lib.Sources_process import CPEDownloads
from lib.DatabaseLayer import getSize

# parse command line arguments
argparser = argparse.ArgumentParser(
    description="populate/update the local CPE database"
)
argparser.add_argument("-u", action="store_true", help="update the database")
argparser.add_argument("-p", action="store_true", help="populate the database")
argparser.add_argument(
    "-a", action="store_true", default=False, help="force populating the CPE database"
)
argparser.add_argument(
    "-f", action="store_true", default=False, help="force update of the CPE database"
)
argparser.add_argument("-v", action="store_true", help="verbose output")
args = argparser.parse_args()


if __name__ == "__main__":
    cpd = CPEDownloads()
    cpd.logger.debug("{}".format(" ".join(sys.argv)))

    if args.u:

        last_modified = cpd.update()

    elif args.p:
        c = getSize(cpd.feed_type.lower())
        if args.v:
            cpd.logger.info(str(c))
        if c > 0 and args.a is False:
            cpd.logger.info("Database already populated")
        else:
            last_modified = cpd.populate()