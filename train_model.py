# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv('Crop_recommendation.csv')
X = data.drop('label', axis=1)
y = data['label']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
