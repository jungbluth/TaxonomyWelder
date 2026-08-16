import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.gtdb import import_gtdb_to_ncbi_to_gg_to_silva_table

class TestGTDB(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.sample_archaea_data = pd.DataFrame({
            'accession': ['RS_GCF_000000001.1', 'RS_GCF_000000002.1'],
            'ncbi_genbank_assembly_accession': ['GCA_000000001.1', 'GCA_000000002.1'],
            'ncbi_species_taxid': ['123', '456'],
            'ncbi_taxid': ['123', '456'],
            'gtdb_taxonomy': ['d__Archaea;p__Euryarchaeota', 'd__Archaea;p__Crenarchaeota'],
            'ncbi_taxonomy': ['Archaea;Euryarchaeota', 'Archaea;Crenarchaeota'],
            'ncbi_taxonomy_unfiltered': ['Archaea;Euryarchaeota', 'Archaea;Crenarchaeota'],
            'ssu_query_id': ['SSU1', 'SSU2'],
            'ssu_gg_taxonomy': ['Archaea;Euryarchaeota', 'Archaea;Crenarchaeota'],
            'ssu_silva_taxonomy': ['Archaea;Euryarchaeota', 'Archaea;Crenarchaeota']
        })

        self.sample_bacteria_data = pd.DataFrame({
            'accession': ['GB_GCF_000000003.1', 'GB_GCF_000000004.1'],
            'ncbi_genbank_assembly_accession': ['GCA_000000003.1', 'GCA_000000004.1'],
            'ncbi_species_taxid': ['789', '012'],
            'ncbi_taxid': ['789', '012'],
            'gtdb_taxonomy': ['d__Bacteria;p__Proteobacteria', 'd__Bacteria;p__Firmicutes'],
            'ncbi_taxonomy': ['Bacteria;Proteobacteria', 'Bacteria;Firmicutes'],
            'ncbi_taxonomy_unfiltered': ['Bacteria;Proteobacteria', 'Bacteria;Firmicutes'],
            'ssu_query_id': ['SSU3', 'SSU4'],
            'ssu_gg_taxonomy': ['Bacteria;Proteobacteria', 'Bacteria;Firmicutes'],
            'ssu_silva_taxonomy': ['Bacteria;Proteobacteria', 'Bacteria;Firmicutes']
        })

    @patch('pandas.read_csv')
    def test_import_gtdb_to_ncbi_to_gg_to_silva_table(self, mock_read_csv):
        # Mock the read_csv calls to return our sample data
        mock_read_csv.side_effect = [self.sample_archaea_data, self.sample_bacteria_data]

        result = import_gtdb_to_ncbi_to_gg_to_silva_table()

        # Check that the result has the expected columns
        expected_columns = [
            'GTDB_accession',
            'RefSeq_or_GenBank',
            'ncbi_genbank_assembly_accession',
            'ncbi_species_taxid',
            'ncbi_taxid',
            'gtdb_taxonomy',
            'ncbi_taxonomy',
            'ncbi_taxonomy_unfiltered',
            'ssu_query_id',
            'ssu_gg_taxonomy',
            'ssu_silva_taxonomy'
        ]
        self.assertEqual(list(result.columns), expected_columns)

        # Check that the result contains all expected rows
        self.assertEqual(len(result), 4)

        # Check that RefSeq_or_GenBank column is correctly populated
        self.assertTrue(all(result['RefSeq_or_GenBank'].isin(['RS', 'GB'])))

        # Check that GTDB_accession column is correctly renamed
        self.assertEqual(result['GTDB_accession'].iloc[0], 'RS_GCF_000000001.1')
        self.assertEqual(result['GTDB_accession'].iloc[2], 'GB_GCF_000000003.1')

if __name__ == '__main__':
    unittest.main() 