from environs import Env
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.client.bot import DefaultBotProperties
from handlers import user_handlers

from services.services import start_scheduler
from keyboards.set_menu import set_main_menu


async def main() -> None:
    env: Env = Env()
    env.read_env()
    bot: Bot = Bot(token=env('TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
    dp: Dispatcher = Dispatcher()

    await start_scheduler(bot)
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling1
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
