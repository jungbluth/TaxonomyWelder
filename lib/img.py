#!/usr/bin/env python3

import pandas as pd


def import_img_to_ncbi_table():

  # paths to data
  img_to_ncbi_archaea = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/current/IMGMER-Archaea_27-oct-2022.tsv"
  img_to_ncbi_bacteria = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/current/IMGMER-Bacteria_27-oct-2022.tsv"
  img_to_ncbi_eukaryota = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/current/IMGMER-Eukaryota_27-oct-2022.tsv"
  img_to_ncbi_plasmid = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/current/IMGMER-Plasmid_27-oct-2022.tsv"
  img_to_ncbi_viruses = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/current/IMGMER-Viruses_27-oct-2022.tsv"
  img_to_ncbi_gfragment = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/current/IMGMER-GFragment_27-oct-2022.tsv"

  # paths to old data
  # img_to_ncbi_archaea = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/old/taxontable36551_19-jan-2021.xls"
  # img_to_ncbi_bacteria = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/old/taxontable37056_19-jan-2021.xls"
  # img_to_ncbi_eukaryota = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/old/taxontable37303_19-jan-2021.xls"
  # img_to_ncbi_plasmid = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/old/taxontable37445_19-jan-2021.xls"
  # img_to_ncbi_viruses = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/old/taxontable37511_19-jan-2021.xls"
  # img_to_ncbi_gfragment = "https://raw.githubusercontent.com/jungbluth/taxonomy_welder/main/docs/IMG/old/taxontable37553_19-jan-2021.xls"

  # import as pandas dataframe
  img_table_header_list = [ "taxon_oid", "Domain", "Sequencing_Status", "Study_Name", "Genome_Name_Sample_Name", "Sequencing_Center", "IMG_Genome_ID", "Phylum", "Class", "Order", "Family", "Genus", "Species", "NCBI_Taxon_ID", "Strain", "Genome_Size_assembled", "Gene_Count_assembled" ]
  df_img_to_ncbi_archaea = pd.DataFrame(pd.read_csv(img_to_ncbi_archaea, sep='\t', index_col=False, skiprows=1, names=img_table_header_list))
  df_img_to_ncbi_bacteria = pd.DataFrame(pd.read_csv(img_to_ncbi_bacteria, sep='\t', index_col=False, skiprows=1, names=img_table_header_list))
  df_img_to_ncbi_eukaryota = pd.DataFrame(pd.read_csv(img_to_ncbi_eukaryota, sep='\t', index_col=False, skiprows=1, names=img_table_header_list))
  df_img_to_ncbi_plasmid = pd.DataFrame(pd.read_csv(img_to_ncbi_plasmid, sep='\t', index_col=False, skiprows=1, names=img_table_header_list))
  df_img_to_ncbi_viruses = pd.DataFrame(pd.read_csv(img_to_ncbi_viruses, sep='\t', index_col=False, skiprows=1, names=img_table_header_list))
  df_img_to_ncbi_gfragment = pd.DataFrame(pd.read_csv(img_to_ncbi_gfragment, sep='\t', index_col=False, skiprows=1, names=img_table_header_list))

  # concatenate dataframes
  df_img_to_ncbi_all = pd.concat([df_img_to_ncbi_archaea, df_img_to_ncbi_bacteria, df_img_to_ncbi_eukaryota, df_img_to_ncbi_plasmid, df_img_to_ncbi_viruses, df_img_to_ncbi_gfragment])

  # keep only columns required for taxonomy linking
  df_img_to_ncbi_all_trim = df_img_to_ncbi_all[["taxon_oid","Domain","Phylum","Class","Order","Family","Genus","Species","Strain","NCBI_Taxon_ID"]]

  # merge taxonomy columns into single column
  df_img_to_ncbi_all_trim_merge = df_img_to_ncbi_all_trim.assign(IMG_taxonomy = df_img_to_ncbi_all_trim.Domain.astype(str) + ';' + df_img_to_ncbi_all_trim.Phylum.astype(str) + ';' + df_img_to_ncbi_all_trim.Class.astype(str) + ';' + df_img_to_ncbi_all_trim.Order.astype(str) + ';' + df_img_to_ncbi_all_trim.Family.astype(str) + ';' + df_img_to_ncbi_all_trim.Genus.astype(str) + ';' + df_img_to_ncbi_all_trim.Species.astype(str))

  # clean IMG_taxonomy column
  df_img_to_ncbi_all_trim_merge['IMG_taxonomy_clean'] = df_img_to_ncbi_all_trim_merge['IMG_taxonomy'].str.replace('GFragment:','')
  # df_img_to_ncbi_all_trim_merge['IMG_taxonomy_clean'] = df_img_to_ncbi_all_trim_merge['IMG_taxonomy_clean'].str.replace('Plasmid:','')

  # keep only columns required for taxonomy linking
  df_img_to_ncbi_all_trim_merge_trim = df_img_to_ncbi_all_trim_merge[["taxon_oid","NCBI_Taxon_ID","IMG_taxonomy_clean", "Strain"]]

  return df_img_to_ncbi_all_trim_merge_trim
