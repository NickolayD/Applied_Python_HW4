from config import model, veg_dict
from fastapi import FastAPI, HTTPException
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
async def predict(obj: MyArr):
    if len(obj.array) != 15488:
        raise HTTPException(
            status_code=1001,
            detail="Wrong data size."
        )
    prediction = model.predict([obj.array])
    return {"Vegetable": veg_dict[prediction[0]]}


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=5001)
