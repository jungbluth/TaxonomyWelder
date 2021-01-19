#!/usr/bin/env python3

import csv
import random
import sys
import argparse
from argparse import RawTextHelpFormatter
from lib import gtdb, silva
import datetime

# increase the field limit count for tables
csv.field_size_limit(10000000000)

def welcome_message():
  print("\ntaxonomy_welder: a toolkit for cross-linking taxonomic ontologies")
  print("by: Sean Jungbluth (sjungbluth@lbl.gov)\n")


def database_versions():

  # produce date stamp for NCBI database acccession date
  now = datetime.datetime.now()
  year = '{:02d}'.format(now.year)
  month = '{:02d}'.format(now.month)
  day = '{:02d}'.format(now.day)
  hour = '{:02d}'.format(now.hour)
  minute = '{:02d}'.format(now.minute)
  day_month_year = '{}-{}-{}'.format(year, month, day)

  # declare versions
  silva_version = 138
  gtdb_version = 95
  ncbi_version = "accession date: {}".format(day_month_year)
  img_version = "accession date: 2021-01-19"

  # print versions
  print("Database versions:")
  print("SILVA - {}".format(silva_version))
  print("GTDB - {}".format(gtdb_version))
  print("IMG - {}".format(img_version))
  print("NCBI - {}\n".format(ncbi_version))

def arg_parser():
  parser = argparse.ArgumentParser(prog='taxonomy_welder',usage='%(prog)s.py --dl_gtdb [y/n] --dl_silva [y/n] --help --version', description="""
  taxonomy_welder is a toolkit for query/parsing/merging NCBI/GTDB/SILVA taxonomies.
  """,formatter_class=RawTextHelpFormatter)
  parser.add_argument("--dl_gtdb", dest="dl_gtdb", default="n", help="""Download GTDB-based files. (default n)""")
  parser.add_argument("--dl_silva", dest="dl_silva", default="n", help="""Download SILVA-based files. (default n)""")
  parser.add_argument('--version', action='version', version='%(prog)s v0.0.1')
  args = parser.parse_args()
  if len(sys.argv) is None:
    parser.print_help()
  return args

if __name__ == "__main__":

  welcome_message()

  args = arg_parser()

  database_versions()

  if args.dl_gtdb is not 'n':
    print("Start: Downloading GTDB files")
    df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim = gtdb.import_gtdb_to_ncbi_to_gg_to_silva_table()
    df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim.to_csv("df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim.tsv", index=False, sep='\t', header=True)
    print("End: Downloading GTDB files")

  if args.dl_silva is not 'n':
    print("Start: Downloading SILVA files")
    df_silva_to_ncbi = silva.import_silva_to_ncbi_table()
    df_silva_to_ncbi.to_csv("df_silva_to_ncbi.tsv", index=False, sep='\t', header=True)
    print("End: Downloading SILVA files")
