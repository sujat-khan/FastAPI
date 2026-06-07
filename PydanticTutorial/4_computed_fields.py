from pydantic import BaseModel, EmailStr, AnyUrl, Field,computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr
    linkedin_url: AnyUrl
    age: int
    weight: float
    height:float
    married: bool = False
    allergies: list[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2 )
        return bmi

def Update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('BMI',patient.bmi)

    print("updated")

Patient_info ={'name': "Tom",'email':'abc@hdfc.com','linkedin_url':'https://www.linkedin.com/in/sujatkhan/ ','age':'61', 'weight':70,'height':1.6, 'allergies':['Pollen', 'dust'], 'contact_details':{'phone': '123','emergency':'123654e' }}


Patient1=Patient(**Patient_info)

Update_patient_data(Patient1)