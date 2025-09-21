from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Load the trained model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return "🌱 Crop Recommendation API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.get_json()

        # Format input as DataFrame with correct feature names
        features = pd.DataFrame([{
            "N": data["N"],
            "P": data["P"],
            "K": data["K"],
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "rainfall": data["rainfall"],
            "ph": data["ph"]
        }])

        # Make prediction
        prediction = model.predict(features)[0]
        return jsonify({"crop": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
