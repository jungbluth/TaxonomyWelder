#!/usr/bin/env python3

import pandas as pd

# gtdb tables provided online generated using online scripts
# info: https://gtdb.ecogenomic.org/tools
# *) https://github.com/nick-youngblut/gtdb_to_taxdump
# *) https://github.com/pirovc/genome_updater
# *) https://github.com/rrwick/Metagenomics-Index-Correction/blob/master/tax_from_gtdb.py

def import_gtdb_to_ncbi_to_gg_to_silva_table():

  # paths to data
  gtdb_to_ncbi_to_gg_silva_archaea = "https://data.ace.uq.edu.au/public/gtdb/data/releases/latest/ar122_metadata.tar.gz"
  gtdb_to_ncbi_to_gg_silva_bacteria = "https://data.ace.uq.edu.au/public/gtdb/data/releases/latest/bac120_metadata.tar.gz"

  # import as pandas dataframe
  df_gtdb_to_ncbi_to_gg_silva_archaea = pd.DataFrame(pd.read_csv(gtdb_to_ncbi_to_gg_silva_archaea, sep='\t'))
  df_gtdb_to_ncbi_to_gg_silva_bacteria = pd.DataFrame(pd.read_csv(gtdb_to_ncbi_to_gg_silva_bacteria, sep='\t'))

  # rename columns
  df_gtdb_to_ncbi_to_gg_silva_archaea.columns.values[0] = "GTDB_accession"
  df_gtdb_to_ncbi_to_gg_silva_bacteria.columns.values[0] = "GTDB_accession"

  # concatenate dataframes
  df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria = pd.concat([df_gtdb_to_ncbi_to_gg_silva_archaea, df_gtdb_to_ncbi_to_gg_silva_bacteria])

  # drop empty rows
  df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria = df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria.dropna(how='all')

  # add column to indicate if data from refseq or genbank
  df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria["RefSeq_or_GenBank"] = df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria["GTDB_accession"].map(lambda x: x[:2])

  # keep only columns required for taxonomy linking
  df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim = df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria[["GTDB_accession","RefSeq_or_GenBank","ncbi_genbank_assembly_accession","ncbi_species_taxid","ncbi_taxid","gtdb_taxonomy","ncbi_taxonomy","ncbi_taxonomy_unfiltered","ssu_query_id","ssu_gg_taxonomy","ssu_silva_taxonomy"]]

  return df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim
