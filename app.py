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

@app.route('/')
def home():
    return "🌱 Crop Recommendation API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Extract features from request
        features = [
            data['N'], data['P'], data['K'],
            data['temperature'], data['humidity'],
            data['rainfall'], data['ph']
        ]

        # Make prediction
        crop = model.predict([features])[0]

        # Return result
        return jsonify({'crop': crop})

    except Exception as e:
        # Return error as JSON instead of HTML
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
