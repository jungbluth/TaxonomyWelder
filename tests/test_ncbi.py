import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.ncbi import import_ncbi_table

class TestNCBI(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.sample_ncbi_data = pd.DataFrame({
            'tax_id': ['1', '2', '3'],
            'tax_name': ['root', 'Bacteria', 'Archaea'],
            'species': ['root', 'Bacteria', 'Archaea'],
            'genus': ['root', 'Bacteria', 'Archaea'],
            'family': ['root', 'Bacteria', 'Archaea'],
            'order': ['root', 'Bacteria', 'Archaea'],
            'class': ['root', 'Bacteria', 'Archaea'],
            'phylum': ['root', 'Bacteria', 'Archaea'],
            'kingdom': ['root', 'Bacteria', 'Archaea'],
            'superkingdom': ['root', 'Bacteria', 'Archaea']
        })

    @patch('pandas.read_csv')
    def test_import_ncbi_table(self, mock_read_csv):
        # Mock the read_csv call to return our sample data
        mock_read_csv.return_value = self.sample_ncbi_data

        result = import_ncbi_table()

        # Check that the result has the expected columns
        expected_columns = [
            'tax_id',
            'tax_name',
            'species',
            'genus',
            'family',
            'order',
            'class',
            'phylum',
            'kingdom',
            'superkingdom'
        ]
        self.assertEqual(list(result.columns), expected_columns)

        # Check that the result contains all expected rows
        self.assertEqual(len(result), 3)

        # Check that the data is preserved
        self.assertEqual(result['tax_id'].iloc[0], '1')
        self.assertEqual(result['tax_name'].iloc[1], 'Bacteria')
        self.assertEqual(result['superkingdom'].iloc[2], 'Archaea')

if __name__ == '__main__':
    unittest.main() 