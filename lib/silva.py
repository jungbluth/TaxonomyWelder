#!/usr/bin/env python3

import pandas as pd

def import_silva_to_ncbi_table():

  # paths to data
  silva_parc_to_ncbi = "https://ftp.arb-silva.de/release_138/Exports/full_metadata/SILVA_138_SSUParc.full_metadata.gz"
  silva_ref_to_ncbi = "https://ftp.arb-silva.de/release_138/Exports/full_metadata/SILVA_138_SSURef.full_metadata.gz"
  silva_nr99_to_ncbi = "https://ftp.arb-silva.de/release_138/Exports/full_metadata/SILVA_138_SSURef_Nr99.full_metadata.gz"

  # paths to data
  silva_parc_taxonomy = "https://ftp.arb-silva.de/release_138/Exports/taxonomy/taxmap_slv_ssu_parc_138.txt.gz"
  silva_ref_taxonomy = "https://ftp.arb-silva.de/release_138/Exports/taxonomy/taxmap_slv_ssu_ref_138.txt.gz"
  silva_nr99_taxonomy = "https://ftp.arb-silva.de/release_138/Exports/taxonomy/taxmap_slv_ssu_ref_nr_138.txt.gz"

  # import as pandas dataframe
  df_silva_parc_to_ncbi = pd.DataFrame(pd.read_csv(silva_parc_to_ncbi, sep='\t', engine='python', usecols=[0,50], encoding='utf-8', error_bad_lines=False))
  df_silva_ref_to_ncbi = pd.DataFrame(pd.read_csv(silva_ref_to_ncbi, sep='\t', engine='python', usecols=[0,50], encoding='utf-8', error_bad_lines=False))
  df_silva_nr99_to_ncbi = pd.DataFrame(pd.read_csv(silva_nr99_to_ncbi, sep='\t', engine='python', usecols=[0,50], encoding='utf-8', error_bad_lines=False))

  # import as pandas dataframe
  df_silva_parc_taxonomy = pd.DataFrame(pd.read_csv(silva_parc_taxonomy, sep='\t', engine='python', usecols=[0,3,4,5], encoding='utf-8', error_bad_lines=False))
  df_silva_ref_taxonomy = pd.DataFrame(pd.read_csv(silva_ref_taxonomy, sep='\t', engine='python', usecols=[0,3,4,5], encoding='utf-8', error_bad_lines=False))
  df_silva_nr99_taxonomy = pd.DataFrame(pd.read_csv(silva_nr99_taxonomy, sep='\t', engine='python', usecols=[0,3,4,5], encoding='utf-8', error_bad_lines=False))

  # concatenate dataframes
  df_silva_to_ncbi_ALL_trimmed = pd.concat([df_silva_parc_to_ncbi,df_silva_ref_to_ncbi,df_silva_nr99_to_ncbi])
  df_silva_taxonomy_ALL_trimmed = pd.concat([df_silva_parc_taxonomy,df_silva_ref_taxonomy,df_silva_nr99_taxonomy])

  # drop duplicates
  df_silva_to_ncbi_ALL_trimmed_dereplication = df_silva_to_ncbi_ALL_trimmed.drop_duplicates()
  df_silva_taxonomy_ALL_trimmed_dereplication = df_silva_taxonomy_ALL_trimmed.drop_duplicates()

  df_silva_to_ncbi_ALL_COMBINED = df_silva_to_ncbi_ALL_trimmed_dereplication.merge(df_silva_taxonomy_ALL_trimmed_dereplication, left_on='acc', right_on='primaryAccession')

  df_silva_to_ncbi_ALL_COMBINED.columns.values[0] = "SLV_accession"
  df_silva_to_ncbi_ALL_COMBINED.columns.values[1] = "NCBI_taxid"
  df_silva_to_ncbi_ALL_COMBINED.columns.values[2] = "NCBI_accession"
  df_silva_to_ncbi_ALL_COMBINED.columns.values[3] = "SLV_taxonomy"
  df_silva_to_ncbi_ALL_COMBINED.columns.values[4] = "SLV_organisms_name"
  df_silva_to_ncbi_ALL_COMBINED.columns.values[5] = "SLV_taxid"

  return df_silva_to_ncbi_ALL_COMBINED
