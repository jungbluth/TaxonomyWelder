#!/usr/bin/env python3

import pandas as pd

def import_silva_to_ncbi_table():

  # paths to data
  silva_parc_to_ncbi = "https://ftp.arb-silva.de/release_138/Exports/full_metadata/SILVA_138_SSUParc.full_metadata.gz"
  silva_ref_to_ncbi = "https://ftp.arb-silva.de/release_138/Exports/full_metadata/SILVA_138_SSURef.full_metadata.gz"
  silva_nr99_to_ncbi = "https://ftp.arb-silva.de/release_138/Exports/full_metadata/SILVA_138_SSURef_Nr99.full_metadata.gz"

  # import as pandas dataframe
  df_silva_parc_to_ncbi = pd.DataFrame(pd.read_csv(silva_parc_to_ncbi, sep='\t', engine='python', usecols=[0,50], encoding='utf-8', error_bad_lines=False)) 
  df_silva_ref_to_ncbi = pd.DataFrame(pd.read_csv(silva_ref_to_ncbi, sep='\t', engine='python', usecols=[0,50], encoding='utf-8', error_bad_lines=False)) 
  df_silva_nr99_to_ncbi = pd.DataFrame(pd.read_csv(silva_nr99_to_ncbi, sep='\t', engine='python', usecols=[0,50], encoding='utf-8', error_bad_lines=False)) 

  # concatenate dataframes
  df_silva_ALL_trimmed = pd.concat([df_silva_parc_to_ncbi,df_silva_ref_to_ncbi,df_silva_nr99_to_ncbi])

  # drop duplicates
  df_silva_ALL_trimmed_dereplication = df_silva_ALL_trimmed.drop_duplicates()

  return df_silva_ALL_trimmed_dereplication
