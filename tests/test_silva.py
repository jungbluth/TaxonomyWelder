import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.silva import import_silva_to_ncbi_table, merge_current_and_legacy_silva

class TestSilva(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.sample_parc_data = pd.DataFrame({
            'acc': ['SLV1', 'SLV2'],
            'ncbi_taxid': ['123', '456']
        })
        self.sample_ref_data = pd.DataFrame({
            'acc': ['SLV3', 'SLV4'],
            'ncbi_taxid': ['789', '012']
        })
        self.sample_nr99_data = pd.DataFrame({
            'acc': ['SLV5', 'SLV6'],
            'ncbi_taxid': ['345', '678']
        })
        self.sample_taxonomy_data = pd.DataFrame({
            'primaryAccession': ['SLV1', 'SLV2', 'SLV3', 'SLV4', 'SLV5', 'SLV6'],
            'taxonomy': ['Bacteria;Proteobacteria', 'Bacteria;Firmicutes', 
                        'Archaea;Euryarchaeota', 'Bacteria;Actinobacteria',
                        'Bacteria;Bacteroidetes', 'Archaea;Crenarchaeota'],
            'organism_name': ['Species1', 'Species2', 'Species3', 'Species4', 'Species5', 'Species6'],
            'taxid': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
        })

    @patch('pandas.read_csv')
    def test_import_silva_to_ncbi_table(self, mock_read_csv):
        # Mock the read_csv calls to return our sample data
        mock_read_csv.side_effect = [
            self.sample_parc_data,
            self.sample_ref_data,
            self.sample_nr99_data,
            self.sample_taxonomy_data,
            self.sample_taxonomy_data,
            self.sample_taxonomy_data
        ]

        result = import_silva_to_ncbi_table(138)

        # Check that the result has the expected columns
        expected_columns = [
            'SLV_accession',
            'NCBI_taxid',
            'NCBI_accession',
            'SLV_taxonomy',
            'SLV_organisms_name',
            'SLV_taxid'
        ]
        self.assertEqual(list(result.columns), expected_columns)

        # Check that the result contains all expected rows
        self.assertEqual(len(result), 6)

    @patch('pandas.read_csv')
    def test_merge_current_and_legacy_silva(self, mock_read_csv):
        # Create sample data for current and legacy SILVA
        current_silva = pd.DataFrame({
            'SLV_accession': ['SLV1', 'SLV2'],
            'NCBI_taxid': ['123', '456'],
            'NCBI_accession': ['NC1', 'NC2'],
            'taxonomy': ['Bacteria;Proteobacteria', 'Bacteria;Firmicutes'],
            'organisms_name': ['Species1', 'Species2'],
            'taxid': ['T1', 'T2']
        })

        legacy_silva = pd.DataFrame({
            'SLV_accession': ['SLV1', 'SLV2'],
            'NCBI_taxid': ['123', '456'],
            'NCBI_accession': ['NC1', 'NC2'],
            'taxonomy': ['Bacteria;Proteobacteria', 'Bacteria;Firmicutes'],
            'organisms_name': ['Species1', 'Species2'],
            'taxid': ['T1', 'T2']
        })

        # Mock the read_csv calls
        mock_read_csv.side_effect = [current_silva, legacy_silva]

        result = merge_current_and_legacy_silva(138, 132)

        # Check that the result has the expected columns
        expected_columns = [
            'SLV138_accession',
            'SLV138_NCBI_taxid',
            'SLV138_NCBI_accession',
            'SLV138_taxonomy',
            'SLV138_organisms_name',
            'SLV138_taxid',
            'SLV132_NCBI_taxid',
            'SLV132_NCBI_accession',
            'SLV132_taxonomy',
            'SLV132_organisms_name',
            'SLV132_taxid'
        ]
        self.assertEqual(list(result.columns), expected_columns)

        # Check that the result contains all expected rows
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main() 