document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("cropForm");
  const resultDiv = document.getElementById("result");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Convert all values to numbers
    Object.keys(data).forEach(key => {
      data[key] = parseFloat(data[key]);
    });

    try {
      const response = await fetch("https://crop-recommendation-api-ivbw.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error("Server error: " + response.status);
      }

      const result = await response.json();
      resultDiv.textContent = "Recommended Crop: " + result.crop;
    } catch (error) {
      resultDiv.textContent = "Error: " + error.message;
    }
  });
});
