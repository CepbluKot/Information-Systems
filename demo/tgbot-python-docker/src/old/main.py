import asyncio
from asyncio import get_event_loop

from aiogram import Dispatcher, types, Bot, executor
import aiogram
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
import sys

import time

import full_pars_2
import prep_text_pars
# sys.path.append('/home/gilfoyle/Documents/coding/telegram_bot/db_setting')

# import tg_connect_db as tg_db
# from db_connect import DataConnect
# from us_init import find_teleg_group

# import sys
# sys.path.append('/home/gilfoyle/Documents/coding/telegram_bot/db_setting')
# import tg_connect_db as tg_db
# from db_connect import DataConnect

API_TOKEN = '5110094448:AAGG_IiPPyjvwtROrBqGu0C74EMSjew3NDQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=get_event_loop())
polls_dispcatcher = []

temp_mem_for_multiple_poll = []

multiple_polls_dispatcher = []

# example
all_groups = []
for data in prep_text_pars.get_prepod_page('https://mai.ru/education/studies/schedule/ppc.php?guid=d0c04806-1d99-11e0-9baf-1c6f65450efa#'):
    all_groups.append(data['group'])

rasp = full_pars_2.parse_group_today('М3О-221Б-20')

# ############### poll + (optional) dispatcher #################


@dp.message_handler(commands=["poll"])
async def cmd_poll(message: types.message):
    await message.answer('Высылаю опрос')
    options = ['MaXImus', 'DmitRUS', 'FedoSUS', 'Ilyxus', 'ArtemOS']
    # chat_id = message.chat.id
    chat_id = message.chat.id
    is_anonymous = True
    # open_period = 10
    question = 'you are'

    poll = await bot.send_poll(options=options, is_anonymous=False, question=question, chat_id=chat_id)
    close_time = time.time() + 5
    # send chat id and poll id
    polls_dispcatcher.append(
        {"chat_id": poll.chat.id, "message_id": poll.message_id, 'close_time': close_time})
    print('poll created')

# ############## end poll #################


# ################regiser zone #############################

class registerUser(StatesGroup):
    waiting_for_role = State()
    waiting_for_fio = State()
    waiting_for_group = State()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print(current_state)
    if current_state is None:
        return
    await state.finish()
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


# ######### is registered check ##################

# @dp.message_handler(lambda message: True, commands='register')
# async def wrong_group(message: types.Message, state: FSMContext):
#     await message.answer('вы уже зареганы')
#     buttons = [
#         types.InlineKeyboardButton(
#             text="Да", callback_data="register_change_true"),
#         types.InlineKeyboardButton(
#             text="Нет", callback_data="register_change_false")
#     ]
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     await message.answer('Хотите изменить рег данные?', reply_markup=keyboard)


