#!/usr/bin/env python3

import pandas as pd

# might use at some point to validate results
def import_validation_files():

  # paths to data
  gtdb_to_ncbi_archaea = "https://data.ace.uq.edu.au/public/gtdb/data/releases/release95/95.0/auxillary_files/gtdb_vs_ncbi_r95_archaea.xlsx"
  gtdb_to_ncbi_bacteria = "https://data.ace.uq.edu.au/public/gtdb/data/releases/release95/95.0/auxillary_files/gtdb_vs_ncbi_r95_bacteria.xlsx"

  # import as pandas dataframe
  df_gtdb_to_ncbi_archaea = pd.DataFrame(pd.read_excel(gtdb_to_ncbi_archaea)) 
  df_gtdb_to_ncbi_bacteria = pd.DataFrame(pd.read_excel(gtdb_to_ncbi_bacteria)) 

  return df_gtdb_to_ncbi_archaea, df_gtdb_to_ncbi_bacteria 


def import_gtdb_to_ncbi_table():

  # paths to data
  gtdb_to_ncbi_archaea = "https://data.ace.uq.edu.au/public/gtdb/data/releases/release95/95.0/ar122_taxonomy_r95.tsv.gz"
  gtdb_to_ncbi_bacteria = "https://data.ace.uq.edu.au/public/gtdb/data/releases/release95/95.0/bac120_taxonomy_r95.tsv.gz"

  # import as pandas dataframe
  df_gtdb_to_ncbi_archaea = pd.DataFrame(pd.read_csv(gtdb_to_ncbi_archaea, sep='\t', header = None)) 
  df_gtdb_to_ncbi_bacteria = pd.DataFrame(pd.read_csv(gtdb_to_ncbi_bacteria, sep='\t', header = None)) 

  # concatenate dataframes
  df_gtdb_to_ncbi_archaea_plus_bacteria = pd.concat([df_gtdb_to_ncbi_archaea, df_gtdb_to_ncbi_bacteria])

  # rename columns
  df_gtdb_to_ncbi_archaea_plus_bacteria = df_gtdb_to_ncbi_archaea_plus_bacteria.rename(columns={0: "NCBI_Assembly_ID", 1: "GTDB_R95_Taxonomy"})

  return df_gtdb_to_ncbi_archaea_plus_bacteria


def add_refseq_or_genbank_column(df_gtdb_to_ncbi_archaea_plus_bacteria):

  # add column to indicate if data from refseq or genbank
  df_gtdb_to_ncbi_archaea_plus_bacteria["RefSeq_or_GenBank"] = df_gtdb_to_ncbi_archaea_plus_bacteria["NCBI_Assembly_ID"].map(lambda x: x[:2])

  # add column with clean version of NCBI Assembly ID
  df_gtdb_to_ncbi_archaea_plus_bacteria["Clean_NCBI_Assembly_ID"] = df_gtdb_to_ncbi_archaea_plus_bacteria["NCBI_Assembly_ID"].map(lambda x: x[3:])

  return df_gtdb_to_ncbi_archaea_plus_bacteria