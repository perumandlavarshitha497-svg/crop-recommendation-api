from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

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
        features = [
            data["N"], data["P"], data["K"],
            data["temperature"], data["humidity"],
            data["rainfall"], data["ph"]
        ]
        prediction = model.predict([features])[0]
        return jsonify({"crop": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
