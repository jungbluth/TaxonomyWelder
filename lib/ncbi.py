#!/usr/bin/env python3

import pandas as pd

# ncbi tables generated using online scripts
# info: https://github.com/zyxue/ncbitax2lin
# *) after install, run the command: ncbitax2lin --nodes-file taxdump/nodes.dmp --names-file taxdump/names.dmp

def import_ncbi_table():

  # paths to data
  ncbi_taxid_to_full_taxonomy = "https://raw.githubusercontent.com/jungbluth/TaxonomyWelder/main/docs/NCBI/ncbi_lineages_2021-10-28.csv.gz"

  # import as pandas dataframe
  df_ncbi_taxid_to_full_taxonomy = pd.DataFrame(pd.read_csv(ncbi_taxid_to_full_taxonomy, sep=','))

  return df_ncbi_taxid_to_full_taxonomy
