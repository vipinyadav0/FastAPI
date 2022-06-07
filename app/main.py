
from typing import Optional
from xmlrpc.client import Boolean
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from random import randrange
from pydantic import BaseModel # to create schema

from sqlalchemy.orm import Session

from . import models #import models to make queries to it 
from .database import engine, get_db

models.Base.metadata.create_all(bind =engine)

app = FastAPI()


class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    
    rating : Optional[int] = None
    
# Connecting to Databse
while True:
    try:
        conn = psycopg2.connect(host= 'localhost' , dbname='FastAPI_db', user='postgres', password='postgres123',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to database")  
        break  
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        time.sleep(1)

my_posts = [{"title":"title of post 1", "content":"content of post 1", "id":1}, 
            {"title": "my first post", "content": "this post is about my dog", "id": 2}]

@app.get("/")
async def root():
    return {"message": "Welcome to my first API here in bangalore"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    # return {"status": "success", "data": {"posts": [post.to_dict() for post in posts]}}
    return {"data": posts}

@app.get("/posts")
def post(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM dbposts") 
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    # return {"data: Here is your post"}
    return {"data": posts} 

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        
def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i




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



@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_post(post_data: Post):
    
    #inserting via cursor
    cursor.execute("INSERT INTO dbposts (title, content, published) VALUES (%s, %s, %s) RETURNING * " , (post_data.title, post_data.content, post_data.published))
    new_post = cursor.fetchone()
    conn.commit()
    # print(posts)
    # return {"Data : Post created"}
    return {"Data" : new_post}
    
    
    # inserting via postman
    
    # post_dict = post_data.dict()
    # post_dict['id'] = randrange(0,1000000) 
    # my_posts.append(post_dict)
    # print(my_posts)
    # return {"Data" : post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    
    cursor.execute("SELECT * FROM dbposts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
        
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} was not found"}
    # return {"Post_datail" : f"here is the post {id}"}
    return {"Post Details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute("DELETE FROM dbposts WHERE id = %s returning *", (id,))
    
    deleted_post = cursor.fetchone()
    conn.commit()
    
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found")
    
    # return {"message": f"post with {id} was deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE dbposts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    # return {"message": f"post with {id} was updated"}
    return {"Post Details": updated_post}

#this is modified in database branch