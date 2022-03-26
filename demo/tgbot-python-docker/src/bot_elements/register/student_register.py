""" Система регистарции студентов, преподов, админов"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_elements.getter.all_getters import registerData_get_fio, registerData_get_group, registerData_get_role, registerData_check_is_registered

import parsers.prep_text_pars as prep_text_pars

from bot_elements.setter.all_setters import registerData_add_user, registerData_change_fio_data, registerData_change_group_data


all_groups = ['М3О-212Б-20', 'М3О-214Б-20', 'М3О-221Б-20', 'М3О-309Б-19', 'М3О-314Б-19', 'М3О-118М-21', 'М3О-118М-21',
              'М3О-111М-21', 'М3О-111М-21', 'М3О-212Б-20', 'М3О-214Б-20', 'М3О-221Б-20', 'М3О-309Б-19', 'М3О-314Б-19']

class registerUser(StatesGroup):
    " FSM для регистрации пользователя"
    input_fio = State()
    waiting_for_fio = State()
    waiting_for_group = State()


class register_change_group_fsm(StatesGroup):
    " FSM для смены группы пользователя"
    waiting_for_new_group = State()


class register_change_fio_fsm(StatesGroup):
    " FSM для смены ФИО пользователя"
    waiting_for_new_fio = State()


async def strangeMessagesHandler(message: types.Message): # !
    " Фиксит кое какие сообщения"
    if message.text in all_groups or '; id ' in message.text:
        await message.answer('reply keyboard removed', reply_markup=types.ReplyKeyboardRemove())


async def already_registered(message: types.Message, state: FSMContext):
    " Проверяет, зарегистрирован ли пользователь"
    
    if registerData_get_role(user_id=message.chat.id) == 'prepod':
        await message.answer('Препод, топай регаться в свой бот, понятно да')
        return
        
    await message.answer('Вы уже зарегистрированы: ' + '\nВы: ' + str(registerData_get_fio(user_id=message.chat.id)) + '; ' + 'Ваша группа: ' + str(registerData_get_group(user_id=message.chat.id) +' Ваша роль: ' + str(registerData_get_role(message.chat.id))), reply_markup=types.ReplyKeyboardRemove())


    buttons = [
        types.InlineKeyboardButton(
            text="Да", callback_data="register_change_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="register_change_false")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer('Хотите изменить рег. данные?', reply_markup=keyboard)


async def get_fio(message: types.Message, state: FSMContext):
    " (registerUser FSM) Выбираем роль при помощи inline кнопок"
    
    await state.update_data(chosen_role="student")
    await message.answer("Введите ФИО")
    await registerUser.waiting_for_fio.set()


async def choose_fio(message: types.Message, state: FSMContext):
    " (registerUser FSM) Получаем ФИО и (для студентов) предлагаем выбрать группу"
    fio = message.text
    await state.update_data(chosen_fio=fio)
    
    marakap = ReplyKeyboardMarkup(one_time_keyboard=True)

    for data in all_groups:
        marakap.add(KeyboardButton(data))

    await message.reply('Выберите группу', reply_markup=marakap)
    await registerUser.waiting_for_group.set()



async def wrong_group(message: types.Message):
    " (registerUser FSM) Срабатывает, если выбрана неверная группа"
    return await message.reply('Выберите группу из списка')


async def choose_group(message: types.Message, state: FSMContext):
    " (registerUser FSM) Получаем группу и добавляем пользователя в хранилище"
    user_data = await state.get_data()
    
    group = message.text

    await state.update_data(chosen_group=group)
    user_data = await state.get_data()
    await message.answer('Ваше ФИО: ' + user_data['chosen_fio'] + '; Ваша группа: ' + user_data['chosen_group'] + '; Ваша роль: ' + user_data['chosen_role'], reply_markup=types.ReplyKeyboardRemove())

    registerData_add_user(user_id=message.chat.id, chosen_fio=user_data['chosen_fio'], chosen_group=user_data['chosen_group'], chosen_role=user_data['chosen_role'])

    await message.answer('Регистрация завершена', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def register_change_true(call: types.CallbackQuery, state: FSMContext):
    " (already_registered Func) Выбираем какие рег. данные изменить"
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

    buttons = [
        types.InlineKeyboardButton(
            text="ФИО", callback_data="register_change_fio"),
        types.InlineKeyboardButton(
            text="Группу", callback_data="register_change_group")
    ]


    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.answer('Что именно изменить?', reply_markup=keyboard)


async def register_change_false(call: types.CallbackQuery, state: FSMContext):
    " (already_registered Func) Не меняем рег. данные"
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await call.message.answer('Окес, ничего не меняем')


# register_change_fio_fsm.waiting_for_new_fio
async def register_change_fio_set_fio(message: types.Message, state: FSMContext):
    " (register_change_fio_fsm FSM) Получаем новую фамилию и обновляем данные"
    new_fio = message.text
    registerData_change_fio_data(user_id=message.chat.id, new_fio=new_fio)
    await state.finish()
    
    await message.answer('Данные обновлены: ' + '\nВы: ' + str(registerData_get_fio(user_id=message.chat.id)) + '; ' + 'Ваша группа: ' + str(registerData_get_group(user_id=message.chat.id)+' Ваша роль: ' + str(registerData_get_role(user_id=message.chat.id))), reply_markup=types.ReplyKeyboardRemove())

   
# register_change_group_fsm.waiting_for_new_group
async def register_change_group_set_group(message: types.Message, state: FSMContext):
    " (register_change_group_fsm FSM) Получаем новую группу и обновляем данные"
    new_group = message.text
    registerData_change_group_data(user_id=message.chat.id, new_group=new_group)

    await state.finish()
    
    await message.answer('Данные обновлены: ' + '\nВы: ' + str(registerData_get_fio(user_id=message.chat.id)) + '; ' + 'Ваша группа: ' + str(registerData_get_group(user_id=message.chat.id)+' Ваша роль: ' + str(registerData_get_role(user_id=message.chat.id))), reply_markup=types.ReplyKeyboardRemove())


async def register_change_fio(call: types.CallbackQuery, state: FSMContext):
    " (register_change_true Func) Предлагаем ввести новую фамилию"
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await register_change_fio_fsm.waiting_for_new_fio.set()
    await call.message.answer('Введите новые ФИО')


async def register_change_group(call: types.CallbackQuery, state: FSMContext):
    " (register_change_true Func) Предлагаем ввести новую группу"
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    # сделать изменения в бд и проверку, есть ли уже такое
    marakap = ReplyKeyboardMarkup(one_time_keyboard=True)
    for data in all_groups:
        marakap.add(KeyboardButton(data))

    await register_change_group_fsm.waiting_for_new_group.set()
    await call.message.answer('Выберите группу', reply_markup=marakap)


async def cancel_handler(message: types.Message, state: FSMContext):
    """ Отменяет действия в FSM"""
    current_state = await state.get_state()
    print(current_state)
    if current_state is None:
        return
    await state.finish()
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_register_student(dp: Dispatcher):
    dp.register_message_handler(
        already_registered, lambda message: registerData_check_is_registered(message.chat.id), commands='register')
    dp.register_message_handler(get_fio, commands="register", state="*")
    dp.register_message_handler(choose_fio, state=registerUser.waiting_for_fio)
    dp.register_message_handler(
        choose_group, lambda message: message.text in all_groups, state=registerUser.waiting_for_group)

    dp.register_message_handler(
        wrong_group, lambda message: message.text not in all_groups, state=registerUser.waiting_for_group)

    dp.register_message_handler(
        register_change_group_set_group, lambda message: message.text in all_groups, state=register_change_group_fsm.waiting_for_new_group)

    dp.register_message_handler(
        wrong_group, lambda message: message.text not in all_groups, state=register_change_group_fsm.waiting_for_new_group)

    dp.register_message_handler(
        register_change_fio_set_fio, state=register_change_fio_fsm.waiting_for_new_fio)


    dp.register_message_handler(cancel_handler, commands="cancel", state="*")

    dp.register_callback_query_handler(
        register_change_true, text="register_change_true")
    dp.register_callback_query_handler(
        register_change_false, text="register_change_false")
    dp.register_callback_query_handler(
        register_change_fio, text="register_change_fio")
    dp.register_callback_query_handler(
        register_change_group, text="register_change_group")

    dp.register_message_handler(strangeMessagesHandler)