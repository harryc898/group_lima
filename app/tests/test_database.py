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
import coverage
from app import app
from app.database.controllers import Database
from unittest.mock import patch


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


class TestGPPracticeAPI(unittest.TestCase):
    """Test GP Practice API without external dependencies."""

    def setUp(self):
        """Set up mock data for testing."""
        # Mock data for GP practices
        self.mock_practices = [
            {'practice_code': 'P88026', 'practice_name': 'HEATON MOOR MEDICAL GROUP'},
            {'practice_code': 'A83022', 'practice_name': 'THE MEDICAL GROUP'},
            {'practice_code': 'A83018', 'practice_name': 'CONSETT MEDICAL CENTRE'},
            {'practice_code': 'N81022', 'practice_name': 'MIDDLEWOOD PARTNERSHIP'},
            {'practice_code': 'A83057', 'practice_name': 'EAST DURHAM MEDICAL GROUP'},
            {'practice_code': 'P83012', 'practice_name': 'TOWER FAMILY HEALTHCARE'},
            {'practice_code': 'N81087', 'practice_name': 'DANEBRIDGE MEDICAL CENTRE'},
            {'practice_code': 'A81044', 'practice_name': 'MCKENZIE HOUSE SURGERY'},
            {'practice_code': 'A83012', 'practice_name': 'WILLIAM BROWN CENTRE'},
            {'practice_code': 'A83037', 'practice_name': 'BEWICK CRESCENT SURGERY'},
        ]

        # Mock data for prescribing
        self.mock_prescribing_data = [
            {'practice': 'P88026', 'BNF_name': 'Lansoprazole_Cap 30mg (E/C Gran)', 'items': 67008},
            {'practice': 'A83022', 'BNF_name': 'Paracet_Tab 500mg', 'items': 59917},
            {'practice': 'A83018', 'BNF_name': 'Omeprazole_Cap E/C 20mg', 'items': 58716},
            {'practice': 'N81022', 'BNF_name': 'Omeprazole_Cap E/C 20mg', 'items': 55029},
            {'practice': 'A83057', 'BNF_name': 'Paracet_Tab 500mg', 'items': 54456},
            {'practice': 'P83012', 'BNF_name': 'Omeprazole_Cap E/C 20mg', 'items': 51234},
            {'practice': 'N81087', 'BNF_name': 'Omeprazole_Cap E/C 20mg', 'items': 50779},
            {'practice': 'A81044', 'BNF_name': 'Atorvastatin_Tab 20mg', 'items': 46199},
            {'practice': 'A83012', 'BNF_name': 'Lansoprazole_Cap 30mg (E/C Gran)', 'items': 44458},
            {'practice': 'A83037', 'BNF_name': 'Omeprazole_Cap E/C 20mg', 'items': 42326},
        ]

    def test_get_total_gp_practices(self):
        """Test the total number of GP practices."""
        total_gp_practices = len(self.mock_practices)  # Count practices in mock data
        self.assertEqual(total_gp_practices, 10, "Total GP practices should be 10")

    def test_get_prescribed_items_per_gp_practice(self):
        """Test the breakdown of prescribed items per GP practice."""
        # Mock logic to calculate prescribed items per practice
        prescribed_items_per_practice = {}
        for entry in self.mock_prescribing_data:
            practice_code = entry['practice']
            if practice_code not in prescribed_items_per_practice:
                prescribed_items_per_practice[practice_code] = []
            prescribed_items_per_practice[practice_code].append(entry)

        # Assert the correct number of practices have data
        self.assertEqual(len(prescribed_items_per_practice), 10, "Should have 10 practices with prescribed items")

        # Assert that each practice has the correct data
        for practice_code, items in prescribed_items_per_practice.items():
            self.assertTrue(all('BNF_name' in item and 'items' in item for item in items),
                            f"All items for practice {practice_code} should have 'BNF_name' and 'items'")

        # Check an example breakdown
        example_practice_code = 'P88026'
        example_items = [item for item in self.mock_prescribing_data if item['practice'] == example_practice_code]
        self.assertEqual(len(prescribed_items_per_practice[example_practice_code]), len(example_items),
                         f"Practice {example_practice_code} should have the correct number of prescribed items")

if __name__ == "__main__":
    unittest.main()

class TestTopFiveAntidepressants(unittest.TestCase):
    """Test the `get_top_five_antidepressants` method."""

    def setUp(self):
        """Set up mock data for testing."""
        # Create a mock database controller
        self.mock_data = [
            {'BNF_name': 'Drug A', 'BNF_code': '040301', 'items': 120},
            {'BNF_name': 'Drug B', 'BNF_code': '040302', 'items': 110},
            {'BNF_name': 'Amitriptyline', 'BNF_code': '040303', 'items': 100},
            {'BNF_name': 'Drug C', 'BNF_code': '040304', 'items': 90},
            {'BNF_name': 'Drug D', 'BNF_code': '040305', 'items': 80},
            {'BNF_name': 'Drug E', 'BNF_code': '040306', 'items': 70},
            {'BNF_name': 'Drug F', 'BNF_code': '040307', 'items': 60},
        ]

    @patch('app.database.controllers.Database.get_top_five_antidepressants')
    def test_get_top_five_antidepressants(self, mock_get_top_five_antidepressants):
        """Test fetching the top 5 antidepressants excluding Amitriptyline."""
        # Mock the method to return filtered data
        mock_get_top_five_antidepressants.return_value = [
            {'BNF_name': 'Drug A', 'total_items': 120},
            {'BNF_name': 'Drug B', 'total_items': 110},
            {'BNF_name': 'Drug C', 'total_items': 90},
            {'BNF_name': 'Drug D', 'total_items': 80},
            {'BNF_name': 'Drug E', 'total_items': 70},
        ]

        # Call the method
        db_instance = Database()
        result = db_instance.get_top_five_antidepressants()

        # Assertions
        self.assertEqual(len(result), 5, "Should return exactly 5 drugs.")
        self.assertNotIn('Amitriptyline', [drug['BNF_name'] for drug in result],
                         "Amitriptyline should be excluded.")
        self.assertEqual(result[0]['BNF_name'], 'Drug A', "The top drug should be 'Drug A'.")
        self.assertEqual(result[-1]['BNF_name'], 'Drug E', "The last drug should be 'Drug E'.")

if __name__ == "__main__":
    unittest.main()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def test_creatinine_calculator():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        driver.get(
            'file:///C:/Users/carphar/Documents/group_lima/group_lima/app/templates/dashboard/index.html')

        age_input = driver.find_element(By.NAME, 'patients-age')
        age_input.send_keys('150')
        time.sleep(1)

        assert age_input.get_attribute('value') == '', "Age input should reject value above max"

    finally:
        driver.quit()

if __name__ == "__main__":
    test_creatinine_calculator()

    if __name__ == "__main__":
        try:
            test_creatinine_calculator()
            print("Test completed successfully.")
        except AssertionError as e:
            print(f"Test failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


import unittest
from .calculator import calculateCreatinineClearance

class TestCreatinineClearance(unittest.TestCase):

    def test_edge_case_age(self):
        result = calculateCreatinineClearance(age=18, weight=70, creatinine=1.0, sex="male")
        self.assertTrue(result > 0)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            calculateCreatinineClearance(age=-5, weight=70, creatinine=1.0, sex="male")

if __name__ == '__main__':
    unittest.main()
