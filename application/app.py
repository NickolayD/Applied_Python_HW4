from config import model, veg_dict
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
import os
import uvicorn
import torch


class PostData(BaseModel):
    array: List[float]


app = FastAPI()


@app.get('/')
async def homepage():
    return {"Status": "Everything is OK!"}


@app.post('/predict')
async def predict(obj: PostData):
    # Проверка на наличие файла
    if len(obj.array) != 3 * 224 * 224:
        raise HTTPException(
            status_code=1001,
            detail="Wrong list size."
        )
    # Предсказание модели
    prediction = model(torch.Tensor(obj.array).resize(1, 3, 224, 224))
    # Возвращает класс, вероятность которого максимальна
    return {"Vegetable": veg_dict[prediction.argmax(dim=1).item()]}


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=5001)
