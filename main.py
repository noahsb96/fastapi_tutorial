from fastapi import FastAPI

app = FastAPI()

# @app.get("/items/{item_id}") # value of path parameter item_id will be passed to 
# async def read_item(item_id: int): # this function as the argument item_id
#     return {"item_id": item_id} # run this function, start uvicorn and go to http://127.0.0.1:8000/items/foo to see response
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

# @app.get("/users")
# async def read_users():
#     return ["Rick", "Morty"]


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

# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item

# If you go to http://127.0.0.1:8000/items/foo?short=1, http://127.0.0.1:8000/items/foo?short=True, http://127.0.0.1:8000/items/foo?short=true, http://127.0.0.1:8000/items/foo?short=on, http://127.0.0.1:8000/items/foo?short=yes or any other case variation, your function will see the parameter short as True. Otherwise as False

# This example is giving a short description, i.e. the item id in the query parameter, if the string short is in the path. Otherwise, the item will have the long description.

# You can declare multiple path parameters and query parameters at the same time. FastAPI will know inherently which is which. You also don't have to declare them in a specific order. They're detected by name.

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# This link will show this in action http://127.0.0.1:8000/users/1/items/foo?short=True

# When you declare a default value for non-path parameters then it isn't required
# If you don't want to add a specific value but just make it optional, you set the default as None
# But when you want to make a query parameter required, you can just not declare any default value

# @app.get("/items/{item_id}")
# async def read_user_item(item_id: str, needy: str):
#     item = {"item_id": item_id, "needy": needy}
#     return item

# The query parameter needy, which is a string, is required
# if you go to http://127.0.0.1:8000/items/foo-item you will get an error
# Since needy is required, you would just need to set that parameter in the URL like this: http://127.0.0.1:8000/items/foo-item?needy=sooooneedy

# You can also define a required, default and optional query parameter at the same time

@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

# needy is required, skip is an int with a default value of 0 and limit is optional and is an int
# This demonstrates all of this: http://127.0.0.1:8000/items/foo-item?needy=sooooneedy&limit=10&skip=20

# First import BaseModel from pydantic
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# @app.post("/items/")
# async def create_item(item: Item):
#     return item

# When a model has a default value, it isn't required, otherwise it is required. Making an attribute have the value of None will make it optional
# When you want to add it to your path operation, declare it the same way with path and query parameters
# Declare its type as the model you created, Item
# With the python type declaration, FastAPI will,
    # Read the body of the request as JSON.
    # Convert the corresponding types (if needed).
    # Validate the data.
        # If the data is invalid, it will return a nice and clear error, indicating exactly where and what was the incorrect data.
    # Give you the received data in the parameter item.
        # As you declared it in the function to be of type Item, you will also have all the editor support (completion, etc) for all of the attributes and their types.
    # Generate JSON Schema definitions for your model, you can also use them anywhere else you like if it makes sense for your project.
    # Those schemas will be part of the generated OpenAPI schema, and used by the automatic documentation UIs.
# The JSON Schemas of your models will be in the OpenAPI generated schema and will be shown in the interactive API docs
# In VSCode, you will also get type hints and completion in the function. This wouldn't happen if a dict was received instead of a Pydantic model
# You will also get error checks
# The whole FastAPI framework was built around this design and was tested to make sure it worked with all editors

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump() # docs say to use dict but VSCode says to use model_dump. Have to research what this is
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Taken from stack overflow: Note that Pydantic models can also be converted to dictionaries using dict(model). With this approach the raw field values are returned, so sub-models will not be converted to dictionaries. Either .model_dump() or dict(model) will provide a dict of fields, but .model_dump() can take numerous other arguments—such as mode, for instance, which is useful when dealing with non-JSON serializable objects (see the relevant documentation)—as well as will recursively convert nested models into dicts.

# You can declare path parameters and request body at the same time
# FastAPI recognizes that function parameters that match path parameters should be taken from the path and function parameters that are declared to be Pydantic models should be taken from the request body

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.model_dump()}

# You can also declare body, path and query parameters, all at the same time
# FastAPI will recognize each of them and take the data from the correct place

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

# The function parameters will be as follows:
# If the parameter is also declared in the path, it will be used as a path parameter.
# If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
# If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.

# FastAPI allows you to declare additonal information and validation for your parameters

# @app.get("/items/")
# async def read_items(q: str | None = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.upfate({"q": q})
#     return results

# The query parameter q is of type Union[str, None] (or str | None in Python 3.10), that means that it's of type str but could also be None, and indeed, the default value is None, so FastAPI will know it's not required.

# We are going to enforce that even though q is optional, whenever it is provided, its length doesn't exceed 50 characters

# To achieve this, we have to import 2 things:
from fastapi import Query
from typing import Annotated

# In Python 3.9 or above, Annotated is part of the standard library, so you can import it from typing

