from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}") # value of path parameter item_id will be passed to 
async def read_item(item_id: int): # this function as the argument item_id
    return {"item_id": item_id} # run this function, start uvicorn and go to http://127.0.0.1:8000/items/foo to see response
# returns {"item_id": "foo"}

# if you run this example at http://127.0.0.1:8000/items/3
# returns {"item_id": 3}