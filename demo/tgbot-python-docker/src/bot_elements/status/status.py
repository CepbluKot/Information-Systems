""" Статус пользователя"""
from aiogram import Bot, Dispatcher, types
from bot_elements.getter.all_getters import completing_forms_dispatcher_get_form_copy, mem_for_created_forms_get_creator_id, mem_for_created_forms_get_form_name, completing_forms_dispatcher_get_current_question_num, completing_forms_dispatcher_get_question_by_num, send_forms_mem_get, completing_forms_dispatcher_get_form_question_message_id, completing_forms_dispatcher_get, completing_froms_dispatcher_is_user_in_list, completing_forms_dispatcher_get_form_id, completing_forms_dispatcher_get_sent_form_id, completing_forms_dispatcher_get_form_question_copy, send_forms_mem_get_form_completed_users, send_forms_mem_get_form_sent_users, temp_mem_for_answers_get
from bot_elements.remover.all_removers import completing_forms_dispatcher_remove_session
from bot_elements.setter.all_setters import completing_forms_dispatcher_add_session, completing_forms_dispatcher_add_1_to_question_num, completing_forms_dispatcher_set_question_id, send_forms_mem_add_completed_user, sendMsgAnswer, sendPollAnswer, sendFormAnswer

import collections
# import configparser

# config = configparser.ConfigParser()
# config.read('/home/gilfoyle/Documents/coding/work-4-food/config.ini')
# config.read('/Users/igormalysh/Documents/codes/demo/tgbot-python-docker/src/config.ini')
bot = Bot(token='5134710670:AAGHtQcQWDxQcqG370rZMZygP_Rs_A5-Sg8')


async def display_user_status(message: types.Message):

    full_message = "Полученные формы:"
    print('\n\n\n',send_forms_mem_get())
    for selected_form in send_forms_mem_get():
        form = send_forms_mem_get()
        select_form = form[selected_form]
        if message.chat.id in select_form['info']['send_to_users_ids'] and not message.chat.id in select_form['info']['got_answers_from']:
            
            full_message += '\n' + str(mem_for_created_forms_get_form_name(select_form['form_id'])) + ' от пользователя ' + str(mem_for_created_forms_get_creator_id(select_form['form_id'])) + ' /complete_' + str(select_form['form_id']) + '_' + str(selected_form)

    await message.answer(full_message)


async def complete_form(message: types.Message):
    """ Получает название формы, добавляет данные в forms_dispatcher,
        запускает отправку вопросов из нужной формы"""

    form_indexes = message.text[10:].split('_')
    unique_form_id = int(form_indexes[0])
    unique_sent_form_id = int(form_indexes[1])

    completing_forms_dispatcher_add_session(chat_id=message.chat.id, unique_form_id=unique_form_id, unique_sent_form_id=unique_sent_form_id)

    print('completing_forms_dispatcher', completing_forms_dispatcher_get())
    await go_cycle(message=message, type='launch_from_message_handler')


# complete polls
async def go_cycle(message, type):
    """Отсылает вопросы/ опросы из completing_forms_dispatcher при вызове"""

    
    user_id = 0
    if type == 'launch_from_poll_handler':
        
        user_id = message.user.id

    elif type == 'launch_from_message_handler':
        
        user_id = message.chat.id

    print(user_id)
   
    curr_question_num = completing_forms_dispatcher_get_current_question_num(user_id=user_id)


    curr_quest = completing_forms_dispatcher_get_question_by_num(user_id=user_id, question_num=curr_question_num)
    
    print('\n IMPORTONT ', curr_question_num, curr_quest)
    if curr_quest['type'] == 'poll':

        msg = await bot.send_poll(chat_id=user_id, question=curr_quest['question'], options=curr_quest['options'], is_anonymous=False)
        completing_forms_dispatcher_set_question_id(user_id=user_id, question_num=curr_question_num, question_id=msg.poll.id)
        

    elif curr_quest['type'] == 'msg':
        msg = await bot.send_message(chat_id=user_id, text=curr_quest['question'])
        completing_forms_dispatcher_set_question_id(user_id=user_id, question_num=curr_question_num, question_id=msg.message_id)


    elif curr_quest['type'] == 'info':
        sent_form_id = completing_forms_dispatcher_get_sent_form_id(user_id=user_id)
        send_forms_mem_add_completed_user(sent_form_id=sent_form_id, user_id=user_id)
        completing_forms_dispatcher_remove_session(user_id=user_id)
        print('theend')
        
        sendFormAnswer(temp_mem_for_answers_get())
        print('\n', temp_mem_for_answers_get())
        print(completing_forms_dispatcher_get())


        if collections.Counter(send_forms_mem_get_form_completed_users(sent_form_id=sent_form_id)) == collections.Counter(send_forms_mem_get_form_sent_users(sent_form_id=sent_form_id)):
            print('FORM FULLY COMPLETED')


