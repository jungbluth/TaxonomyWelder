#!/usr/bin/env python3

import csv
import random
from lib import gtdb, ncbi, silva

# increase the field limit count for tables
csv.field_size_limit(10000000000)

def welcome_message():
  print("\ntaxonomy_welder: a toolkit for cross-linking taxonomic ontologies")
  print("by: Sean Jungbluth\n")

def database_versions():

  # declare versions
  silva_version = 138
  gtdb_version = 95
  ncbi_version = "placeholder"

  # print versions
  print("Database versions:")
  print("SILVA: {}".format(silva_version))
  print("GTDB: {}".format(gtdb_version))
  print("NCBI: {}\n".format(ncbi_version))

if __name__ == "__main__":
  
  welcome_message()
  
  database_versions()

  # step 1) import gtdb data
  df_gtdb_to_ncbi_archaea_plus_bacteria = gtdb.import_gtdb_to_ncbi_table()

  # step 2) clean gtdb data
  df_gtdb_to_ncbi_archaea_plus_bacteria = gtdb.add_refseq_or_genbank_column(df_gtdb_to_ncbi_archaea_plus_bacteria)

  # step 3) extract list of Assembly IDs from gtdb_to_ncbi table
  assembly_id_list = df_gtdb_to_ncbi_archaea_plus_bacteria["Clean_NCBI_Assembly_ID"].tolist()

  random.shuffle(assembly_id_list)
  assembly_id_list = assembly_id_list[:20]

  # step 4) link GTDB Assembly IDs to NCBI TaxIDs
  ncbi.fetch_taxonomy_name_from_assembly_id(assembly_id_list, size=20)

  # step A) import silva data
  #df_silva_to_ncbi = silva.import_silva_to_ncbi_table()

  #print(assembly_id_list)
