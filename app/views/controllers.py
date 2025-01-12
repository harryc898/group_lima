"""
NAME:          views\controllers.py
AUTHOR:        Alan Davies (Senior Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          18/12/2019
UPDATED:       07/06/2024
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Views module. Renders HTML pages and passes in associated data to render on the
               dashboard.
"""
import json
import plotly
import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request,jsonify
from app.database.controllers import Database

views = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# get the database class
db_mod = Database()

# Set the route and accepted methods
@views.route('/home/', methods=['GET', 'POST'])
def home():
    """Render the home page of the dashboard passing in data to populate dashboard."""
    pcts = db_mod.get_distinct_pcts()
    practices = db_mod.get_distinct_practices()
    if request.method == 'POST':
        form = request.form
        # Preserve the current selections from the form
        selected_pct = form.get('pct-option', pcts[0])
        selected_practice = form.get('practice-option', practices[0])
    else:
        # Default selections
        selected_pct = pcts[0]
        selected_practice = practices[0]
    # Fetch data based on selections
    selected_pct_data = db_mod.get_n_data_for_PCT(selected_pct, 5)
    selected_practice_data = db_mod.get_antidepressant_data_for_practice(selected_practice, 5)
    # prepare data structure to send to front end to update display
    dashboard_data = {    
        #Tiles
        "tile_data_items": generate_data_for_tiles(),
        #Graph already on dashboard for PCT items
        "top_items_plot_data": generate_top_px_items_barchart_data(),
        #pct/practice list, data and selected cells
        "pct_list": pcts,
        "practice_list": practices,
        "pct_data": selected_pct_data,
        "practice_data": selected_practice_data,
        "selected_pct": selected_pct,
        "selected_practice": selected_practice,
    }
    
    # render the HTML page passing in relevant data
    return render_template('dashboard/index.html',dashboard_data=dashboard_data)

def generate_data_for_tiles():
    """Generate the data for the home page tiles."""
    tile_data = {
        "total_items": db_mod.get_total_number_items(),
        "total_gp_practices": db_mod.get_total_gp_practices(),
        "avg_act_cost": None,
        "top_px_item": None,
        "num_unique_items": None,
        "total_act_cost": "{:,.2f}".format(db_mod.get_total_act_cost())
    }
    return tile_data

def generate_top_px_items_barchart_data():
    """Generate the data needed to populate the number of most prescrbed items per PCT barchart."""
    
    # Create a dataframe to store the database query results
    df = pd.DataFrame({
        "data_values": db_mod.get_prescribed_items_per_pct(),
        "pct_codes": db_mod.get_distinct_pcts()
    })
    # Generate the plot
    fig = px.bar(df, x="pct_codes", y="data_values", 
                 labels={"pct_codes": "PCT code", 
                         "data_values": "Prescribed items (number)"}).update_xaxes(categoryorder="sum descending")

    # Convert the plot for rendering and add any metadata (description/header)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Prescribed items per Primary Care Trust (PCT)"
    description = "Total number (sum) of prescribed items per PCT (Primary Care Trust) by PCT code."
    plot_data = {
        'graphJSON': graphJSON,
        'header': header,
        'description': description
    }
    return plot_data