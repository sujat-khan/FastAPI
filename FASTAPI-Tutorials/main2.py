from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field,computed_field
from typing import Annotated, Literal, Optional
app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='Id of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the Patient')]
    city: Annotated[str, Field(..., description='city where Patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='age of the patient')]
    gender: Annotated[Literal['male','female','others'], Field(..., description='gender of the patient')]
    height:Annotated[float, Field(..., gt=0, description='height of the patient')]
    weight:Annotated[float, Field(..., gt=0, description='Weight of the Patient in Kgs')]

    @computed_field
    @property
    def bmi(Self)->float:
        bmi = Self.weight/(Self.height**2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)-> str:

        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi <25:
            return "Normal"
        elif self.bmi <30:
            return 'Normal 2'
        else:
            return "Obese"


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male','female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open ('patients.json','r') as f:
        data =json.load(f)
        return data

def save_data(data):
    with open ('patients.json','w') as f:
        json.dump(data,f)

#viewing the data
@app.get("/")
def hello():
    return {'message':'Patients Management System API'}


@app.get("/about")
def about():
    return {'message':'Fully functional API to manage your patient records'}

@app.get("/view")
def view():
    return load_data()

#creating a new patient record
@app.post('/create')
def create_patient(patient:Patient):

    #load existing data
    #check if the patient already exists


    data =load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    #then create new patient to the database
    data[patient.id]=patient.model_dump(exclude=['id'])

    #save into the Json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

#creating a new put endpoint

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update:PatientUpdate):

    data =load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    existing_patient_info = data[patient_id] #has all the fields

    updated_patient_info = patient_update.model_dump(exclude_unset=True) #only fields which client want to update

    for key, value in updated_patient_info.items():
        existing_patient_info[key]=value

    #existing_patient_info -> Pydantic object -> updated bmi + Verdict -> Pydantic Object -> dict
    existing_patient_info['id']=patient_id
    Patient_Pydantic_object = Patient(**existing_patient_info)

    existing_patient_info= Patient_Pydantic_object.model_dump(exclude='id')

    data[patient_id] =existing_patient_info

    #saving the data
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'Patient Updated'})




@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):

    #loading the data first
    data =load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted'})