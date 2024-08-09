from aiogram.fsm.state import State, StatesGroup


class FillForm(StatesGroup):
    name: State = State()
    age: State = State()
    confirm: State = State()


class Echo(StatesGroup):
    echo: State = State()


class Photo(StatesGroup):
    get_photo: State = State()


class Weather(StatesGroup):
    get_city: State = State()
