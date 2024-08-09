import requests

from aiogram import Bot
from aiogram.types import Message
from environs import Env
from database.database import Database
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


def get_photo_size(message: Message) -> str:
    width = message.photo[-1].width
    height = message.photo[-1].height
    return f'{width}x{height}'


def get_photo_as_file_size(message: Message) -> str:
    width = message.document.thumbnail.width
    height = message.document.thumbnail.height
    return f'{width}x{height}'


def get_weather(message: Message) -> str:
    env: Env = Env()
    env.read_env()
    api = env('WEATHER_API')
    weather_data = requests.get(f'https://ru.api.openweathermap.org/data/2.5/weather?q={message.text}&units=metric'
                                f'&appid={api}&lang=ru').json()
    if int(weather_data['cod']) == 200:
        return (f'Страна: {weather_data['sys']['country']}\n'
                f'Город: {weather_data['name']}\n'
                f'Погода: {weather_data['main']['temp']}°C, {weather_data['weather'][0]['description']}, '
                f'ветер {weather_data['wind']['speed']}м/с')
    elif int(weather_data['cod']) == 404:
        return 'Город с таким названием не найден!'
    else:
        raise Exception(f'Код ошибки: {weather_data['cod']}, сообщение: {weather_data['message']}')


async def start_scheduler(bot: Bot) -> None:
    # эту функцию и функцию ниже, наверное, можно было бы вынести в отдельный модуль
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_scheduled_message, trigger='cron', hour=9, minute=0, start_date=datetime.now(),
                      args=(bot,))
    scheduler.start()


async def send_scheduled_message(bot: Bot) -> None:
    id_list = Database().get_ids()
    for chat_id in id_list:
        await bot.send_message(chat_id=chat_id, text='Не забудьте проверить уведомления!')
