from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from FSM.fsm import FillForm, Echo, Photo, Weather
from keyboards.inline import inline_kb
from keyboards.reply import get_reply_keyboard
from filters import filter
from database.database import Database
import sqlite3
import logging
from services.services import get_photo_size, get_photo_as_file_size, get_weather


logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO',
                    format='#%(levelname)-8s [%(asctime)s] %(filename)s: %(lineno)d - %(name)s - %(message)s',
                    filename='logs.log')

router: Router = Router()


@router.message(StateFilter(None), F.text.lower() == 'отмена')
async def process_cancel_button_none_state(message: Message, state: FSMContext) -> None:
    await state.set_data({})
    await message.answer(text='Нечего отменять')


@router.message(F.text.lower() == 'отмена')
async def process_cancel_button(message: Message, state: FSMContext) -> None:
    # Срабатывает, когда пользователь находится в состоянии != None, возвращает пользователя в состояние None
    await state.set_data({})
    await state.set_state(None)
    await message.answer(text='Действие отменено')


@router.message(StateFilter(None), CommandStart())
async def process_start_command(message: Message) -> None:
    logger.info(f'User id: {message.from_user.id}, Process start command')
    await message.answer('Добро пожаловать в наш бот!')


@router.message(StateFilter(None), Command(commands='help'))
async def process_help_command(message:Message) -> None:
    logger.info(f'User id: {message.from_user.id}, Process help command')
    await message.answer('Доступные команды: /start, /help, /echo, /photo, /users, /weather, задание 3, задание 4')


@router.message(StateFilter(None), Command(commands='echo'))
async def process_echo_command(message: Message, state: FSMContext) -> None:
    logger.info(f'User id: {message.from_user.id}, Process echo command')
    await message.answer('Напишите мне что-нибудь и в ответ я пришлю Ваше сообщение',
                         reply_markup=get_reply_keyboard(['Отмена']))
    await state.set_state(Echo.echo)


@router.message(StateFilter(Echo.echo))
async def send_echo(message: Message, state: FSMContext) -> None:
    logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, sending echo')
    await message.send_copy(chat_id=message.chat.id)
    await state.set_state(None)
    logger.info(f'State: {await state.get_state()}, echo has been sent')


@router.message(StateFilter(None), Command(commands='photo'))
async def process_photo_command(message: Message, state: FSMContext) -> None:
    logger.info(f'User id: {message.from_user.id}, Process photo command')
    await message.answer('Пришлите фото, а я пришлю Вам его размер', reply_markup=get_reply_keyboard(['Отмена']))
    await state.set_state(Photo.get_photo)


@router.message(StateFilter(Photo.get_photo), F.photo)
async def send_photo_size(message: Message, state: FSMContext) -> None:
    # срабатывает только на сжатое фото
    logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, Getting photo size')
    size = get_photo_size(message)
    await message.answer(f'Размер фото: {size}')
    await state.set_state(None)
    logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, Photo size has been sent')


@router.message(StateFilter(Photo.get_photo), F.document)
async def send_photo_size(message: Message, state: FSMContext) -> None:
    # срабатывает только на фото, отправленное как документ; выводит только размер иконки, как вывести размер фото из
    # файл я не разобрался
    logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, Got photo as document,'
                f' getting photo size')
    try:
        size = get_photo_as_file_size(message)
        await message.answer(f'Размер иконки файла: {size}')
        await state.set_state(None)
        logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, Photo size has been sent')
    except:
        await message.answer('Пожалуйста, пришлите фото', reply_markup=get_reply_keyboard(['Отмена']))


@router.message(StateFilter(Photo.get_photo))
async def request_photo(message: Message, state: FSMContext) -> None:
    logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, '
                f'Entered incorrect data (photo requested)')
    await message.answer('Пожалуйста, пришлите фото', reply_markup=get_reply_keyboard(['Отмена']))


@router.message(StateFilter(None), Command(commands='users'))
async def get_all_users(message: Message) -> None:
    logger.info(f'User id: {message.from_user.id}, Process users command')
    db = Database(user_id=message.from_user.id)
    users = db.select_all_users()
    await message.answer(f'Список пользователей: \n'
                         f'{users}')


@router.message(StateFilter(None), Command(commands='weather'))
async def request_city(message: Message, state: FSMContext) -> None:
    logger.info(f'User id: {message.from_user.id}, Process weather command, requesting city')
    await message.answer('Введите город', reply_markup=get_reply_keyboard(['Отмена']))
    await state.set_state(Weather.get_city)