# @app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# We used Annotated  to add metadata to parameters in Python Types Intro, here's how we use it with FastAPI

# The default value is still None, so the parameter is still optional
# Having Query(max_length=50) inside of annotated, we are telling FastAPI that we want this value extracted from the query parameters. This would have been the default anyway but we also want additonal validation for this value. This is the reason we do this, for the additional validation.
# FastAPI will validate the data making sure the max length is 50 characters. It will also show a clear error for the client when the data isn't valid. Also FastAPI will document the parameter in the OpenAPI schema path operation so it will show up in the automatic docs UI

# Previous versions of FastAPI required you to use Query as the default value of your parameter instead of putting it in Annotated. There's a high chance of seeing code around it so this is the explanation:
# This is how to use Query() as the defualt value of the function parameter to set the max_length to 50

# @app.get("/items/")
# async def read_items(q: str | None = Query(default=None, max_length=50)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# In this case without using Annotated, we replace the default value None in the function with Query(). Then set the default Value with the parameter Query(default=None). This serves the same purpose of defining the default value
# q: Union[str, None] = Query(default=None) makes the parameter optional with a default value of None, same thing as q: Union[str, None] = None
# In Python 3.10 and up, q: str | None = Query(default=None) is the same as q: str | None = None but it's explicitly a query parameter
# You then pass more parameters to Query, like max_length that applies to strings
# This validates the data and shows a clear error when the data isn't valid, then documents the parameter in the OpenAPI schema path operation

# When using Query inside Annotated, you cannot use the default parameter for Query
# You would use the actual default value of the function parameter. Otherwise it wouldn't be consistent
# q: Annotated[str, Query(default="rick")] = "morty" wouldn't be allowed because it isn't clear if the default value should be "rick" or "morty"
# instead, you would use q: Annotated[str, Query()] = "rick"
# in older code, you would see q: str = Query(default="rick")

# Using Annotated is recommended instead of the default value in function parameters
# The default value of the function parameter is the actual default value
# You could call that same function in other places without FastAPI and it would work as expected. If there's a required parameter without a default value, VSCode would let you know with an error. Python would also let you know this.
# When Annotated isn't used and the old default value style is, when you call that function without FastAPI elsewhere, you'd have to remember to pass the arguments to the function for it to work. Otherwise the values would be different than expected and VSCode and Python wouldn't say anything. You'd only know when the operations error out.

# We can also add a min_length parameter

# @app.get("/items/")
# async def read_items(
#     q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# We can define a regular expression pattern that the parameter should match

# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
#     ] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# ^ starts with the following characters and doesn't have characters before
# fixedquery has the exact value of fixedquery
# $ ends there and doesn't have anymore characters after fixedquery
# You can use regex directly in FastAPI
# Using the parameter regex="^fixedquery$" is deprecated

# You can use default values other than None
# if we wanted to declare the q query parameter to have a min_length of 3 and to have a default value of fixedquery

# @app.get("/items/")
# async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# When we don't need to declare more validations or metadata, we can make the q query parameter required not just by setting a default value to q like q:str instead of q: Union[str, None] = None
# We can now declare it with Query like q: Annotated[Union[str, None], Query(min_length=3)] = None
# So if we need to declare a value as required while using Query, you just don't declare a default value

# @app.get("/items/")
# async def read_items(q: Annotated[str, Query(min_length=3)]):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# There's another way to explicitly declare a required value. You set the default to the literal value ...
# @app.get("/items/")
# async def read_items(q: Annotated[str, Query(min_length=3)] = ...):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# The elipses lets FastAPI know that the parameter is required

# You can declare that a parameter accepts None but that it's still required. This forces the clients to send a value even if the value is None
# You would just declare None is a valid type but use the elipses as the default
# @app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(min_length=3)] = ...):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# When a query parameter is explicity defined with Query you can also declare it to receive a list or multiple values
# To declare a query parameter q that can appear multiple times in the URL, you can write:
# @app.get("/items/")
# async def read_items(q: Annotated[list[str] | None, Query()] = None):
#     query_items = {"q": q}
#     return query_items

# Then when you go to http://localhost:8000/items/?q=foo&q=bar
# You would get multiple q query parameter values (foo and bar) in a list inside your path operation function, in the function parameter q
# The response to the URL would be:
# {
#   "q": [
#     "foo",
#     "bar"
#   ]
# }
# and the API docs would update accordingly to allow multiple values

# You can also define a default list of values if it isn't provided
# @app.get("/items/")
# async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
#     query_items = {"q": q}
#     return query_items
# Then if you went to http://localhost:8000/items/
# The default of q will be ["foo", "bar"] and the response would be the same as above

# You can also just write list instead of just using List[str] or list[str] in Python 3.9+
@app.get("/items/")
async def read_items(q: Annotated[list, Query()] = []):
    query_items = {"q": q}
    return query_items