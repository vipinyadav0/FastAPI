
from typing import Optional
from xmlrpc.client import Boolean
from fastapi import FastAPI
from fastapi.params import Body

from random import randrange

from pydantic import BaseModel # to create schema

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    
    rating : Optional[int] = None
    
my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, 
            {"title": "my first post", "content": "this post is about my dog", "id": 2}]

@app.get("/")
async def root():
    return {"message": "Welcome to my first API here in bangalore"}

@app.get("/posts")
def post():
    # return {"data: Here is your post"}
    return {"data": my_posts}



@app.post("/createpost")  # though not the best practice to create post routing
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
    print(post_data.published)
    print(post_data.rating)
    
    print(post_data.dict())  #converting data into dictionary
    # return {"Data : Post created"}
    # return {"data" : "NewPost"}
    return {"Data" : post_data}



@app.post("/posts")
def userpost(post_data: Post):
    post_dict = post_data.dict()
    post_dict['id'] = randrange(0,1000000) 
    my_posts.append(post_dict)
    return {"Data" : post_dict}

@app.get("/posts{id}")
def get_post(id):
    print(id)
    return {"Post_datail" : f"here is the post {id}"}
    ...