
# To understand a simple hello world application using FastAPI

from fastapi import FastAPI , Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing_extensions import Annotated
from typing import Literal

import json

app = FastAPI()

class Patient(BaseModel):  #defining a Pydantic model for patient data validation
# we will calculte bmi on the basis of height and weight
#we will giver verdict on the basis of bmi
# will put condition based on age 

    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field #In pydantic, the computed_field decorator is used to define a field that is computed based on other fields in the model.
    @property  #property decorator is used to define a method as a property, allowing it to be accessed like an attribute.
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)   
    
    @computed_field
    @property   
    def verdict(self) -> str:  # To give health verdict based on BMI, it will trigger bmi and give verdict
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        


  



def load_data(): #function to load patient data from a JSON file
    with open("./patients.json", "r") as file:
        data = json.load(file)
        return data
    
def save_data(data):                                     #model_dump() method is used to convert the Pydantic model instance into a dictionary representation.
    with open("./patients.json", "w") as file:
        json.dump(data, file, indent=4)  #write the updated patient data back to the JSON file
    return {"message": "Patient record created successfully."}  #return a success message   
    

#define a root endpoint
@app.get("/")  #get request to the root URL, That is when someone want to see data from the server then uses get request.
               # "/" means the root URL, where a person is hitting the server.

def hello():
    return {"message": "Patient management system API"}  #returning a JSON response with a message key and "Hello, World!" as its value.




# Now let's create another endpoint tells about me.
@app.get("/about") 
def about():
    return {
        "message": "a Fully functional API to manage your Patient records efficiently."}



@app.get("/view") #endpoint to view all patient records
def view():
    data = load_data()  #load patient data from the JSON file
    return data  #return the loaded patient data as a JSON response 

# Lets use path parameter to view a specific patient record based on patient ID.
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(...,description = "Id of the patient in the DB",example = 'P001') ):  #path parameter to capture the patient ID from the URL, uNDER path parameter we can add more validation and description.
    data = load_data()  #load patient data from the JSON file
    if patient_id in data:
        return data[patient_id] #return the matching patient record
    
    # return {"message": "Patient not found"}  #return a message if no matching patient is found
    raise HTTPException(status_code=404, detail="Patient not found")  #return a 404 HTTP exception if no matching patient is found

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):  #endpoint to create a new patient record, accepting a Patient model as input
                                       #The patient parameter variable will check the incoming data against the Patient model for validation.

    # In this function the client didn't gave the bmi and verdict still we are not worried as both are computed fields so it will be calculated automatically.
    data = load_data()  #load existing patient data from the JSON file
    if patient.id in data: #check if the patient ID already exists in the data
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")  #return a 400 HTTP exception if the patient ID already exists
    
    data[patient.id] = patient.model_dump(exclude=['id'])  #add the new patient record to the existing data
    
    
    save_data(data)  #save the updated patient data back to the JSON file
    return JSONResponse(status_code=201, content={"message": "Patient record created successfully."})  #return a success message with a 201 status code




    


                  

























