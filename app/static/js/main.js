/*
    NAME:          main.js
    AUTHOR:        Alan Davies (Lecturer Health Data Science)
    EMAIL:         alan.davies-2@manchester.ac.uk
    DATE:          18/12/2019
    INSTITUTION:   University of Manchester (FBMH)
    DESCRIPTION:   JavaScript file for initializing the JavaScript functionality.
*/

var popup = null;

// initialisation function
function initializeMain()
{
    popup = Popup();
}
document.addEventListener("DOMContentLoaded", function () {
    // Change the button text to 'Toggle Theme'
    const darkModeButton = document.getElementById('darkModeToggle');
    if (darkModeButton) {
        darkModeButton.innerText = 'Toggle Theme';
    }
});

document.addEventListener("DOMContentLoaded", function () {
    fetch('/dbutils/total_gp_practices')
        .then(response => response.json())
        .then(data => {
            document.getElementById('gp-practices').innerText = data.total_gp_practices;
        })
        .catch(error => {
            console.error('Error fetching GP practices data:', error);
            document.getElementById('gp-practices').innerText = "Error";
        });

    // Fetch the Top GP Practices chart data
    fetch('/dashboard/top_practices_chart_data')
        .then(response => response.json())
        .then(data => {
            Plotly.newPlot('top-practices-chart', JSON.parse(data.graphJSON));
        })
        .catch(error => {
            console.error('Error loading chart data:', error);
        });

function toggleTheme() {
    const body = document.body;
    body.classList.toggle('university-theme');
}

// Add an event listener for the 'Toggle Theme' button
document.getElementById('darkModeToggle').addEventListener('click', toggleTheme);

});