def lambda_checker_poll(pollAnswer: types.PollAnswer):
    """Проверяет принадлежит ли опрос выбранной форме"""
    if completing_froms_dispatcher_is_user_in_list(user_id=pollAnswer.user.id):
        selected_form = completing_forms_dispatcher_get_form_copy(user_id=pollAnswer.user.id)

        curr_question_num = completing_forms_dispatcher_get_current_question_num(user_id=pollAnswer.user.id)
        

        # print(selected_form)
        # print(selected_form[curr_question_num])

        print(selected_form[curr_question_num], pollAnswer['poll_id'])

        if completing_forms_dispatcher_get_form_question_message_id(user_id=pollAnswer.user.id, question_num=curr_question_num) == pollAnswer['poll_id']:
            question_number = completing_forms_dispatcher_get_current_question_num(user_id=pollAnswer.user.id)
            unique_form_id = completing_forms_dispatcher_get_form_id(user_id=pollAnswer.user.id)
            unique_sent_form_id = completing_forms_dispatcher_get_sent_form_id(user_id=pollAnswer.user.id)
            pollCopy = completing_forms_dispatcher_get_form_question_copy(user_id=pollAnswer.user.id, question_num=question_number)

            sendPollAnswer(pollAnswer=pollAnswer, question_number=question_number, unique_form_id=unique_form_id, unique_sent_form_id=unique_sent_form_id, pollCopy=pollCopy)

            return True
        # print('folss')
        return False


def lambda_checker_msg(message: types.Message):
    """Проверяет является ли сообщение ответом на вопрос из формы"""

    if completing_froms_dispatcher_is_user_in_list(user_id=message.chat.id):
        
        ''' send answer data + quest indexes + quest copy'''

        curr_question_num = completing_forms_dispatcher_get_current_question_num(user_id=message.chat.id)
        
        print(completing_forms_dispatcher_get_form_question_message_id(user_id=message.chat.id, question_num=curr_question_num) + 1, message.message_id)
        if completing_forms_dispatcher_get_form_question_message_id(user_id=message.chat.id, question_num=curr_question_num) + 1 == message.message_id:
            
            question_number = completing_forms_dispatcher_get_current_question_num(user_id=message.chat.id)
            unique_form_id = completing_forms_dispatcher_get_form_id(user_id=message.chat.id)
            unique_sent_form_id = completing_forms_dispatcher_get_sent_form_id(user_id=message.chat.id)
            messageCopy = completing_forms_dispatcher_get_form_question_copy(user_id=message.chat.id, question_num=question_number)

            sendMsgAnswer(messageAnswer=message, question_number=question_number, unique_form_id=unique_form_id, unique_sent_form_id=unique_sent_form_id, messageCopy=messageCopy)
            
            completing_forms_dispatcher_add_1_to_question_num(user_id=message.chat.id)
            # print(message.text)
            return True
        # print('folss')
        return False


# handler activates when vote/send answer
async def poll_handler(pollAnswer: types.PollAnswer):
    """Активируется, когда приходит ответ на опрос/ опрос закрывается"""
    print('completing_forms_dispatcher ', completing_forms_dispatcher_get())
    # print(pollAnswer)
    if completing_forms_dispatcher_get():
        completing_forms_dispatcher_add_1_to_question_num(user_id=pollAnswer.user.id)
        await go_cycle(message=pollAnswer, type='launch_from_poll_handler')
    # print(poll['id'])


async def msg_handlr(message: types.Message):
    """Активируется, когда приходит сообщение"""
    print('completing_forms_dispatcher', completing_forms_dispatcher_get())
    
    if completing_forms_dispatcher_get():
        # print('go ahead msg')
        await go_cycle(message=message, type='launch_from_message_handler')


def register_handlers_status(dp: Dispatcher):
    dp.register_message_handler(
        display_user_status, commands="status", state="*")
    dp.register_message_handler(
        complete_form, lambda message: message.text.startswith('/complete'))
    dp.register_poll_answer_handler(
        poll_handler, lambda message: lambda_checker_poll(message))
    dp.register_message_handler(
        msg_handlr, lambda message: lambda_checker_msg(message))
