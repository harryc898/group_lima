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
    selected_practice_data = db_mod.get_top_antidepressants_per_practice(selected_practice, 5)
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
        #Graph for top 5 antidepressant drugs prescribed
        "top_antidepressant_quantity_plot_data": generate_antidepressant_barchart_data(selected_practice=selected_practice),
    }
    
    # render the HTML page passing in relevant data
    return render_template('dashboard/index.html',dashboard_data=dashboard_data)

@views.route('/top_practices_chart_data', methods=['GET'])
def top_practices_chart_data():
    """API endpoint to fetch top GP practices chart data."""
    chart_data = generate_top_practices_barchart_data()
    return jsonify(chart_data)


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

def generate_top_practices_barchart_data():
    """Generate data for the top 10 GP practices chart with total items and tooltip showing the most prescribed item."""
    # Fetch the data from the database method
    data = db_mod.get_prescribed_items_per_gp_practice()

    # Extract practices, total items, and most prescribed items for the chart
    practices = []
    total_items = []
    most_prescribed_items = []
    for practice_breakdown in data['breakdown']:
        practices.append(practice_breakdown['practice'])
        # Get total items for the practice (already provided in 'top_practices')
        total_items.append(next(item[1] for item in data['top_practices'] if item[0] == practice_breakdown['practice']))
        # Get the most prescribed item for each practice
        most_prescribed = max(practice_breakdown['items'], key=lambda x: x[1])  # Sort by item count
        most_prescribed_items.append(f"{most_prescribed[0]} ({most_prescribed[1]})")

    # Create a DataFrame for Plotly
    df = pd.DataFrame({
        "practice": practices,
        "total_items": total_items,
        "most_prescribed_item": most_prescribed_items
    })

    # Generate the Plotly bar chart
    fig = px.bar(
        df,
        x="practice",
        y="total_items",
        labels={"practice": "GP Practice", "total_items": "Total Prescribed Items"}
    ).update_xaxes(categoryorder="total descending")

    # Customize hover template
    fig.update_traces(
        hovertemplate=(
            "<b>GP Practice:</b> %{x}<br>" +
            "<b>Total Prescribed Items:</b> %{y}<br>" +
            "<b>Most Prescribed Item:</b> %{customdata}<extra></extra>"
        ),
        customdata=df['most_prescribed_item']  # Add the most prescribed item to the hover tooltip
    )

    # Convert the plot for rendering
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return {
        'graphJSON': graphJSON,
        'header': "Top 10 GP Practices by Prescribed Items",
        'description': "Bar chart of the top 10 GP practices by the total number of prescribed items. Hover over a bar to see the most prescribed item for each practice."
    }




def generate_antidepressant_barchart_data(selected_practice=None):
    """Generate the data needed to populate the top 5 antidepressants prescribed in each practice barchart."""
    # Fetch all data
    db_mod = Database()
    raw_data = db_mod.get_top_antidepressants_per_practice(selected_practice=selected_practice)
    # Organize data by practice
    practices = {}
    for row in raw_data:
        practice = row[0]  # Adjust index for practice
        if practice not in practices:
            practices[practice] = []
        practices[practice].append({"BNF_code": row[1], "quantity": row[3]})
    # Default to the first practice if none is selected
        # Handle cases where no practice is selected or the selected practice has no data
        if not selected_practice:
            selected_practice = list(practices.keys())[0]  # Default to the first practice
        if selected_practice not in practices or not practices[selected_practice]:
            # Return a placeholder response if no data is available for the selected practice
            return {
                'graphJSON': None,
                'header': f"No data available for {selected_practice}",
                'description': "Try selecting a different practice.",
                'practice_list': list(practices.keys()),
                'selected_practice': selected_practice,
            }
    # Prepare the DataFrame for the selected practice
    df = pd.DataFrame(practices[selected_practice])
    # Generate the bar chart
    fig = px.bar(df, x="BNF_code", y="quantity",
                 labels={"BNF_code": "BNF code",
                         "quantity": "Quantity prescribed (number)"}).update_xaxes(categoryorder="sum descending")
    # Convert the plot for rendering and add metadata
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = f"Top antidepressants prescribed in practice: {selected_practice}"
    description = "INSERT DESCRIPTION HERE (views/controllers.py)"
    plot_data = {
        'graphJSON': graphJSON,
        'header': header,
        'description': description,
        'practice_list': list(practices.keys()),  # All practices for dropdown
        'selected_practice': selected_practice   # Currently selected practice
    }
    return plot_data

