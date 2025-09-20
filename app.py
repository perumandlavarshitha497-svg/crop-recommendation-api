from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Load trained model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully.")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not available'}), 500

    try:
        data = request.get_json()
        print("📥 Received data:", data)

        # Validate input
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'rainfall', 'ph']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing one or more required fields'}), 400

        # Convert to float and check for validity
        try:
            features = [float(data[field]) for field in required_fields]
        except ValueError:
            return jsonify({'error': 'Invalid input: all fields must be numeric'}), 400

        # Make prediction
        prediction = model.predict([features])[0]
        print("🌿 Predicted crop:", prediction)

        return jsonify({'crop': prediction})

    except Exception as e:
        print("❌ Prediction error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
