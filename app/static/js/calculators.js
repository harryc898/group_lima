         /*
    NAME:          calculators.js
    AUTHOR:        Team Lima
    DATE:          10/01/25
    INSTITUTION:   University of Manchester (FBMH)
    DESCRIPTION:   JavaScript file for managing display of calculators
*/

function calculateCreatinineClearance() {
    // document.getElementById("result").innerHTML = "Hello";

    // Get user inputs
    let age = parseFloat(document.getElementById("patients-age").value);
    let weight = parseFloat(document.getElementById("patients-weight").value);
    let serumCreatinine = parseFloat(document.getElementById("patients-serum").value);
    let isMale = document.getElementById("sex").value === "male";

    // Validate inputs
    if (age <= 0 || weight <= 0 || serumCreatinine <= 0 || isNaN(age) || isNaN(weight) || isNaN(serumCreatinine)) {
        document.getElementById("result").innerHTML = "Please enter valid positive numbers.";
        return;
    }

    // Cockcroft-Gault formula constants
    let K = isMale ? 1.23 : 1.04;

    // Calculate creatinine clearance
    let creatinineClearance = ((140 - age) * weight * K) / serumCreatinine;

   // Display result
    document.getElementById("result").innerHTML =
        `Estimated Creatinine Clearance: <strong>${creatinineClearance.toFixed(2)} mL/min</strong>`;
}