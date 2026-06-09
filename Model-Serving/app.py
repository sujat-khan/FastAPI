from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal,Annotated
import pickle
import pandas as pd

#import the ML model
import os

model_dir = os.path.dirname(os.path.abspath(__file__))
model_subdir_path = os.path.join(model_dir, 'model', 'model.pkl')
model_path = model_subdir_path if os.path.exists(model_subdir_path) else os.path.join(model_dir, 'model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

app =FastAPI()

#making Pydantic model to validate data

class UserInput(BaseModel):

    age:Annotated[int, Field(..., gt=0, lt=120, description='age of the user')]
    weight:Annotated[float, Field(..., gt=0, description='weight of the user')]
    height:Annotated[float, Field(..., gt=0, lt=2.5, description='height of the user')]
    income_lpa:Annotated[float, Field(..., gt=0, description='annual salary of the user')]
    smoker:Annotated[bool, Field(...,  description='Is the user a smoker')]
    city:Annotated[str, Field(..., description='city of the user')]
    occupation: Annotated[Literal[ 'retired',     'freelancer',        'student', 'government_job',
 'business_owner',     'unemployed',    'private_job'], Field(..., description='occupation of the user')]

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v:str)->str:
        v= v.strip().title()
        return v


    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

#human readable
@app.get('/')
def home():
    return {'message':'Insurance Premium Prediction APi'}

#machine readable
@app.get('/health')
def health_check():
    return {
        'status': 'OKK'
    }

@app.post('/predict')
def predict_premium(data:UserInput):

    input_df= pd.DataFrame([{
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation
    }])
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    
    # Calculate probabilities and confidence
    probabilities = model.predict_proba(input_df)[0]
    class_probs = {str(cls): float(prob) for cls, prob in zip(model.classes_, probabilities)}
    confidence = float(max(probabilities))
    
    return JSONResponse(
        status_code=200,
        content={
            'response': {
                'predicted_category': prediction,
                'confidence': confidence,
                'class_probabilities': class_probs
            }
        }
    )




 

