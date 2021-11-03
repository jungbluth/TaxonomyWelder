#!/usr/bin/env python3

import csv
import random
import sys
import argparse
from argparse import RawTextHelpFormatter
from lib import gtdb, silva, img, ncbi
import datetime

# notes:
# *) may not need to query NCBI directly because other ontologies all link to it

# increase the field limit count for tables
csv.field_size_limit(10000000000)

# declare versions
silva_version = 138
gtdb_version = 202
img_version = "accession date: 2021-10-27"
ncbi_version = "accession date: 2021-10-27"

def welcome_message():
  print("\nTaxonomyWelder: a toolkit for cross-linking taxonomic ontologies")
  print("by: Sean Jungbluth (sjungbluth@lbl.gov) and the DOE Systems Biology KnowledgeBase (KBase) Team\n")

def database_versions(silva_version, gtdb_version, img_version, ncbi_version):

  # print versions
  print("Current database versions and sources:")
  print("IMG - {}".format(img_version))
  print("NCBI - {}".format(ncbi_version))
  print("GTDB - v{}".format(gtdb_version))
  print("SILVA - v{}".format(silva_version))

def arg_parser():
  parser = argparse.ArgumentParser(prog='TaxonomyWelder',usage='%(prog)s.py --dl_gtdb [y/n] --dl_silva [y/n] --help --version', description="""
  TaxonomyWelder: a toolkit for cross-linking taxonomic ontologies.
  by: Sean Jungbluth (sjungbluth@lbl.gov) and the DOE Systems Biology KnowledgeBase (KBase) Team.
  """,formatter_class=RawTextHelpFormatter)
  parser.add_argument("--dl_img", dest="dl_img", default="n", help="""Download current IMG-based files. (default n)""")
  parser.add_argument("--dl_ncbi", dest="dl_ncbi", default="n", help="""Download current NCBI-based files. (default n)""")
  parser.add_argument("--dl_gtdb", dest="dl_gtdb", default="n", help="""Download current GTDB-based files. (default n)""")
  parser.add_argument("--dl_silva", dest="dl_silva", default="n", help="""Download current SILVA-based files. (default n)""")
  parser.add_argument("--dl_legacy_silva", dest="dl_legacy_silva", default="n", help="""Download legacy SILVA-based files. (default n)""")
  parser.add_argument("--legacy_silva_version", dest="legacy_silva_version", default="132", help="""Legacy SILVA version to use (must be >=132). (default 132)""")
  parser.add_argument('--version', action='version', version='%(prog)s v0.0.1')
  args = parser.parse_args()
  if len(sys.argv) is None:
    parser.print_help()
  return args

if __name__ == "__main__":

  args = arg_parser()

  welcome_message()

  database_versions(silva_version, gtdb_version, img_version, ncbi_version)

  # unique use cases require legacy silva (e.g. MGnify currently uses SILVA v132)
  legacy_silva_version = args.legacy_silva_version

  if args.dl_img is not 'n':
    print("\nStart: Loading cached IMG files")
    df_img_to_ncbi = img.import_img_to_ncbi_table()
    df_img_to_ncbi.to_csv("IMG__img_to_ncbi.tsv", index=False, sep='\t', header=True)
    print("End: Loading cached IMG files")

  if args.dl_ncbi is not 'n':
    print("\nStart: Loading cached NCBI files")
    df_ncbi = ncbi.import_ncbi_table()
    df_ncbi.to_csv("NCBI__ncbi_full_taxonomy.tsv", index=False, sep='\t', header=True)
    print("End: Loading cached NCBI files")

  if args.dl_gtdb is not 'n':
    print("\nStart: Downloading current GTDB files")
    df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim = gtdb.import_gtdb_to_ncbi_to_gg_to_silva_table()
    df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim.to_csv("GTDB__gtdb_to_ncbi_to_silva_to_gg.tsv", index=False, sep='\t', header=True)
    print("End: Downloading GTDB files")

  if args.dl_silva is not 'n':
    print("\nStart: Downloading current SILVA files")
    df_silva_to_ncbi = silva.import_silva_to_ncbi_table(silva_version)
    df_silva_to_ncbi.to_csv("SILVA__slv{}_to_ncbi.tsv".format(silva_version), index=False, sep='\t', header=True)
    print("End: Downloading current SILVA files")

  if args.dl_legacy_silva is not 'n':
    print("\nStart: Downloading legacy (v{}) SILVA files".format(legacy_silva_version))
    df_silva_to_ncbi = silva.import_silva_to_ncbi_table(legacy_silva_version)
    df_silva_to_ncbi.to_csv("SILVA__slv{}_to_ncbi.tsv".format(legacy_silva_version), index=False, sep='\t', header=True)
    print("End: Downloading legacy (v{}) SILVA files".format(legacy_silva_version))

  if args.dl_silva is not 'n' and args.dl_legacy_silva is not 'n':
    print("\nStart: Merging current and legacy (v{}) SILVA files".format(legacy_silva_version))
    silva_merged = silva.merge_current_and_legacy_silva(silva_version, legacy_silva_version)
    silva_merged.to_csv("SILVA__slv{}_slv{}_to_ncbi.tsv".format(silva_version,legacy_silva_version), index=False, sep='\t', header=True)
    print("End: Merging current and legacy (v{}) SILVA files".format(legacy_silva_version))
