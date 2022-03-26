""" Система регистарции студентов, преподов, админов"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_elements.getter.all_getters import registerData_get_fio, registerData_get_group, registerData_get_role, registerData_check_is_registered

from bot_elements.setter.all_setters import registerData_add_user, registerData_change_fio_data, registerData_change_group_data


all_groups = ['М3О-212Б-20', 'М3О-214Б-20', 'М3О-221Б-20', 'М3О-309Б-19', 'М3О-314Б-19', 'М3О-118М-21', 'М3О-118М-21',
              'М3О-111М-21', 'М3О-111М-21', 'М3О-212Б-20', 'М3О-214Б-20', 'М3О-221Б-20', 'М3О-309Б-19', 'М3О-314Б-19']

class registerUser(StatesGroup):
    " FSM для регистрации пользователя"
    ask_for_fio = State()
    waiting_for_fio = State()


class register_change_fio_fsm(StatesGroup):
    " FSM для смены ФИО пользователя"
    waiting_for_new_fio = State()


async def strangeMessagesHandler(message: types.Message): # !
    " Фиксит кое какие сообщения"
    if message.text in all_groups or '; id ' in message.text:
        await message.answer('reply keyboard removed', reply_markup=types.ReplyKeyboardRemove())


async def already_registered(message: types.Message, state: FSMContext):
    " Проверяет, зарегистрирован ли пользователь"
    if registerData_get_role(user_id=message.chat.id) == 'student':
        await message.answer('Студент, топай регаться в свой бот, понятно да')
        return
  
    await message.answer('Вы уже зарегистрированы' + '\nВы: ' + str(registerData_get_fio(user_id=message.chat.id)) + '; ' + 'Ваша роль: ' + str(registerData_get_role(message.chat.id)), reply_markup=types.ReplyKeyboardRemove())

    buttons = [
        types.InlineKeyboardButton(
            text="Да", callback_data="register_change_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="register_change_false")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer('Хотите изменить рег. данные?', reply_markup=keyboard)


async def ask_fio(message: types.message, state: FSMContext):
    " (registerUser FSM) Предлагаем ввести ФИО"
    await state.update_data(chosen_role="prepod")
    await message.answer('Введите ФИО')
    await registerUser.waiting_for_fio.set()


async def choose_fio(message: types.Message, state: FSMContext):
    " (registerUser FSM) Получаем ФИО и отправляем данные"
    fio = message.text
    await state.update_data(chosen_fio=fio)
    user_data = await state.get_data()

    # ############### БРАТЬ ДАННЫЕ О РЕГИСТРАЦИИ ПРЕПОДА ТУТ ##########

    await message.reply('Ваше ФИО: ' + user_data['chosen_fio'] + '; Ваша роль: ' + user_data['chosen_role'])

    registerData_add_user(user_id=message.chat.id, chosen_fio=user_data['chosen_fio'], chosen_group='prepod', chosen_role=user_data['chosen_role'])

    await message.answer('Регистрация завершена', reply_markup=types.ReplyKeyboardRemove())

    # ######################### ############### ##########
    await state.finish()


async def register_change_true(call: types.CallbackQuery, state: FSMContext):
    " (already_registered Func) Выбираем какие рег. данные изменить"
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

# ДОБАВИТЬ ПРОВЕРКУ НА ПРЕПА/СТУДЕНТА

    buttons = [
        types.InlineKeyboardButton(
            text="ФИО", callback_data="register_change_fio"),
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
    
    await message.answer('Данные обновлены: ' + '\nВы: ' + str(registerData_get_fio(user_id=message.chat.id)) + '; ' + 'Ваша роль: ' + str(registerData_get_role(user_id=message.chat.id)), reply_markup=types.ReplyKeyboardRemove())


async def register_change_fio(call: types.CallbackQuery, state: FSMContext):
    " (register_change_true Func) Предлагаем ввести новую фамилию"
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await register_change_fio_fsm.waiting_for_new_fio.set()
    await call.message.answer('Введите новые ФИО')


async def cancel_handler(message: types.Message, state: FSMContext):
    """ Отменяет действия в FSM"""
    current_state = await state.get_state()
    print(current_state)
    if current_state is None:
        return
    await state.finish()
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_register_prepod(dp: Dispatcher):
    dp.register_message_handler(
        already_registered, lambda message: registerData_check_is_registered(message.chat.id), commands='register')
    dp.register_message_handler(ask_fio, commands="register", state="*")
    dp.register_message_handler(choose_fio, state=registerUser.waiting_for_fio)

    dp.register_message_handler(
        register_change_fio_set_fio, state=register_change_fio_fsm.waiting_for_new_fio)

    dp.register_message_handler(cancel_handler, commands="cancel", state="*")

    dp.register_callback_query_handler(
        register_change_true, text="register_change_true")
    dp.register_callback_query_handler(
        register_change_false, text="register_change_false")
    dp.register_callback_query_handler(
        register_change_fio, text="register_change_fio")

    dp.register_message_handler(strangeMessagesHandler)
