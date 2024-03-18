from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}") # value of path parameter item_id will be passed to 
async def read_item(item_id: int): # this function as the argument item_id
    return {"item_id": item_id} # run this function, start uvicorn and go to http://127.0.0.1:8000/items/foo to see response
# returns {"item_id": "foo"}

# if you run this example at http://127.0.0.1:8000/items/3
# returns {"item_id": 3}
# if I go to http://127.0.0.1:8000/items/foo or http://127.0.0.1:8000/items/4.2, I get HTTP error
# Going to http://127.0.0.1:8000/docs gets automatic, interactive, API documentation
# Going to http://127.0.0.1:8000/redoc gets alternative API documentaion using ReDoc

# When creating path operations, you may have a fixed path, like the example below where we want to get data about the current user
# You then have a path to get data about a specific user with a user ID
# The path for the current user needs to be before the path for the user id path because path operations are evaluated in order
# If the user ID path was before the current user path, the user id path would match also for the current user path because it thinks that it's receiving a "user_id" parameter with a value of "me"

@app.get("/users/me")
async def read_user_me():
    return {"current user": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# You also cannot redefine a path operation

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]

# The first path will always be used since the path matches first

from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "leCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}