@router.message(StateFilter(Weather.get_city))
async def send_weather(message: Message, state: FSMContext) -> None:
    logger.info(f'User id: {message.from_user.id}, city received, trying to get weather')
    try:
        weather = get_weather(message)
        logger.info(f'{weather}')
        await message.answer(text=f'{weather}')
        await state.set_state(None)
    except:
        logger.exception('error occurred')
        await message.answer('Произошла ошибка, попробуйте позже')
        await state.set_state(None)





@router.message(StateFilter(None), F.text.lower() == 'задание 3')
async def show_inline_kb(message: Message) -> None:
    await message.answer(text='Это инлайн-кнопки. Нажми на любую!', reply_markup=inline_kb)
    logger.info('Show inline keyboard')


@router.callback_query(F.data == 'button1')
async def process_button1_pressed(callback: CallbackQuery) -> None:
    logger.info(f'User id: {callback.from_user.id}, Caught update with callback data "button1"')
    await callback.message.answer('Вы выбрали Выбор 1')
    await callback.answer()


@router.callback_query(F.data == 'button2')
async def process_button2_pressed(callback: CallbackQuery) -> None:
    logger.info(f'User id: {callback.from_user.id} Caught update with callback data "button2"')
    await callback.message.answer('Вы выбрали Выбор 2')
    await callback.answer()


@router.message(StateFilter(None), F.text.lower() == 'задание 4')
async def insert_data(message: Message, state: FSMContext) -> None:
    logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, requesting name')
    await message.answer('Введите имя', reply_markup=get_reply_keyboard(['Отмена']))
    await state.set_state(FillForm.name)


@router.message(StateFilter(FillForm.name), filter.check_name)
async def insert_age(message: Message, state: FSMContext) -> None:
    logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, requesting age')
    await state.update_data(name=message.text)
    await message.answer('Введите возраст (сколько Вам полных лет)', reply_markup=get_reply_keyboard(['Отмена']))
    await state.set_state(FillForm.age)


@router.message(StateFilter(FillForm.name))
async def incorrect_name(message: Message) -> None:
    await message.answer('Неверный формат имени. Введите имя еще раз', reply_markup=get_reply_keyboard(['Отмена']))
    logger.info(f'User id: {message.from_user.id}, entered incorrect age format')


@router.message(StateFilter(FillForm.age), filter.check_age)
async def confirm_data(message: Message, state: FSMContext):
    logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, requesting confirmation')
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    await message.answer(f'Введенные данные:\n'
                         f'Имя: {data['name']}\n'
                         f'Возраст: {data['age']}\n'
                         f'\n'
                         f'Вносим данные в бд?', reply_markup=get_reply_keyboard(['Да', 'Нет', 'Отмена'],
                                                                                 width=2))
    await state.set_state(FillForm.confirm)


@router.message(StateFilter(FillForm.age))
async def incorrect_age(message: Message) -> None:
    await message.answer('Неверный формат возраста. Введите возраст еще раз',
                         reply_markup=get_reply_keyboard(['Отмена']))
    logger.info(f'User id: {message.from_user.id}, Entered incorrect age format')


@router.message(StateFilter(FillForm.confirm), F.text.lower() == 'да')
async def add_userdata_to_db(message: Message, state: FSMContext) -> None:
    db = Database(user_id=message.from_user.id)
    data = await state.get_data()
    try:
        db.insert_user(user_name=data['name'], age=data['age'])
        await message.answer('Данные внесены.')
        await state.set_data({})
        await state.set_state(None)
        logger.info(f'State: {await state.get_state()}, data has been inserted')
    except sqlite3.IntegrityError:
        await message.answer('Пользователь с таким ID уже есть в базе!')
        logger.error(f'User ID {message.from_user.id} already exists!')
        await state.set_data({})
        await state.set_state(None)
    except:
        await message.answer('Произошла ошибка, попробуйте позже')
        logger.exception('Query or connection error')
        await state.set_data({})
        await state.set_state(None)


@router.message(StateFilter(FillForm.confirm), F.text.lower() == 'нет')
async def cancel_inserting_data(message: Message, state: FSMContext) -> None:
    logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, Cancelling inserting data into db')
    await message.answer('Данные не внесены в базу данных')
    await state.set_data({})
    await state.set_state(None)


@router.message(StateFilter(FillForm.confirm))
async def incorrect_answer(message: Message, state: FSMContext) -> None:
    logger.info(f'User id: {message.from_user.id}, State: {await state.get_state()}, Entered incorrect data')
    await message.answer('Введите "да" или "нет"',
                         reply_markup=get_reply_keyboard(['Да', 'Нет', 'Отмена'], width=2))


@router.message(StateFilter(None))
async def process_other_answer(message: Message) -> None:
    await message.answer(text='К сожалению, такой команды я не знаю :(')
