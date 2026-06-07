from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title='Name of the Patient', description='give the name of the patient in less than 50 words', examples=['Sujat', 'Mohit'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age : int=Field(gt=0, le=120)
    weight:Annotated[float, Field(gt=0, strict=True)]
    married:Annotated[bool, Field(default=None, description='Is the patient married or Not')]
    allergies: Annotated[Optional[list[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]

def insert_patient_data(Patient: Patient):

    print(Patient.name)
    print(Patient.age)
    print("inseted into database")

def Update_patient_data(Patient: Patient):

    print(Patient.name)
    print(Patient.age)
    print(Patient.married)
    print("updated")

Patient_info ={'name': "Tom",'email':'abc@gmail.com','linkedin_url':'https://www.linkedin.com/in/sujatkhan/ ','age':30, 'weight':70, 'allergies':['Pollen', 'dust'], 'contact_details':{'phone': '123'}}


Patient1=Patient(**Patient_info)

insert_patient_data(Patient1)
Update_patient_data(Patient1)