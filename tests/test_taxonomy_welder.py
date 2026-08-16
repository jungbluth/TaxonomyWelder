import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TaxonomyWelder import (
    welcome_message,
    database_versions,
    arg_parser
)

class TestTaxonomyWelder(unittest.TestCase):
    def setUp(self):
        self.silva_version = 138
        self.gtdb_version = 202
        self.img_version = "accession date: 2021-10-27"
        self.ncbi_version = "accession date: 2021-10-27"

    def test_welcome_message(self):
        with patch('builtins.print') as mock_print:
            welcome_message()
            mock_print.assert_called()
            # Check that the welcome message contains key phrases
            self.assertTrue(any("TaxonomyWelder" in call[0][0] for call in mock_print.call_args_list))
            self.assertTrue(any("cross-linking taxonomic ontologies" in call[0][0] for call in mock_print.call_args_list))

    def test_database_versions(self):
        with patch('builtins.print') as mock_print:
            database_versions(self.silva_version, self.gtdb_version, self.img_version, self.ncbi_version)
            # Check that all version numbers are printed
            self.assertTrue(any(f"SILVA - v{self.silva_version}" in call[0][0] for call in mock_print.call_args_list))
            self.assertTrue(any(f"GTDB - v{self.gtdb_version}" in call[0][0] for call in mock_print.call_args_list))
            self.assertTrue(any(f"IMG - {self.img_version}" in call[0][0] for call in mock_print.call_args_list))
            self.assertTrue(any(f"NCBI - {self.ncbi_version}" in call[0][0] for call in mock_print.call_args_list))

    def test_arg_parser_defaults(self):
        with patch('sys.argv', ['TaxonomyWelder.py']):
            args = arg_parser()
            self.assertEqual(args.dl_img, 'n')
            self.assertEqual(args.dl_ncbi, 'n')
            self.assertEqual(args.dl_gtdb, 'n')
            self.assertEqual(args.dl_silva, 'n')
            self.assertEqual(args.dl_legacy_silva, 'n')
            self.assertEqual(args.legacy_silva_version, '132')

    def test_arg_parser_custom_values(self):
        test_args = [
            'TaxonomyWelder.py',
            '--dl_img', 'y',
            '--dl_ncbi', 'y',
            '--dl_gtdb', 'y',
            '--dl_silva', 'y',
            '--dl_legacy_silva', 'y',
            '--legacy_silva_version', '135'
        ]
        with patch('sys.argv', test_args):
            args = arg_parser()
            self.assertEqual(args.dl_img, 'y')
            self.assertEqual(args.dl_ncbi, 'y')
            self.assertEqual(args.dl_gtdb, 'y')
            self.assertEqual(args.dl_silva, 'y')
            self.assertEqual(args.dl_legacy_silva, 'y')
            self.assertEqual(args.legacy_silva_version, '135')

if __name__ == '__main__':
    unittest.main() 