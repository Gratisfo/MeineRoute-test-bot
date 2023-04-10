import pytest
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.testing import MockBot, MockUser, MockMessage, MockCallbackQuery
from aiogram.utils.emoji import emojize

from your_module import (
    process_callback_list_all_bars,
    process_callback_nearby_bars,
    process_location,
    Location
)

# инициализируем тестового пользователя и бота
user = MockUser(id=1, first_name="Test", username="test_user")
bot = MockBot()

# тест для обработчика list_all_bars
def test_process_callback_list_all_bars():
    # создаем тестовый CallbackQuery
    callback_query = MockCallbackQuery(data="list_all_bars", from_user=user)

    # вызываем обработчик
    process_callback_list_all_bars(callback_query)

    # проверяем, что бот отправил правильное сообщение
    messages = bot.sent_messages
    assert len(messages) == 1
    assert messages[0]["text"] == "Список всех баров: улица Пушкина колотушкина 10, улица Баранкина 12"

# тест для обработчика nearby_bars
def test_process_callback_nearby_bars():
    # создаем тестовый CallbackQuery
    callback_query = MockCallbackQuery(data="nearby_bars", from_user=user)

    # вызываем обработчик
    process_callback_nearby_bars(callback_query)

    # проверяем, что бот отправил правильное сообщение
    messages = bot.sent_messages
    assert len(messages) == 1
    assert messages[0]["text"] == "Отправьте свою текущую локацию"

# тест для обработчика сообщений с локацией
@pytest.mark.asyncio
async def test_process_location():
    # создаем тестовое сообщение с локацией
    location = types.Location(latitude=55.753215, longitude=37.622504)
    message = MockMessage(location=location, from_user=user)

    # вызываем обработчик
    state = FSMContext()
    await process_location(message, state)

    # проверяем, что бот отправил правильное сообщение
    messages = bot.sent_messages
    assert len(messages) == 1
    assert "Список баров на улице" in messages[0]["text"]

    # проверяем, что состояние FSMContext было завершено
    assert state.current_state() is None
