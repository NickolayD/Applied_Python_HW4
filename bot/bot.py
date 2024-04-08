import asyncio
import config
import json
import logging
import requests
import time
from aiogram import Dispatcher, Bot, F
from aiogram.filters.command import Command
from aiogram.types import Message
from io import BytesIO
from PIL import Image
from skimage import color
from skimage.feature import hog

# логирование
logging.basicConfig(level=logging.INFO)
# бот
bot = Bot(config.TOKEN)
# диспетчер
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logging.info(
        f"Start Command: {user_id} {user_name} "
        f"{time.asctime()}."
    )
    await message.answer(config.START_TEXT)


@dp.message(Command("help"))
async def command_help_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logging.info(
        f"Help Command: {user_id} {user_name} "
        f"{time.asctime()}."
    )
    await message.answer(config.HELP_TEXT)


@dp.message(Command("info"))
async def command_info_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logging.info(
        f"Info Command: {user_id} {user_name} "
        f"{time.asctime()}."
    )
    await message.answer(config.INFO_TEXT)


@dp.message(Command("check_service"))
async def command_check_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logging.info(
        f"Check_service Command: {user_id} "
        f"{user_name} {time.asctime()}"
    )
    r = requests.get(
        config._APP_ADRESS
    )
    if r.status_code == 200:
        logging.info("Service is working.")
        await message.answer(config.CHECK_STATUS_OK)
    else:
        logging.info("Some trouble while requesting a service.")
        await message.answer(config.CHECK_STATUS_FAIL)


@dp.message(F.text)
async def text_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logging.info(
        f"Text Handler: {user_id} {user_name} "
        f"{time.asctime()}. Text was sent, photo expected."
    )
    await message.reply(config.REPLY_ON_TEXT)


@dp.message(F.photo)
async def predict_by_photo(message: Message, bot: Bot):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logging.info(
        f"Fhoto Handler: {user_id} {user_name}"
        f"{time.asctime()}. Photo was sent."
    )
    try:
        logging.info("Downloading a photo.")
        io = BytesIO()
        await bot.download(
            message.photo[-1],
            destination=io
        )
        logging.info("Preparing data.")
        # подготовка данных
        image = Image.open(io)
        fd = hog(color.rgb2gray(image.resize((224, 224))),
                 orientations=8,
                 pixels_per_cell=(16, 16),
                 cells_per_block=(4, 4),
                 block_norm='L2'
                 )
        fd = fd.reshape((fd.shape[0],))
        logging.info("Making a prediction.")
        # POST-запрос к сервису
        r = requests.post(
            config._APP_ADRESS+"/predict",
            data=json.dumps({"array": list(fd)})
        )
        # обработка ответа от сервиса
        dct = dict(json.loads(r.text))
        await message.answer(
             config.PREDICT.format(dct["Vegetable"])
        )
    except Exception:
        logging.info("Problem while predicting.")
        await message.answer(config.PREDICTFAIL)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
