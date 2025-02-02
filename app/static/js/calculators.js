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

function calculateBMI() {
      // Get user input
      const weight = parseFloat(document.getElementById('weight').value);
      const heightCm = parseFloat(document.getElementById('height').value);
      // Define maximum values
      const maxWeight = 1000
      const maxHeightCm = 350

      if (weight > 0 && heightCm > 0 && weight <= maxWeight && heightCm <= maxHeightCm) {
          // Convert height from cm to meters
          const heightM = heightCm / 100;

          // Calculate BMI
          const bmi = weight / (heightM * heightM);

          // Determine BMI category
          let category = '';
          if (bmi < 18.5) {
              category = 'Underweight';
          } else if (bmi < 24.9) {
              category = 'Normal weight';
          } else if (bmi < 29.9) {
              category = 'Overweight';
          } else {
              category = 'Obesity';
          }

          // Display the result
          document.getElementById('bmiResult').innerHTML =
              `<p>Your BMI is <strong>${bmi.toFixed(2)}</strong> (${category}).</p>`;
      } else {
          document.getElementById('bmiResult').innerHTML = '<p>Please enter valid weight and height values.</p>';
      }
  }