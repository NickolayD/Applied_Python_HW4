from config import model, veg_dict
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import uvicorn

class MyArr(BaseModel):
    array: List[float]

app = FastAPI()


@app.get('/')
async def homepage():
    return {"Status": "Everything is OK!"}

@app.post('/predict')
async def make_prediction(obj: MyArr):
    prediction = model.predict([obj.array])
    return {
        "Vegetable": veg_dict[prediction[0]],
        }
    
if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=5001)
