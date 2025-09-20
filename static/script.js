document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('cropForm');
  const resultDiv = document.getElementById('result');

  form.addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent form from refreshing the page

    // Collect and validate input values
    const data = {
      N: parseFloat(document.getElementById('nitrogen').value),
      P: parseFloat(document.getElementById('phosphorus').value),
      K: parseFloat(document.getElementById('potassium').value),
      temperature: parseFloat(document.getElementById('temperature').value),
      humidity: parseFloat(document.getElementById('humidity').value),
      rainfall: parseFloat(document.getElementById('rainfall').value),
      ph: parseFloat(document.getElementById('ph').value)
    };

    // Check for NaN values (empty or invalid input)
    if (Object.values(data).some(val => isNaN(val))) {
      resultDiv.innerText = '⚠️ Please fill in all fields with valid numbers.';
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const result = await response.json();

      if (result.crop) {
        resultDiv.innerText = `🌿 Recommended Crop: ${result.crop}`;
      } else {
        resultDiv.innerText = '❌ No crop recommendation received.';
      }
    } catch (error) {
      console.error('Error:', error);
      resultDiv.innerText = '🚫 Failed to fetch crop recommendation.';
    }
  });
});
