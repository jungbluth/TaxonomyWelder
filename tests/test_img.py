import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.img import import_img_to_ncbi_table

class TestIMG(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.img_table_header_list = [
            "IMG_ID_taxon_oid", "Domain", "Sequencing_Status", "Study_Name",
            "Genome_Name_Sample_Name", "Sequencing_Center", "IMG_Genome_ID",
            "Phylum", "Class", "Order", "Family", "Genus", "Species",
            "IMG_Cluster_ID", "IMG_Release_Pipeline_Version", "NCBI_Taxon_ID",
            "Strain", "Genome_Size_assembled", "Gene_Count_assembled"
        ]

        self.sample_archaea_data = pd.DataFrame({
            'IMG_ID_taxon_oid': ['IMG1', 'IMG2'],
            'Domain': ['Archaea', 'Archaea'],
            'Phylum': ['Euryarchaeota', 'Crenarchaeota'],
            'Class': ['Methanobacteria', 'Thermoprotei'],
            'Order': ['Methanobacteriales', 'Thermoproteales'],
            'Family': ['Methanobacteriaceae', 'Thermoproteaceae'],
            'Genus': ['Methanobacterium', 'Thermoproteus'],
            'Species': ['Methanobacterium sp.', 'Thermoproteus sp.'],
            'Strain': ['Strain1', 'Strain2'],
            'IMG_Cluster_ID': ['Cluster1', 'Cluster2'],
            'IMG_Release_Pipeline_Version': ['v1', 'v1'],
            'NCBI_Taxon_ID': ['123', '456']
        }, columns=self.img_table_header_list)

        self.sample_bacteria_data = pd.DataFrame({
            'IMG_ID_taxon_oid': ['IMG3', 'IMG4'],
            'Domain': ['Bacteria', 'Bacteria'],
            'Phylum': ['Proteobacteria', 'Firmicutes'],
            'Class': ['Gammaproteobacteria', 'Bacilli'],
            'Order': ['Enterobacterales', 'Bacillales'],
            'Family': ['Enterobacteriaceae', 'Bacillaceae'],
            'Genus': ['Escherichia', 'Bacillus'],
            'Species': ['Escherichia coli', 'Bacillus subtilis'],
            'Strain': ['Strain3', 'Strain4'],
            'IMG_Cluster_ID': ['Cluster3', 'Cluster4'],
            'IMG_Release_Pipeline_Version': ['v1', 'v1'],
            'NCBI_Taxon_ID': ['789', '012']
        }, columns=self.img_table_header_list)

    @patch('pandas.read_csv')
    def test_import_img_to_ncbi_table(self, mock_read_csv):
        # Mock the read_csv calls to return our sample data
        mock_read_csv.side_effect = [
            self.sample_archaea_data,
            self.sample_bacteria_data,
            pd.DataFrame(columns=self.img_table_header_list),  # eukaryota
            pd.DataFrame(columns=self.img_table_header_list),  # plasmid
            pd.DataFrame(columns=self.img_table_header_list),  # viruses
            pd.DataFrame(columns=self.img_table_header_list)   # gfragment
        ]

        result = import_img_to_ncbi_table()

        # Check that the result has the expected columns
        expected_columns = [
            'IMG_ID_taxon_oid',
            'IMG_taxonomy_clean',
            'Strain',
            'IMG_Cluster_ID',
            'IMG_Release_Pipeline_Version',
            'NCBI_Taxon_ID'
        ]
        self.assertEqual(list(result.columns), expected_columns)

        # Check that the result contains all expected rows
        self.assertEqual(len(result), 4)

        # Check that taxonomy is correctly merged and cleaned
        expected_taxonomy = 'Archaea;Euryarchaeota;Methanobacteria;Methanobacteriales;Methanobacteriaceae;Methanobacterium;Methanobacterium sp.'
        self.assertEqual(result['IMG_taxonomy_clean'].iloc[0], expected_taxonomy)

        # Check that NCBI Taxon IDs are preserved
        self.assertEqual(result['NCBI_Taxon_ID'].iloc[0], '123')
        self.assertEqual(result['NCBI_Taxon_ID'].iloc[2], '789')

if __name__ == '__main__':
    unittest.main() 