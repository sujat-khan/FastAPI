from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr
    linkedin_url: AnyUrl
    age: int
    weight: float
    married: bool = False
    allergies: list[str]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted into database")

Patient_info ={'name': "Tom",'email':'abc@hdfc.com','linkedin_url':'https://www.linkedin.com/in/sujatkhan/ ','age':'61', 'weight':70, 'allergies':['Pollen', 'dust'], 'contact_details':{'phone': '123','emergency':'123654e' }}


Patient1=Patient(**Patient_info)

insert_patient_data(Patient1)