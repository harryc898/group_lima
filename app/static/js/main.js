/*
    NAME:          main.js
    AUTHOR:        Alan Davies (Lecturer Health Data Science)
    EMAIL:         alan.davies-2@manchester.ac.uk
    DATE:          18/12/2019
    INSTITUTION:   University of Manchester (FBMH)
    DESCRIPTION:   JavaScript file for initializing the JavaScript functionality.
*/

var popup = null;
var barChart = null;

// initialisation function
function initializeMain()
{
    popup = Popup();
    barChart = BarChart();
}

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
});
