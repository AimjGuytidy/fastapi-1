from typing import Optional
from fastapi import FastAPI,requests,HTTPException,status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from starlette.responses import Response

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

my_post = [{"title":"post 1","content":"this is the first post","id":1},{"title":"post 2","content":"this is the second post","id":2}]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

def find_index(id):
    for i,p in enumerate(my_post):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"message":"Hello World!"}
#min 47:35

"""
@app.get("/posts")
async def get_posts():
    return {"data":"this is a post"}
"""

@app.get("/posts")
async def get_posts():
    return {"data":my_post}

"""
@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"}
"""

"""
@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post.rating)
    return {"posty": "new post"}
"""

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_post.append(post_dict) 
    return {"posty": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    posty = find_post(id)
    if not posty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"this id {id} is not available")
    return {"data":posty}
#1:48:12

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    index = find_index(id)
 
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'this id {id} is not available')

    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'this id {id} is not available')
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_post[index] = post_dict
    return {"updated data":post_dict}