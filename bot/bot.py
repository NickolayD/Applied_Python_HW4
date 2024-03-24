import asyncio
import config
import requests
import json
import numpy as np
import os
from aiogram import Dispatcher, Bot, types, F
from aiogram.filters.command import Command
from aiogram.types import Message
from io import BytesIO
from PIL import Image
from skimage import color
from skimage.feature import hog


bot = Bot(config.TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}!"
        "\nОтправь мне фото и получишь предсказание."
    )


@dp.message(Command("check_service"))
async def check_service(message: Message):
    r = requests.get(
        config._APP_ADRESS
    )
    if r.status_code == 200:
    	await message.answer("Сервис работает исправно!")
    else:
        await message.answer("Что-то пошло не так.")

@dp.message(F.text)
async def text_handler(message: Message):
    await message.reply("Это не фотография!")


@dp.message(F.photo)
async def predict_by_photo(message: Message, bot: Bot):
    io = BytesIO()
    await bot.download(
        message.photo[-1],
        destination=io
    )
    image = Image.open(io)
    fd = hog(color.rgb2gray(image.resize((224, 224))), 
             orientations=8, 
             pixels_per_cell=(16,16), 
             cells_per_block=(4, 4), 
             block_norm= 'L2'
         )
    fd = fd.reshape((fd.shape[0],))
    r = requests.post(
        config._APP_ADRESS+"/predict", 
        data=json.dumps({"array": list(fd)})
    )
    await message.answer(r.text)


async def main() -> None:    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
   

if __name__ == '__main__':
    asyncio.run(main())
