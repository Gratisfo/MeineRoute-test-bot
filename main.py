from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import geopy
from geopy.geocoders import Nominatim
import logging

# Здесь необходимо вставить ваш токен Telegram Bot API
API_TOKEN = '...'

# настройки логгирования
logging.basicConfig(level=logging.INFO)

# создание экземпляра бота
bot = Bot(token=API_TOKEN)

# создание экземпляра диспетчера и установка хранилища состояний
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)

# создание группы состояний для обработки событий, связанных с локацией пользователя
class Location(StatesGroup):
    waiting_for_location = State()


# обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Этот обработчик отправляет пользователю приветственное сообщение
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text="Список всех баров", callback_data='list_all_bars')
    button2 = InlineKeyboardButton(text="Бары рядом", callback_data='nearby_bars')
    keyboard.add(button1, button2)
    #
    # await message.answer("Привет, этот бот предназначен для знакомства с барной культурой Петербурга.\nЧто умеет этот бот:", reply_markup=keyboard)
    # await message.delete()

    # отправляем приветственное сообщение и сохраняем его идентификатор
    welcome_message = await message.answer(
        "Привет, этот бот предназначен для знакомства с барной культурой Петербурга.\nЧто умеет этот бот:",
        reply_markup=keyboard)
    welcome_message_id = welcome_message.message_id



@dp.callback_query_handler(text='list_all_bars')
async def process_callback_list_all_bars(callback_query: types.CallbackQuery):
    """
    Этот обработчик отправляет пользователю список всех адресов баров
    """
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Список всех баров: улица Пушкина колотушкина 10, улица Баранкина 12')
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import geopy
from geopy.geocoders import Nominatim
import logging

# Здесь необходимо вставить ваш токен Telegram Bot API
API_TOKEN = '5979420055:AAFI7tVXEdzc_YL-OP2SumMQBjYGhb4PuLk'

# настройки логгирования
logging.basicConfig(level=logging.INFO)

# создание экземпляра бота
bot = Bot(token=API_TOKEN)

# создание экземпляра диспетчера и установка хранилища состояний
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)

# создание группы состояний для обработки событий, связанных с локацией пользователя
class Location(StatesGroup):
    waiting_for_location = State()


# обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Этот обработчик отправляет пользователю приветственное сообщение
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text="Список всех баров", callback_data='list_all_bars')
    button2 = InlineKeyboardButton(text="Бары рядом", callback_data='nearby_bars')
    keyboard.add(button1, button2)
    #
    # await message.answer("Привет, этот бот предназначен для знакомства с барной культурой Петербурга.\nЧто умеет этот бот:", reply_markup=keyboard)
    # await message.delete()

    # отправляем приветственное сообщение и сохраняем его идентификатор
    welcome_message = await message.answer(
        "Привет, этот бот предназначен для знакомства с барной культурой Петербурга.\nЧто умеет этот бот:",
        reply_markup=keyboard)
    welcome_message_id = welcome_message.message_id



@dp.callback_query_handler(text='list_all_bars')
async def process_callback_list_all_bars(callback_query: types.CallbackQuery):
    """
    Этот обработчик отправляет пользователю список всех адресов баров
    """
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Список всех баров: улица Пушкина колотушкина 10, улица Баранкина 12')

@dp.callback_query_handler(text='nearby_bars')
async def process_callback_nearby_bars(callback_query: types.CallbackQuery):
    """
    Этот обработчик запрашивает у пользователя геолокацию
    """
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Отправьте свою текущую локацию', reply_markup=types.ReplyKeyboardRemove())
    await Location.waiting_for_location.set()

# обработчик сообщений с локацией пользователя
@dp.message_handler(content_types=types.ContentType.LOCATION, state=Location.waiting_for_location)
async def process_location(message: types.Message, state: FSMContext):
    """
    Этот обработчик получает локацию пользователя и находит бары, находящиеся в радиусе 500 метров от него
    """
    # получаем координаты пользователя
    latitude = message.location.latitude
    longitude = message.location.longitude
    # инициализируем объект геокодера
    geolocator = Nominatim(user_agent="my_app")

    # получаем название улицы, на которой находится пользователь
    location = geolocator.reverse(f"{latitude}, {longitude}")
    address = location.raw['address']
    street = address.get('road')

    # получаем список баров рядом с пользователем
    nearby_bars = ["Бар на улице Пушкина, д. 10", "Бар на улице Баранкина, д. 12"]

    # формируем сообщение для отправки пользователю
    if len(nearby_bars) > 0:
        message_text = f"Список баров на улице {street}:\n\n"
        for bar in nearby_bars:
            message_text += f"• {bar}\n"
    else:
        message_text = f"К сожалению, на улице {street} баров не найдено."

    # отправляем сообщение пользователю
    await message.answer(message_text, reply_markup=types.ReplyKeyboardRemove())

    # завершаем состояние ожидания локации пользователя
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
@dp.callback_query_handler(text='nearby_bars')
async def process_callback_nearby_bars(callback_query: types.CallbackQuery):
    """
    Этот обработчик запрашивает у пользователя геолокацию
    """
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Отправьте свою текущую локацию', reply_markup=types.ReplyKeyboardRemove())
    await Location.waiting_for_location.set()

# обработчик сообщений с локацией пользователя
@dp.message_handler(content_types=types.ContentType.LOCATION, state=Location.waiting_for_location)
async def process_location(message: types.Message, state: FSMContext):
    """
    Этот обработчик получает локацию пользователя и находит бары, находящиеся в радиусе 500 метров от него
    """
    # получаем координаты пользователя
    latitude = message.location.latitude
    longitude = message.location.longitude
    # инициализируем объект геокодера
    geolocator = Nominatim(user_agent="my_app")

    # получаем название улицы, на которой находится пользователь
    location = geolocator.reverse(f"{latitude}, {longitude}")
    address = location.raw['address']
    street = address.get('road')

    # получаем список баров рядом с пользователем
    nearby_bars = ["Бар на улице Пушкина, д. 10", "Бар на улице Баранкина, д. 12"]

    # формируем сообщение для отправки пользователю
    if len(nearby_bars) > 0:
        message_text = f"Список баров на улице {street}:\n\n"
        for bar in nearby_bars:
            message_text += f"• {bar}\n"
    else:
        message_text = f"К сожалению, на улице {street} баров не найдено."

    # отправляем сообщение пользователю
    await message.answer(message_text, reply_markup=types.ReplyKeyboardRemove())

    # завершаем состояние ожидания локации пользователя
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
