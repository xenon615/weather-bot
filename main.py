import requests
import datetime
# import logging
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

# logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привіт! Напиши мені назву міста і я надішлю тобі погоду на сьогодні!")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear":"Ясно \U00002600",
        "Clouds":"Хмарно \U00002601",
        "Rain":"Дощ \U00002614",
        "Drizzle":"Дощ \U00002614",
        "Thunderstorm":"Гроза \U000026A1",
        "Show":"Сніг \U0001F328",
        "Mist":"Туман \U0001F328"
    }
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Сам подивись що відбувається, не зрозумію що за погода!"


        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(
            f"----------{datetime.datetime.now().strftime('%Y-%m-%d--%H:%M')}-----------\n"
            f"Погода в місті:  {city}\nТемпература повітря:  {cur_weather} C° {wd}\n"
            f"Вологість:  {humidity} %\nТиск:  {pressure} гПа\nВітер:  {wind} км/год\n"
            f"Схід сонця:  {sunrise_timestamp}\nЗахід сонця:  {sunset_timestamp}\nТривалість дня:  {lenght_of_the_day}\n"
            f"-------------Гарного дня !-------------")



    except:
        await message.reply('\U00002620 Перевірте назву міста \U00002620')

executor.start_polling(dp)



