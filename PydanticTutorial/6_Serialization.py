from pydantic import BaseModel

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

temp = Patient1.model_dump(include=['name'])

print(temp)
print(type(temp))

temp1 = Patient1.model_dump_json()

print(temp1)
print(type(temp1))