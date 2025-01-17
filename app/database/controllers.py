"""
NAME:          database\controllers.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          17/12/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Contains the Database class that contains all the methods used for accessing the database
"""
from sqlalchemy.sql import func, text
from flask import Blueprint, jsonify

from app import db
from app.database.models import PrescribingData, PracticeData

database = Blueprint('dbutils', __name__, url_prefix='/dbutils')
@database.route('/total_gp_practices', methods=['GET'])
def get_total_gp_practices():
    """API endpoint to fetch total number of GP practices."""
    db_instance = Database()
    total_practices = db_instance.get_total_gp_practices()
    return jsonify({"total_gp_practices": total_practices})



class Database:
    """Class for managing database queries."""
    
    def convert_tuple_list_to_raw(self, tuple_list):
        """Helper function to convert results from tuple list to plain list."""
        order_row = [tuple(row) for row in tuple_list]
        return  [item for i in order_row for item in i]

    #Already there: Total number of items for tile 1
    def get_total_number_items(self):
        """Return the total number of prescribed items."""
        return int(db.session.execute(db.select(func.sum(PrescribingData.items))).first()[0])

    #Already there: Prescribed items per PCT for graph 1
    def get_prescribed_items_per_pct(self):
        """Return the total items per PCT."""
        result = db.session.execute(db.select(func.sum(PrescribingData.items).label('item_sum')).group_by(PrescribingData.PCT)).all()
        return self.convert_tuple_list_to_raw(result)

    def get_prescribed_items_per_gp_practice(self):
        """Return the top 10 GP Practices by total prescribed items with breakdown."""
        # Query for the top 10 practices based on total items prescribed
        result = db.session.query(
            PrescribingData.practice,
            func.sum(PrescribingData.items).label('total_items')
        ).group_by(PrescribingData.practice).order_by(func.sum(PrescribingData.items).desc()).limit(10).all()

        # Fetch the breakdown of the most prescribed items for each top practice
        breakdown = []
        for practice, _ in result:
            most_prescribed = db.session.query(
                PrescribingData.BNF_name,
                func.sum(PrescribingData.items).label('item_count')
            ).filter(PrescribingData.practice == practice).group_by(PrescribingData.BNF_name).order_by(
                func.sum(PrescribingData.items).desc()).all()
            breakdown.append({
                'practice': practice,
                'items': most_prescribed
            })

        return {
            'top_practices': result,
            'breakdown': breakdown
        }

    #Already there: BNF data per PCT table
    def get_distinct_pcts(self):
        """Return the distinct PCT codes."""
        result = db.session.execute(db.select(PrescribingData.PCT).distinct()).all()
        return self.convert_tuple_list_to_raw(result)
    def get_n_data_for_PCT(self, pct, n):
        """Return all the data for a given PCT."""
        return db.session.query(PrescribingData).filter(PrescribingData.PCT == pct).limit(n).all()

    #Sprint 1: Total ACT cost tile
    def get_total_act_cost(self):
        """Return the total ACT cost."""
        return (db.session.execute(db.select(func.sum(PrescribingData.ACT_cost)))).first()[0]

    #Sprint 1: Total GP practices tile
    def get_total_gp_practices(self):
        """Return the total number of unique GP practices."""
        total_practices = db.session.execute(func.count((PracticeData.practice_code))).scalar()
        return (total_practices)

    #Sprint 2: Antidepressants visualisation (task 30)
    def get_distinct_practices(self):
        """Return the distinct practice codes."""
        result = db.session.execute(db.select(PrescribingData.practice).distinct()).all()
        return self.convert_tuple_list_to_raw(result)
    def get_top_antidepressants_per_practice(self, selected_practice, limit=5):
        """Fetch the top antidepressants prescribed in a practice, filtered by BNF_code and limited to a specified number."""
        # Query the database and filter by practice and BNF_code, limiting the result to 5 rows per practice
        result = db.session.query(PrescribingData).filter(
            PrescribingData.practice == selected_practice,
            PrescribingData.BNF_code.like('0403%')  # Adjust the BNF_code filter as necessary
        ).limit(limit).all()
        # Return a list of tuples containing the data for each row
        return [(row.practice, row.BNF_code, row.BNF_name, row.quantity, row.items) for row in result]

