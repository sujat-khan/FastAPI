from fastapi import FastAPI
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