@dp.message_handler(commands='register')
async def choose_role(message: types.Message):

    buttons = [
        types.InlineKeyboardButton(text="Студент", callback_data="is_student"),
        types.InlineKeyboardButton(
            text="Преподаватель", callback_data="is_prepod"),
        types.InlineKeyboardButton(
            text="Админ", callback_data="is_admin")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer("Выберите роль      ", reply_markup=keyboard)


@dp.message_handler(state=registerUser.waiting_for_fio)
async def fio_choosen(message: types.Message, state: FSMContext):
    fio = message.text
    await state.update_data(chosen_fio=fio)
    user_data = await state.get_data()
    if user_data['chosen_role'] == 'student':
        marakap = ReplyKeyboardMarkup(one_time_keyboard=True)

        for data in all_groups:
            marakap.add(KeyboardButton(data))

        await registerUser.next()
        await message.reply('Выберите группу', reply_markup=marakap)

    else:

        # ############### БРАТЬ ДАННЫЕ О РЕГИСТРАЦИИ ПРЕПОДА ТУТ ##########

        # await message.reply('вы ' + user_data['chosen_fio'] + ' ' + user_data['chosen_role'])
        await message.answer('Регистрация завершена', reply_markup=types.ReplyKeyboardRemove())

        # ######################### ############### ##########
        await state.finish()


@dp.message_handler(lambda message: message.text not in all_groups, state=registerUser.waiting_for_group)
async def wrong_group(message: types.Message, state: FSMContext):
    return await message.reply('Выберите группу из списка')


@dp.message_handler(state=registerUser.waiting_for_group)
async def choose_group(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['chosen_role'] != "prepod":

        group = message.text

        await state.update_data(chosen_group=group)
        user_data = await state.get_data()
# ############### БРАТЬ ДАННЫЕ О РЕГИСТРАЦИИ СТУДЕНТА ТУТ ##########

        # await message.answer(f"{user_data['chosen_role']} {user_data['chosen_group']} {user_data['chosen_fio']}.\n", reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Регистрация завершена', reply_markup=types.ReplyKeyboardRemove())
# #########################################################

    await state.finish()


@dp.callback_query_handler(text="register_change_true")
async def is_stud(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

# ДОБАВИТЬ ПРОВЕРКУ НА ПРЕПА/СТУДЕНТА

    buttons = [
        types.InlineKeyboardButton(
            text="ФИО", callback_data="register_change_fio"),
        types.InlineKeyboardButton(
            text="Группу", callback_data="register_change_group")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.answer('Что именно изменить?', reply_markup=keyboard)


@dp.callback_query_handler(text="register_change_false")
async def is_prep(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await call.message.answer('Окес')


@dp.callback_query_handler(text="register_change_fio")
async def is_prep(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

# сделать изменения в бд и проверку, есть ли уже такое

    await call.message.answer('фио изменено')


@dp.callback_query_handler(text="register_change_group")
async def is_prep(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

# сделать изменения в бд и проверку, есть ли уже такое

    await call.message.answer('группа изменена')


@dp.callback_query_handler(text="is_student")
async def is_stud(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await registerUser.waiting_for_role.set()
    await state.update_data(chosen_role="student")
    await call.answer()
    await registerUser.next()
    await call.message.answer('Введите ФИО')


@dp.callback_query_handler(text="is_prepod")
async def is_prep(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await registerUser.waiting_for_role.set()
    await state.update_data(chosen_role="prepod")
    await call.answer()
    # user_data = await state.get_data()
    # await call.message.answer('Вы '+ user_data['chosen_role'])
    await registerUser.next()
    await call.message.answer('Введите ФИО')


@dp.callback_query_handler(text="is_admin")
async def is_stud(call: types.CallbackQuery):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    print(call.from_user)
    await call.message.answer('user '+ str(call.from_user.id) + ' tryin 2 becum admin')

# ################ end register ########


# ############## poll creator ###########


async def make_poll(chat_id, end_time, options=['NO OPTIONS'], is_anonymous=True, question='NO QUESTION'):

    for recipient in chat_id:
        poll = await bot.send_poll(options=options, is_anonymous=is_anonymous, question=question, chat_id=recipient)
        splited_close_time = end_time.split(':')

        close_time = time.time() + int(splited_close_time[0]) * 60 * 60 + int(
            splited_close_time[1]) * 60 + int(splited_close_time[2])

    # send chat id and poll id
        polls_dispcatcher.append(
            {"chat_id": poll.chat.id, "message_id": poll.message_id, 'close_time': close_time})


class createPoll(StatesGroup):
    waiting_for_question = State()
    waiting_for_options = State()
    waiting_for_recipient = State()
    waiting_for_time = State()


@dp.message_handler(commands='create_poll')
async def choose_question(message: types.Message):
    await createPoll.next()
    await message.reply("Введите вопрос")


@dp.message_handler(state=createPoll.waiting_for_question)
async def get_question(message: types.Message, state: FSMContext):

    question = message.text

    await state.update_data(question=question)
    await message.reply('Пришлите варианты ответов через запятую')
    await createPoll.next()


@dp.message_handler(state=createPoll.waiting_for_options)
async def get_options(message: types.Message, state: FSMContext):

    options = message.text.split(',')
    await state.update_data(options=options)

    marakap = ReplyKeyboardMarkup(one_time_keyboard=True)

    for data in all_groups:
        marakap.add(KeyboardButton(data))

    await message.reply('Выберите какой группе отправить', reply_markup=marakap)

    await createPoll.next()


@dp.message_handler(lambda message: message.text not in all_groups, state=createPoll.waiting_for_recipient)
async def wrong_group(message: types.Message, state: FSMContext):
    return await message.reply('Выберите группу из списка')


@dp.message_handler(state=createPoll.waiting_for_recipient)
async def get_recipient(message: types.Message, state: FSMContext):
    group = message.text
    await state.update_data(group=group)
    await message.reply('Сколько времени будет открыто голосование (Пишите в формате часы:минуты:секунды)', reply_markup=types.ReplyKeyboardRemove())
    await createPoll.next()


@dp.message_handler(state=createPoll.waiting_for_time)
async def get_time(message: types.Message, state: FSMContext):
    select_time = message.text
    await state.update_data(time=select_time)
    user_data = await state.get_data()

    

# ############### ЗДЕСЬ ДОБАВИТЬ FOR ЧТОБЫ ЗАПОЛНИТЬ СПИСОК USER_ID_LIST АЙДИШНИКАМИ ЮЗЕРОВ СООТВЕТСТВУЮЩЕЙ ГРУППЫ ##########
    # выбранная группа = user_data['group']

# ############### # ############### # ############### # ###############

    user_data = await state.get_data()
    await message.answer('ГОТОВО')
    await state.finish()
    users_id_list = [506629389]
    await make_poll(chat_id=users_id_list, question=user_data['question'], options=user_data['options'], end_time=user_data['time'])
    # await make_poll(chat_id=find_teleg_group(group), question=user_data['question'], options=user_data['options'])


# ################# creatr end #########



# states test


class statesTest(StatesGroup):
    state_middle = State()
    state_end = State()
    eshe = State()
    
@dp.message_handler( commands=['test'])
async def choose_group(message: types.Message, state: FSMContext):
    await message.answer('first steg')
    await statesTest.next()


@dp.message_handler(state=statesTest.state_middle)
async def choose_group(message: types.Message, state: FSMContext):
    await message.answer('midle steg')
    await statesTest.next()


@dp.message_handler(state=statesTest.state_end)
async def choose_group(message: types.Message, state: FSMContext):
    # await statesTest
    await message.answer('end steg')
    await statesTest.next()


@dp.message_handler(state=statesTest.eshe)
async def choose_group(message: types.Message, state: FSMContext):
    # await statesTest
    await message.answer('fin steg')
    
    await statesTest.state_middle.set()
    # await state.finish()
    await message.answer('finishd')




# new opros type ##########


# async def make_poll(chat_id, options=['NO OPTIONS'], is_anonymous=True, question='NO QUESTION'):

#     for recipient in chat_id:
#         poll = await bot.send_poll(options=options, is_anonymous=is_anonymous, question=question, chat_id=recipient)
        # splited_close_time = end_time.split(':')

        # close_time = time.time() + int(splited_close_time[0]) * 60 * 60 + int(
        #     splited_close_time[1]) * 60 + int(splited_close_time[2])

    # send chat id and poll id
        


class poll_t(StatesGroup):
    
    waiting_for_question = State()
    waiting_for_options = State()

class group_chooser(StatesGroup):
    waiting_for_group = State()

@dp.message_handler(commands='multi_poll')
async def choose_question(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Опрос", callback_data="question_type_poll"),
        types.InlineKeyboardButton(
            text="Ввод с клавы", callback_data="question_type_msg")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    
    await message.reply("Выберите тип вопроса", reply_markup=keyboard)



@dp.message_handler(state=poll_t.waiting_for_question)
async def get_question(message: types.Message, state: FSMContext):
    
    question = message.text
    await state.update_data(question=question)
    data = await state.get_data()
    if data['type'] == 'msg':
        temp_mem_for_multiple_poll.append({'question': data['question'], 'id': 0, 'type': 'msg'})
        buttons = [
        types.InlineKeyboardButton(text="Да", callback_data="add_quest_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="add_quest_false"),
        types.InlineKeyboardButton(
            text="Удалить последний вопрос", callback_data="del_quest_true")
        ]
        
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
    
        await message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)
        # print(temp_mem_for_multiple_poll)
        await state.finish()

    else:
        await state.update_data(question=question)
        await poll_t.next()
        await message.reply('Пришлите варианты ответов через запятую')


@dp.message_handler(state=poll_t.waiting_for_options)
async def get_options(message: types.Message, state: FSMContext):

    options = message.text.split(',')
    await state.update_data(options=options)

    user_data = await state.get_data()
    # print(user_data['question'], user_data['options'])
    
    temp_mem_for_multiple_poll.append({'question': user_data['question'], 'options': user_data['options'], 'id': 0, 'type': 'poll'})
    
    buttons = [
        types.InlineKeyboardButton(text="Да", callback_data="add_quest_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="add_quest_false"),
        types.InlineKeyboardButton(
            text="Удалить последний вопрос", callback_data="del_quest_true")
        ]
        
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    

    await message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)
    # print(temp_mem_for_multiple_poll)
    await state.finish()


@dp.message_handler(state=group_chooser.waiting_for_group)
async def choose_group(message: types.Message, state: FSMContext):
    
    group = message.text
    await message.answer('groop' + ' ' + group)
    # bd search
    users_id_list = [506629389]
    temp_mem_for_multiple_poll.append({'users_id': users_id_list, 'type': 'recipient_info'})
    multiple_polls_dispatcher.append([*temp_mem_for_multiple_poll])

    # print(multiple_polls_dispatcher)
    temp_mem_for_multiple_poll.clear()
    await state.finish()



@dp.callback_query_handler(text="add_quest_true")
async def add_poll_true(call: types.CallbackQuery):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    buttons = [
        types.InlineKeyboardButton(text="Опрос", callback_data="question_type_poll"),
        types.InlineKeyboardButton(
            text="Ввод с клавы", callback_data="question_type_msg")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    
    await call.message.reply('Выберите тип вопроса', reply_markup=keyboard)
    
    


@dp.callback_query_handler(text="add_quest_false")
async def add_poll_false(call: types.CallbackQuery):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await call.message.answer('gotovo')
    
    
    await group_chooser.waiting_for_group.set()
    await call.message.answer('choose group')



@dp.callback_query_handler(text="del_quest_true")
async def add_poll_false(call: types.CallbackQuery):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    temp_mem_for_multiple_poll.pop()
    await call.message.answer('last quest deleted')
    # print(temp_mem_for_multiple_poll)
    buttons = [
        types.InlineKeyboardButton(text="Да", callback_data="add_quest_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="add_quest_false"),
        types.InlineKeyboardButton(
            text="Удалить последний вопрос", callback_data="del_quest_true")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await call.message.reply('Добавить ещё 1 вопрос?', reply_markup=keyboard)
    
    

@dp.callback_query_handler(text="question_type_poll")
async def question_type_poll(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await poll_t.waiting_for_question.set()
    await state.update_data(type='poll')
    await call.message.answer('Введите вопрос')
    


@dp.callback_query_handler(text="question_type_msg")
async def question_type_msg(call: types.CallbackQuery, state: FSMContext):
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await poll_t.waiting_for_question.set()
    await state.update_data(type='msg')
    await call.message.answer('Введите вопрос')


@dp.message_handler(commands='send')
async def start_cycle(message: types.Message):
    await go_cycle()

async def go_cycle():
    print(multiple_polls_dispatcher)
    if multiple_polls_dispatcher:
        
        if multiple_polls_dispatcher[0]:
            
            if multiple_polls_dispatcher[0][0]:
                
                curr_quest = multiple_polls_dispatcher[0][0]
                for reciever in multiple_polls_dispatcher[0][-1]['users_id']:

                    # print(multiple_polls_dispatcher[0][-1]['users_id'])
                    if curr_quest['type'] == 'poll':
                    
                        msg = await bot.send_poll(chat_id=506629389, question=curr_quest['question'], options=curr_quest['options'], is_anonymous=True)
                        curr_quest['id'] = msg.poll.id

                    elif curr_quest['type'] == 'msg':
                        msg = await bot.send_message(chat_id=reciever, text=curr_quest['question'])
                        curr_quest['id'] = msg.message_id
                        # print(curr_quest['id'])
                    else:
                        multiple_polls_dispatcher[0].remove({'users_id': curr_quest['users_id'], 'type': 'recipient_info'})
                

def lambda_checker_poll(message):
    for data in multiple_polls_dispatcher:
        for a in data:
            # print(a)
            if a['id'] == message['id']:
                multiple_polls_dispatcher[0].remove({'question': a['question'], 'options': a['options'], 'id': a['id'], 'type': 'poll'})
                # print('eh')
                return True
    # print('folss')
    return False

def lambda_checker_msg(message: types.Message):
    for data in multiple_polls_dispatcher:
        for a in data:
            if a['id'] + 1 == message.message_id:
                multiple_polls_dispatcher[0].remove({'question': a['question'], 'id': a['id'], 'type': 'msg'})
                # print('eh')
                # print(message.text)
                return True
    # print('folss')
    return False

@dp.poll_handler(lambda message: lambda_checker_poll(message))
async def poll_hanlr(poll: types.PollAnswer):
    print(poll)
    if multiple_polls_dispatcher:
        await go_cycle()
    # print(poll['id'])

@dp.message_handler(lambda message: lambda_checker_msg(message))
async def msg_handlr(message: types.Message):
    print(message)
    if multiple_polls_dispatcher:
        await go_cycle()

# ################# creatr end #########

# new vopros end #######

async def set_commands():

    commands = [
        BotCommand(command="/multi_poll", description="Создать мульти опрос"),
        BotCommand(command="/create_poll", description="Создать опрос"),
        BotCommand(command="/poll", description="Опрос"),
        BotCommand(command="/register", description="Регистрация"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]

    await bot.set_my_commands(commands)


@dp.poll_answer_handler()
async def lol(poll):
    print(poll)

async def polls_dispatcher():
    while True:
        await asyncio.sleep(1)

        for select_poll in polls_dispcatcher:
            if select_poll['close_time'] < time.time():
                closed_poll = await bot.stop_poll(chat_id=select_poll['chat_id'], message_id=select_poll['message_id'])
                # print(closed_poll)
                # print(polls_dispcatcher)
                polls_dispcatcher.remove(
                    {"chat_id": select_poll['chat_id'], "message_id": select_poll['message_id'], "close_time": select_poll['close_time']})
                # print(polls_dispcatcher)


async def rasp_notification():
    while True:

        #  rasp = full_pars_2.parse_group_today('М3О-221Б-20') - ЗАПИХНИ ЭТО В САМОЕ НАЯАЛО ПЕРЕД ВСЕМИ ФУНКЦИЯМИ

        await asyncio.sleep(1)
        for data in rasp:
            time_diff = -(int(time.localtime().tm_hour) * 60 + int(time.localtime().tm_min)) + \
                int(data['time_start_hour']) * 60 + \
                int(data['time_start_minutes'])
            if time_diff <= 15 and time_diff > 0:
                pass
                # for user in data['notify']:
                #     if int(user['notify_status']) != 1:
                #         await bot.send_message(user['user'], str(data['name']) + ' через {0} минут'.format(time_diff))
                #         user['notify_status'] = 1
            # print(time_diff, data['name'])

if __name__ == '__main__':

    dp.loop.create_task(set_commands())
    dp.loop.create_task(polls_dispatcher())
    dp.loop.create_task(rasp_notification())
    executor.start_polling(dp)
