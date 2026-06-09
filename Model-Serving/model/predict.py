#import the ML model
import os
import pickle
import pandas as pd

model_dir = os.path.dirname(os.path.abspath(__file__))
model_subdir_path = os.path.join(model_dir, 'model', 'model.pkl')
model_path = model_subdir_path if os.path.exists(model_subdir_path) else os.path.join(model_dir, 'model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# MLFlow
MODEL_VERSION = '1.0.0'

# Get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(user_input: dict):

    df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = model.predict(df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)
    
    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }