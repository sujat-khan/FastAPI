from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
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

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains=['hdfc.com', 'icici.com']

        domain_name= value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid email')

        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0<value<100:
            return value
        else:
            raise ValueError('age shiuld be between 0 and 100')

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted into database")

Patient_info ={'name': "Tom",'email':'abc@hdfc.com','linkedin_url':'https://www.linkedin.com/in/sujatkhan/ ','age':'30', 'weight':70, 'allergies':['Pollen', 'dust'], 'contact_details':{'phone': '123'}}


Patient1=Patient(**Patient_info)

insert_patient_data(Patient1)