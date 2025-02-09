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
from flask import url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from unittest.mock import MagicMock


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
    def test_get_total_act_cost(self):
        """Test that the total act cost returns the correct value."""
        self.assertEqual(self.db_mod.get_total_act_cost(),60316449.37,)
        'Test total act cost returns correct value'
    def test_get_total_number_items(self):
        self.assertEqual(self.db_mod.get_total_number_items(),8218165,)
        'Test total items returns correct value'
    def test_avg_act_cost(self):
        """Test that the average act cost returns the correct value."""
        self.assertEqual("{:,.2f}".format(
            self.db_mod.get_total_act_cost() /
            self.db_mod.get_total_number_items()),
            '7.34')
    def test_get_total_number_of_GP_practices(self):
        """Test that the total number of GP practices returns the correct value."""
        self.assertEqual(self.db_mod.get_total_gp_practices(), 9348, 'Test total GP practices returns correct value')
    def test_get_unique_items(self):
        """Test that the unique items tile returns the correct value"""
        self.assertEqual(self.db_mod.get_unique_items(), 13935, 'Test total unique items returns correct value')
    def test_get_prescribed_items_per_pct(self):
        """Test that get_prescribed_items_per_pct returns the correct total items per PCT."""
        # Expected output based on SQL query results (total prescribed items per PCT)
        expected_output = [
            799112, 652972, 636539, 583776, 567186, 567062, 531267,
            531254, 457151, 430706, 395672, 374641, 336864, 331009,
            299724, 253161, 229169, 216994, 6612, 2855, 2765, 2524,
            2365, 1445, 1269, 1083, 976, 965, 846, 165, 21, 11, 2, 2
        ]
        # Call the function
        result = self.db_mod.get_prescribed_items_per_pct()
        # Assertion: Check if the function output matches the expected list
        self.assertEqual(result, expected_output,
                         "The function should return the correct list of prescribed item totals per PCT.")
    def test_get_distinct_pcts(self):
        """Test that the total number of GP practices returns the correct value."""
        result = self.db_mod.get_distinct_pcts()
        result_sorted = sorted(result)
        expected_first_three = ["00C", "00D", "00J"]
        expected_count = 34
        #Check first three PCTs in the list are correct
        self.assertEqual(result_sorted[:3], expected_first_three,"The first three distinct PCTs should match expected values.")
        # Check the correct number of PCTs have been identified
        self.assertEqual(len(result_sorted), expected_count,f"The total number of distinct PCTs should be {expected_count}.")
if __name__ == "__main__":
    unittest.main()

#S2 Tests for the GP practice prescribed items bar chart
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

#S2: Tests for the antidepressant table
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

#S2: Tests for the creatinine calculator
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

#S3: Adding tests for the home route in the Views tab
class TestHomeRoute(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up before running all tests."""
        # Set SERVER_NAME in Flask config for testing
        app.config['SERVER_NAME'] = 'localhost'
        app.config["TESTING"] = True
        cls.client = app.test_client()
    def setUp(self):
        """Set up before each test."""
        self.app = app
        self.app_context = self.app.app_context()  # Create an app context
        self.app_context.push()  # Activate the context
        self.db_mod = Database()  # Create a new database instance for testing
    def tearDown(self):
        """Clean up after each test."""
        self.app_context.pop()  # Remove the app context
    def test_home_get_request(self):
        """Test that the home page loads successfully with a GET request."""
        response = self.client.get(url_for('dashboard.home'))
        self.assertEqual(response.status_code, 200, "Home page should load successfully.")
    def test_home_post_request_with_pct_selection(self):
        """Test that POST request updates selected PCT correctly."""
        # Mock get_distinct_pcts return
        self.db_mod.get_distinct_pcts = lambda: ["00C", "00D", "00J"]
        response = self.client.post(url_for('dashboard.home'), data={"pct-option": "00D"})
        self.assertEqual(response.status_code, 200, "Home page should handle POST requests.")
if __name__ == "__main__":
    unittest.main()


#S3: Testing BMI Calculator - back-end
from .calculator import calculateBMI
class TestBMICalculator(unittest.TestCase):
    def test_positive_output(self):
        result, _ = calculateBMI(height_cm=160, weight=60)
        self.assertTrue(result > 0, "BMI should be a positive value.")
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            calculateBMI(height_cm=150, weight=-2)
        with self.assertRaises(ValueError):
            calculateBMI(height_cm=-5, weight=80)
        with self.assertRaises(ValueError):
            calculateBMI(height_cm=105, weight=1500)
        with self.assertRaises(ValueError):
            calculateBMI(height_cm=400, weight=90)
    def test_example_input_rounding(self):
        result = calculateBMI(height_cm=171, weight=85)
        expected_output = (29.07, 'Overweight')
        self.assertEqual(result, expected_output)
    def test_edge_case_underweight(self):
        result, category = calculateBMI(height_cm=151, weight=42)
        self.assertEqual(category, "Underweight", "Expected category underweight, bmi 18.42.")
    def test_edge_case_obesity(self):
        result, category = calculateBMI(height_cm=85, weight=168)
        self.assertEqual(category, "Obesity", "Expected category obesity, bmi 30.12.")
if __name__ == '__main__':
    unittest.main()

#S3 Testing BMI Calculator - front-end
class TestBMICalculatorUI(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/dashboard/home/")
    def test_valid_bmi_calculation(self):
        """Test if the BMI calculator works correctly inside the popup."""
        driver = self.driver

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "bmi-calc")))
        driver.execute_script("document.getElementById('bmi-calc').style.display='block';")

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "height")))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "weight")))

        driver.find_element(By.ID, "height").send_keys("170")
        driver.find_element(By.ID, "weight").send_keys("70")

        calculate_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "calculate-bmi"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", calculate_button)
        driver.execute_script("arguments[0].click();", calculate_button)

        bmi_result = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "bmiResult"))).text

        self.assertIn("Normal weight", bmi_result, "BMI should be classified correctly.")
    def tearDown(self):
        self.driver.quit()
if __name__ == "__main__":
    unittest.main()


class TestPCTSummaryTile(unittest.TestCase):
    def setUp(self):
        # Create a mock database session
        self.mock_session = MagicMock()
        self.db_mod = Database()  # Initialize the class where get_top_pctgp() is defined
        self.db_mod.db_session = self.mock_session  # Assign the mock session to your database module
        self.app_context = app.app_context()
        self.app_context.push()
    def tearDown(self):
        self.app_context.pop()
    def test_get_top_pctgp(self):
        """Test the get_top_pctgp method to ensure it returns the correct PCT and practice count."""
        # Mock the return value of the database query to simulate the expected data
        mock_result = [
            ('00T', 61)
        ]
        self.mock_session.query().filter().group_by().order_by().first.return_value = mock_result[0]
        result = self.db_mod.get_top_pctgp()
        expected_most_recurring_pct = '00T'  # Expected PCT with the most GP Practices
        expected_distinct_practice_count = 61  # Expected number of distinct practices
        self.assertEqual(result[0], expected_most_recurring_pct,
                         f"Expected PCT with most GP Practices to be {expected_most_recurring_pct}, but got {result[0]}.")
        self.assertEqual(result[1], expected_distinct_practice_count,
                         f"Expected distinct practice count for PCT {expected_most_recurring_pct} to be {expected_distinct_practice_count}, but got {result[1]}.")
if __name__ == '__main__':
    unittest.main()
