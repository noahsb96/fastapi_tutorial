from fastapi import FastAPI

app = FastAPI()

# @app.get("/items/{item_id}") # value of path parameter item_id will be passed to 
# async def read_item(item_id: int): # this function as the argument item_id
#     return {"item_id": item_id} # run this function, start uvicorn and go to http://127.0.0.1:8000/items/foo to see response
# # returns {"item_id": "foo"}

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
class ModelName(str, Enum): # sub class that that inherits from str and from Enum
                            # When inheriting from str, the API docs will know that the values must be a string and will render correctly
    alexnet = "alexnet" # Attributes will have fixed values, which will be the available valid values
    resnet = "resnet"
    lenet = "lenet"

# The value of the path parameter will be an enumeration member
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet: # This compares the model_name in the path parameter to the enumeration member in the ModelName
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet": # You can also get the model_name in the path parameter and check the value in the enumeration member
        return {"model_name": model_name, "message": "leCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"} # All the return statements return the enum mebers from your path operation, even nested in a JSON body
                                                                        # They will then be converted to their values, like strings in this case, before returning to the client

# The available values for the path parameter are predefined so the docs can show them nicely
# Going here shows this: http://127.0.0.1:8000/docs#/default/get_model_models__model_name__get

# If you have a path operation with a path of /files/{file_path} but the file_path contains a path of home/johndoe/myfile.txt so the full path would be /files/home/johndoe/myfile.txt
# OpenAPI does not support a way to declare a path parameter inside because they're difficult to test and define
# You can accomplish this in FastAPI using an internal tool from Starlette
# The docs would still work if you did this but would not have any documentation saying that parameter should contain a path

# Using an option directly from Starlette, you can declare a path parameter containing a path using /files/{file_path:path}
# The name of this parameter would be file_path and the :path part would tell it that the parameter should match any path
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}\
    
# When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.
# For example, in the URL: http://127.0.0.1:8000/items/?skip=0&limit=10
# skip: with a value of 0
# limit: with a value of 10
# As they are part of the URL, they are "naturally" strings.
# But when you declare them with Python types (in the example above, as int), they are converted to that type and validated against it.

# Query Parameters aren't fixed parts of a path so they are optional and you can set default values on them.
# The first example have default values of skip = 0 and limit = 10
# Going to http://127.0.0.1:8000/items/ is the same as going to http://127.0.0.1:8000/items/?skip=0&limit=10
# But going to http://127.0.0.1:8000/items/?skip=20 would make skip = 20 and limit = 10

# You can declare optional query parameters by setting the default value to None

# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# If you go to http://127.0.0.1:8000/items/foo?short=1, http://127.0.0.1:8000/items/foo?short=True, http://127.0.0.1:8000/items/foo?short=true, http://127.0.0.1:8000/items/foo?short=on, http://127.0.0.1:8000/items/foo?short=yes or any other case variation, your function will see the parameter short as True. Otherwise as False

# This example is giving a short description, i.e. the item id in the query parameter, if the string short is in the path. Otherwise, the item will have the long description.

