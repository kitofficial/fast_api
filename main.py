
# To understand a simple hello world application using FastAPI

from fastapi import FastAPI


app = FastAPI()

#define a root endpoint
@app.get("/")  #get request to the root URL, That is when someone want to see data from the server then uses get request.
               # "/" means the root URL, where a person is hitting the server.

def hello():
    return {"message": "Hello, World!"}  #returning a JSON response with a message key and "Hello, World!" as its value.



# To run above code use the command: uvicorn main:app --reload  . Here main is the name of the python file without .py extension and app is the name of the FastAPI instance.
# --reload makes the server restart after code changes. Only use this for development.
# After running the command, you can access the application at http://  



# Now let's create another endpoint tells about me.
@app.get("/about") 
def about_me():
    return {
        "name": "Ankit",
        "profession": "Data Scientist",
        "hobbies": ["reading", "traveling", "coding"]
    }

# Now if i go to previous endpoint and add "/about" at the end of the URL, I will get the information about me in JSON format.
# This atomatically came as in the first step i use --reload while running the server.So server restarts after code change, and new endpoint is also available without restarting the server manually.

# Also , if i go to my url and add /docs at the end of the URL, I will get the automatic interactive API documentation (provided by Swagger UI) where I can see all the available endpoints and even test them out directly from the browser. FastAPI automatically generates this documentation for you based on your code.
