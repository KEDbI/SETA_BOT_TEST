from aiogram.types import Message


def check_name(message: Message) -> bool:
    if message.text.isalpha():
        return True
    return False


def check_age(message: Message) -> bool:
    if message.text.isdigit():
        return True
    return False
