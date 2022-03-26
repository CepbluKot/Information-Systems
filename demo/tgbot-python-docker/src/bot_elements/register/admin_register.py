""" Система регистарции студентов, преподов, админов"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


async def talking_ben(message: types.Message):
    """ Ben"""
    await message.answer('HO HO HO\nNO')


def register_handlers_register_admin(dp: Dispatcher):
    dp.register_message_handler(
        talking_ben, commands='register')
