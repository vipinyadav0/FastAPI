from ast import Str
from xmlrpc.client import Boolean
from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel # to create schema

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str

@app.get("/")
async def root():
    return {"message": "Welcome to my first API here in bangalore"}

@app.get("/post")
def post():
    return {"data: Here is your post"}

@app.post("/createpost")
def userpost(payLoad: dict = Body(...)):                 # Extract Data that we send in Body section 
    print(payLoad)
    # return {"Data : Post created"}
    return { "New_Post" : f"title: {payLoad['title']}, content: {payLoad['content']}"}

# Data we want for a specific post request
# 1. Title i.e string (str) , 2. Content i.e string(str)


# Instead of extracting data i.e Payload

@app.post("/makepost")
def userpost(post_data : Post):                 # Extract Data that we send in Body section 
    print(post_data)
    print(post_data.title)
    
    
    # return {"Data : Post created"}
    return {"data" : "NewPost"}