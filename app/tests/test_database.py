"""
NAME:          test_database.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          24/12/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Suite of tests for testing the dashboards database
               functionality.
"""

import unittest
from app import app
from app.database.controllers import Database

class DatabaseTests(unittest.TestCase):
    """Class for testing database functionality and connection."""

    def setUp(self):
        """Set up before each test."""
        # Tell Flask to use the app
        self.app = app
        self.app_context = self.app.app_context()  # Create app context
        self.app_context.push()  # Activate the context
        self.db_mod = Database()  # Create the database instance

    def tearDown(self):
        """Run post each test."""
        # Pop the application context
        self.app_context.pop()

    def test_get_total_number_items(self):
        """Test that the total number of items returns the correct value."""
        self.assertEqual(self.db_mod.get_total_number_items(),8218165,)
        'Test total items returns correct value'

    def test_get_total_act_cost(self):
        """Test that the total act cost returns the correct value."""
        self.assertEqual(self.db_mod.get_total_act_cost(),60316449.37,)
        'Test total act cost returns correct value'

        self.assertEqual(self.db_mod.get_total_number_items(),8218165,)
        'Test total items returns correct value'

    def test_get_total_number_of_GP_practices(self):
        """Test that the total number of GP practices returns the correct value."""
        self.assertEqual(self.db_mod.get_total_gp_practices(), 9348, 'Test total GP practices returns correct value')

if __name__ == "__main__":
    unittest.main()

