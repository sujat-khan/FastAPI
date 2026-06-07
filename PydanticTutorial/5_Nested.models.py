from pydantic import BaseModel, EmailStr, AnyUrl, Field,computed_field
from typing import List, Dict, Optional, Annotated

class Address(BaseModel):
    city:str
    state:str
    pin:str

class Patient(BaseModel):

    name:str
    gender:str
    age: int
    address:Address

address_dict={'city':'gurgaon', 'state':'haryana', 'pin':'122001'}

address1= Address(**address_dict)

Patient_dict= {'name':'Nitesh', 'gender':'male', 'age':37, 'address':address1}

Patient1=Patient(**Patient_dict)

print(Patient1)
print(Patient1.address.city)
print(Patient1.address.pin)