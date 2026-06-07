from fastapi import FastAPI, Path, HTTPException, Query
import json
app = FastAPI()

def load_data():
    with open ('patients.json','r') as f:
        data =json.load(f)
        return data

@app.get("/")
def hello():
    return {'message':'Patients Management System API'}


@app.get("/about")
def about():
    return {'message':'Fully functional API to manage your patient records'}

@app.get("/view")
def view():
    return load_data()

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str= Path(...,description='ID of the patient in Db', example='P001')):
    #load all the patients
    data =load_data()
    #search for the patient ID
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404,detail="Patient Not Found")    

@app.get("/sort")
def sort_patient(sort_by:str=Query(..., description="Sort on the basis of height, weight or bmi", example='bmi'), order=Query('asc', description='sort in ascending or descending order')):
    
    Valid_fields=['height','weight','bmi']
    if sort_by not in Valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field selected from {Valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Invalid order selected. Select asc or desc')
    
    #load all the patients 
    data = load_data()
    # now we will sort the data
    if order == 'desc':
        reverse=True
    else:
        reverse=False
    
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1][sort_by], reverse=reverse))
    return sorted_data