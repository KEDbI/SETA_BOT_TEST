from aiogram import Bot
from aiogram.types import BotCommand


commands = {
    '/start': 'Начало работы с ботом',
    '/help': 'Просмотр доступных команд',
    '/echo': 'Отправка копии сообщения пользователя',
    '/photo': 'Вывод размеров фото',
    '/users': 'Вывод всех пользователей',
    '/weather': 'Вывод погоды',
}


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in commands.items()
    ]
    await bot.set_my_commands(main_menu_commands)
