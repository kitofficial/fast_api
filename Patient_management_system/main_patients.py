
# To understand a simple hello world application using FastAPI

from fastapi import FastAPI , Path, HTTPException
import json

app = FastAPI()

def load_data(): #function to load patient data from a JSON file
    with open("./patients.json", "r") as file:
        data = json.load(file)
        return data
    

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
























