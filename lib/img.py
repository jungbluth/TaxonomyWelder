#!/usr/bin/env python3

import pandas as pd


def import_img_to_ncbi_table():

  # paths to data
  img_to_ncbi_archaea = "https://github.com/jungbluth/taxonomy_welder/blob/main/docs/IMG/taxontable36551_19-jan-2021.xls"
  img_to_ncbi_bacteria = "https://github.com/jungbluth/taxonomy_welder/blob/main/docs/IMG/taxontable37056_19-jan-2021.xls"
  img_to_ncbi_eukaryota = "https://github.com/jungbluth/taxonomy_welder/blob/main/docs/IMG/taxontable37303_19-jan-2021.xls"
  img_to_ncbi_plasmid = "https://github.com/jungbluth/taxonomy_welder/blob/main/docs/IMG/taxontable37445_19-jan-2021.xls"
  img_to_ncbi_viruses = "https://github.com/jungbluth/taxonomy_welder/blob/main/docs/IMG/taxontable37511_19-jan-2021.xls"
  img_to_ncbi_gfragment = "https://github.com/jungbluth/taxonomy_welder/blob/main/docs/IMG/taxontable37553_19-jan-2021.xls"

  # import as pandas dataframe
  img_table_header_list = [ "taxon_oid", "Domain", "Sequencing_Status", "Study_Name", "Genome_Name_Sample_Name", "Sequencing_Center", "IMG_Genome_ID", "Phylum", "Class", "Order", "Family", "Genus", "Species", "NCBI_Taxon_ID", "Strain", "Genome_Size_assembled", "Gene_Count_assembled" ]
  df_img_to_ncbi_archaea = pd.DataFrame(pd.read_csv(img_to_ncbi_archaea, sep='\t', header=0, names=img_table_header_list))
  df_img_to_ncbi_bacteria = pd.DataFrame(pd.read_csv(img_to_ncbi_bacteria, sep='\t'))
  df_img_to_ncbi_eukaryota = pd.DataFrame(pd.read_csv(img_to_ncbi_eukaryota, sep='\t'))
  df_img_to_ncbi_plasmid = pd.DataFrame(pd.read_csv(img_to_ncbi_plasmid, sep='\t'))
  df_img_to_ncbi_viruses = pd.DataFrame(pd.read_csv(img_to_ncbi_viruses, sep='\t'))
  df_img_to_ncbi_gfragment = pd.DataFrame(pd.read_csv(img_to_ncbi_gfragment, sep='\t'))




  # # rename columns
  # df_gtdb_to_ncbi_to_gg_silva_archaea.columns.values[0] = "GTDB_accession"
  # df_gtdb_to_ncbi_to_gg_silva_bacteria.columns.values[0] = "GTDB_accession"

  # concatenate dataframes
  df_img_to_ncbi_all = pd.concat([df_img_to_ncbi_archaea, df_img_to_ncbi_bacteria, df_img_to_ncbi_eukaryota, df_img_to_ncbi_plasmid, df_img_to_ncbi_viruses, df_img_to_ncbi_gfragment])

  # keep only columns required for taxonomy linking
  df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim = df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria[["GTDB_accession","RefSeq_or_GenBank","ncbi_genbank_assembly_accession","ncbi_taxid","gtdb_taxonomy","ncbi_taxonomy","ncbi_taxonomy_unfiltered","ssu_gg_taxonomy","ssu_silva_taxonomy"]]

  return df_gtdb_to_ncbi_to_gg_silva_archaea_plus_bacteria_trim
