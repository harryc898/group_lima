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
        result = db.session.execute(
            db.select(func.sum(PrescribingData.items).label('item_sum'))
            .group_by(PrescribingData.PCT)
            .order_by(func.sum(PrescribingData.items).desc())
        ).all()
        return self.convert_tuple_list_to_raw(result)

    def get_prescribed_items_per_gp_practice(self):
        """Return the top 10 GP Practices by total prescribed items with breakdown."""

        # Join PrescribingData and PracticeData to get practice names
        result = db.session.query(
            PracticeData.practice_name,  # Fetch practice name instead of practice code
            func.sum(PrescribingData.items).label('total_items')
        ).join(
            PracticeData, PrescribingData.practice == PracticeData.practice_code  # Join condition
        ).group_by(
            PracticeData.practice_name
        ).order_by(
            func.sum(PrescribingData.items).desc()
        ).limit(10).all()

        # Fetch the breakdown of the most prescribed items for each top practice
        breakdown = []
        for practice_name, _ in result:
            most_prescribed = db.session.query(
                PrescribingData.BNF_name,
                func.sum(PrescribingData.items).label('item_count')
            ).join(
                PracticeData, PrescribingData.practice == PracticeData.practice_code
                # Ensure join applies to breakdown query
            ).filter(
                PracticeData.practice_name == practice_name  # Filter by practice name
            ).group_by(
                PrescribingData.BNF_name
            ).order_by(
                func.sum(PrescribingData.items).desc()
            ).all()

            breakdown.append({
                'practice': practice_name,
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

    #Sprint 2: Task 30 version 2 - list top 5 antidepressants
    def get_top_five_antidepressants(self):
        result = db.session.query(
            PrescribingData.BNF_name,  # Group by this column
            func.sum(PrescribingData.items).label("total_items"),  # Sum the items
        ).filter(
            PrescribingData.BNF_code.like('0403%'),  # BNF code starts with 0403
            ~PrescribingData.BNF_name.like('Amitriptyline%')  # BNF name does not start with Amitriptyline
        ).group_by(PrescribingData.BNF_name).order_by(func.sum(PrescribingData.items).desc()).limit(5).all()
        return [{"BNF_name": row[0],"total_items": row[1]}for row in result]



    #Sprint3 t31
    def get_top_pctgp(self):
        """Find PCT with the most GP Practices."""
        # Query to count the number of distinct GP practices per PCT
        result = db.session.query(
            PrescribingData.PCT,
            func.count(func.distinct(PrescribingData.practice)).label('num_practices')
        ).group_by(PrescribingData.PCT).order_by(
            func.count(func.distinct(PrescribingData.practice)).desc()
        ).first()  # Get the top result (PCT with most practices)
        # If result is found, unpack it; otherwise, return default values
        most_recurring_PCT = result[0] if result else None
        distinct_practice_count = result[1] if result else 0
        return most_recurring_PCT, distinct_practice_count


    #Sprint 3: Task 3 - unique items tile
    def get_unique_items(self):
        """Return the total number of unique items"""
        unique_items = db.session.execute(db.select(func.count(db.distinct(PrescribingData.BNF_code)))).scalar()
        return(unique_items)

