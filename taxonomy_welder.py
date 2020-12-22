#!/usr/bin/env python3

import csv
import random
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
  #ncbi_version = "accession date: {}".format(day_month_year)

  # print versions
  print("Database versions:")
  print("SILVA - {}".format(silva_version))
  print("GTDB - {}".format(gtdb_version))
  #print("NCBI - {}\n".format(ncbi_version))


if __name__ == "__main__":

  welcome_message()

  database_versions()

  # step 1) import gtdb data
  df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim = gtdb.import_gtdb_to_ncbi_to_gg_to_silva_table()

  # step 2) import silva data
  df_silva_to_ncbi = silva.import_silva_to_ncbi_table()

  # step 3) write tables
  df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim.to_csv("df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim.tsv", index=False, sep='\t', header=True)
  df_silva_to_ncbi.to_csv("df_silva_to_ncbi.tsv", index=False, sep='\t', header=True)


  #print(df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim)
  #print(df_silva_to_ncbi)
