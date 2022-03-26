""" Система опросов"""

""" Создается форма, добавляется в хранилище форм"""

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_elements.remover.all_removers import temp_form_recipient_data_remove_element, temp_mem_for_form_creator_remove_form, temp_mem_for_form_creator_remove_form_element



from bot_elements.getter.all_getters import temp_mem_for_form_creator_get_data, temp_form_recipient_data_get_form_id, temp_form_recipient_data_get_recip_data, temp_form_recipient_data_get, temp_mem_for_form_creator_get, mem_for_created_forms_get, unique_form_id_get
from bot_elements.setter import all_setters
from bot_elements.setter.all_setters import unique_form_id_plus_one
from bot_elements.forms.form_display import display_current_temp_mem_status




class name(StatesGroup):
    """ FSM для выбора названия опроса"""
    waiting_for_name = State()


class form(StatesGroup):
    """ FSM для добавления одного вопроса/ опроса в форму"""

    waiting_for_question = State()
    waiting_for_options = State()


async def choose_name(message: types.Message, state: FSMContext):
    """ (name FSM) Предлагает выбрать название формы"""

    await message.reply("Выберите название формы")
    await name.waiting_for_name.set()


async def choose_type(message: types.Message, state: FSMContext):  # name.waiting_for_name
    """ (name FSM) Запоминает название и предлагает выбрать тип первого добавляемого вопроса"""

    all_setters.temp_form_recipient_data_add_user_data(chat_id=message.chat.id, 
    form_name=str(message.text), type="info", form_id=unique_form_id_get(), creator_id=message.chat.id)

    unique_form_id_plus_one()

    buttons = [
        types.InlineKeyboardButton(
            text="Опрос", callback_data="question_type_poll"),
        types.InlineKeyboardButton(
            text="Ввод с клавы", callback_data="question_type_msg")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await message.reply("Выберите тип вопроса", reply_markup=keyboard)
    await state.finish()


async def get_question(message: types.Message, state: FSMContext): # form.waiting_for_question
    """ (form FSM) Получает текст вопроса и тип, затем ЗАПОМИНАЕТ (и предлагает ввести варианты ответов)
        и предлагает добавить вопрос"""

    question = message.text
    await state.update_data(question=question)
    data = await state.get_data()
    if data['type'] == 'msg':

        all_setters.temp_mem_for_form_creator_add_element(user_id=message.chat.id, data={'question': data['question'], 'message_id': 0, 'type': 'msg'})

        print('temp_mem_for_form_creator', temp_mem_for_form_creator_get())
        buttons = [
            types.InlineKeyboardButton(
                text="Да", callback_data="add_quest_true"),
            types.InlineKeyboardButton(
                text="Нет", callback_data="add_quest_false")
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await display_current_temp_mem_status(message)

        await message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)
        await state.finish()

    else:
        await state.update_data(question=question)
        await message.reply('Пришлите варианты ответов через запятую')
        await form.waiting_for_options.set()


async def get_options(message: types.Message, state: FSMContext): # form.waiting_for_options
    """ (form FSM) Получает варианты ответов, ЗАПОМИНАЕТ и предлагает добавить вопрос"""

    options = message.text.split(',')
    await state.update_data(options=options)

    user_data = await state.get_data()
    # print(user_data['question'], user_data['options'])

    all_setters.temp_mem_for_form_creator_add_element(user_id=message.chat.id, data={'question': user_data['question'], 'options': user_data['options'], 'message_id': 0, 'type': 'poll'})
    
    print('temp_mem_for_form_creator', temp_mem_for_form_creator_get())

    buttons = [
        types.InlineKeyboardButton(text="Да", callback_data="add_quest_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="add_quest_false")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await display_current_temp_mem_status(message)

    await message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)
    # print(temp_mem_for_multiple_poll)
    await state.finish()


# callback queries handlers

async def add_quest_true(call: types.CallbackQuery):
    """ Выбор параметров для нового вопроса"""

    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    buttons = [
        types.InlineKeyboardButton(
            text="Опрос", callback_data="question_type_poll"),
        types.InlineKeyboardButton(
            text="Ввод с клавы", callback_data="question_type_msg")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await call.message.reply('Выберите тип вопроса', reply_markup=keyboard)


async def add_quest_false(call: types.CallbackQuery):
    """ Заканчивает создание формы"""

    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await display_current_temp_mem_status(message=call.message)


    all_setters.temp_mem_for_form_creator_add_element(user_id=call.message.chat.id, data=temp_form_recipient_data_get_recip_data(user_id=call.message.chat.id).copy())

    all_setters.mem_for_created_forms_add_element(form_id=temp_form_recipient_data_get_form_id(user_id=call.message.chat.id), data=temp_mem_for_form_creator_get_data(call.message.chat.id).copy())

    print('mem_for_created_forms ', mem_for_created_forms_get())

    temp_mem_for_form_creator_remove_form(user_id=call.message.chat.id)
    temp_form_recipient_data_remove_element(user_id=call.message.chat.id)

    print('temp_form_recipient_data ', temp_form_recipient_data_get())

    await call.message.answer('Форма создана', reply_markup=types.ReplyKeyboardRemove())


async def question_type_poll(call: types.CallbackQuery, state: FSMContext):
    """ Начало создания опроса"""

    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await state.update_data(type='poll')
    await call.message.answer('Введите вопрос', reply_markup=types.ReplyKeyboardRemove())
    await form.waiting_for_question.set()


async def question_type_msg(call: types.CallbackQuery, state: FSMContext):
    """ Начало создания обычного вопроса"""
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await state.update_data(type='msg')
    await call.message.answer('Введите вопрос', reply_markup=types.ReplyKeyboardRemove())
    await form.waiting_for_question.set()


async def del_handler(message: types.Message):
    """Удаляет одну запись из списка temp_mem по её идентификатору (из сообщения)"""
    
    delete_id = int(message.text[4:])
    temp_mem_for_form_creator_remove_form_element(user_id=message.chat.id, delete_id=delete_id)

    await message.answer('удалил пункт ' + str(delete_id), reply_markup=types.ReplyKeyboardRemove())
    await display_current_temp_mem_status(message)


def register_handlers_forms(dp: Dispatcher):
    dp.register_message_handler(choose_name, commands="multi_form", state="*")

    dp.register_message_handler(choose_type, state=name.waiting_for_name)
    dp.register_message_handler(get_question, state=form.waiting_for_question)
    dp.register_message_handler(get_options, state=form.waiting_for_options)

    dp.register_callback_query_handler(
        add_quest_true, text="add_quest_true")
    dp.register_callback_query_handler(
        add_quest_false, text="add_quest_false")
    dp.register_callback_query_handler(
        question_type_poll, text="question_type_poll")
    dp.register_callback_query_handler(
        question_type_msg, text="question_type_msg")

    dp.register_message_handler(
        del_handler, lambda message: message.text.startswith('/del'))
