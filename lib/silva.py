#!/usr/bin/env python3

import pandas as pd

def import_silva_to_ncbi_table(slv_version):

  # paths to data
  silva_parc_to_ncbi = "https://ftp.arb-silva.de/release_{}/Exports/full_metadata/SILVA_{}_SSUParc.full_metadata.gz".format(slv_version,slv_version)
  silva_ref_to_ncbi = "https://ftp.arb-silva.de/release_{}/Exports/full_metadata/SILVA_{}_SSURef.full_metadata.gz".format(slv_version,slv_version)
  silva_nr99_to_ncbi = "https://ftp.arb-silva.de/release_{}/Exports/full_metadata/SILVA_{}_SSURef_Nr99.full_metadata.gz".format(slv_version,slv_version)

  # paths to data
  silva_parc_taxonomy = "https://ftp.arb-silva.de/release_{}/Exports/taxonomy/taxmap_slv_ssu_parc_{}.txt.gz".format(slv_version,slv_version)
  silva_ref_taxonomy = "https://ftp.arb-silva.de/release_{}/Exports/taxonomy/taxmap_slv_ssu_ref_{}.txt.gz".format(slv_version,slv_version)
  silva_nr99_taxonomy = "https://ftp.arb-silva.de/release_{}/Exports/taxonomy/taxmap_slv_ssu_ref_nr_{}.txt.gz".format(slv_version,slv_version)

  # import as pandas dataframe
  df_silva_parc_to_ncbi = pd.DataFrame(pd.read_csv(silva_parc_to_ncbi, sep='\t', engine='python', usecols=[0,50], encoding='utf-8', error_bad_lines=False))
  df_silva_ref_to_ncbi = pd.DataFrame(pd.read_csv(silva_ref_to_ncbi, sep='\t', engine='python', usecols=[0,50], encoding='utf-8', error_bad_lines=False))
  df_silva_nr99_to_ncbi = pd.DataFrame(pd.read_csv(silva_nr99_to_ncbi, sep='\t', engine='python', usecols=[0,50], encoding='utf-8', error_bad_lines=False))

  # import as pandas dataframe
  df_silva_parc_taxonomy = pd.DataFrame(pd.read_csv(silva_parc_taxonomy, sep='\t', engine='python', usecols=[0,3,4,5], encoding='utf-8', error_bad_lines=False))
  df_silva_ref_taxonomy = pd.DataFrame(pd.read_csv(silva_ref_taxonomy, sep='\t', engine='python', usecols=[0,3,4,5], encoding='utf-8', error_bad_lines=False))
  df_silva_nr99_taxonomy = pd.DataFrame(pd.read_csv(silva_nr99_taxonomy, sep='\t', engine='python', usecols=[0,3,4,5], encoding='utf-8', error_bad_lines=False))

  # concatenate dataframes
  df_silva_to_ncbi_ALL_trimmed = df_silva_nr99_to_ncbi
  df_silva_taxonomy_ALL_trimmed = df_silva_nr99_taxonomy
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

def merge_current_and_legacy_silva(slv_version, legacy_slv_version):
  # import as pandas dataframe
  current_silva = pd.DataFrame(pd.read_csv("SILVA__slv{}_to_ncbi.tsv".format(slv_version), sep='\t', engine='python', encoding='utf-8', on_bad_lines=False))
  legacy_silva = pd.DataFrame(pd.read_csv("SILVA__slv{}_to_ncbi.tsv".format(legacy_slv_version), sep='\t', engine='python', encoding='utf-8', on_bad_lines=False))

  # merge
  silva_ALL_COMBINED = current_silva.merge(legacy_silva, left_on='SLV_accession', right_on='SLV_accession')

  # rename columns from current silva
  silva_ALL_COMBINED.columns.values[0] = "SLV{}_accession".format(slv_version)
  silva_ALL_COMBINED.columns.values[1] = "SLV{}_NCBI_taxid".format(slv_version)
  silva_ALL_COMBINED.columns.values[2] = "SLV{}_NCBI_accession".format(slv_version)
  silva_ALL_COMBINED.columns.values[3] = "SLV{}_taxonomy".format(slv_version)
  silva_ALL_COMBINED.columns.values[4] = "SLV{}_organisms_name".format(slv_version)
  silva_ALL_COMBINED.columns.values[5] = "SLV{}_taxid".format(slv_version)

  # rename columns from legacy silva
  silva_ALL_COMBINED.columns.values[6] = "SLV{}_NCBI_taxid".format(legacy_slv_version)
  silva_ALL_COMBINED.columns.values[7] = "SLV{}_NCBI_accession".format(legacy_slv_version)
  silva_ALL_COMBINED.columns.values[8] = "SLV{}_taxonomy".format(legacy_slv_version)
  silva_ALL_COMBINED.columns.values[9] = "SLV{}_organisms_name".format(legacy_slv_version)
  silva_ALL_COMBINED.columns.values[10] = "SLV{}_taxid".format(legacy_slv_version)

  return silva_ALL_COMBINED
