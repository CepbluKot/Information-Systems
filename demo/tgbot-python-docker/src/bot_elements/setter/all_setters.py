from aiogram import types
from bot_elements.storages.all_storages import temp_form_recipient_data 
from bot_elements.storages.all_storages import temp_mem_for_form_creator
from bot_elements.storages.all_storages import mem_for_created_forms
from bot_elements.storages.all_storages import send_forms_mem 
from bot_elements.storages.all_storages import completing_forms_dispatcher 
from bot_elements.storages.all_storages import registerData 
from bot_elements.storages.all_storages import temp_mem_for_answers
import bot_elements.storages.all_storages


def temp_form_recipient_data_add_user_data(chat_id: int, form_name: str, type: str, form_id: int, creator_id: int):
    """Добавляет даныне пользователя во временный словарь со служебными данными формы"""
    if not chat_id in temp_form_recipient_data:
        temp_form_recipient_data[chat_id] = {}

    temp_form_recipient_data[chat_id]["form_name"] = form_name
    temp_form_recipient_data[chat_id]["type"] = type
    temp_form_recipient_data[chat_id]["form_id"] = form_id
    temp_form_recipient_data[chat_id]["creator_id"] = creator_id


def temp_mem_for_form_creator_add_element(user_id: int, data: dict):
    """ Добавляет 1 элемент формы во временный словарь для создания формы"""
    if user_id in temp_mem_for_form_creator:
            temp_mem_for_form_creator[user_id].append(data)
    else:
        temp_mem_for_form_creator[user_id] = [data]


def mem_for_created_forms_add_element(form_id: int, data):
    """ Добавляет 1 форму в словарь сохраненных форм"""
    mem_for_created_forms[form_id] = data


def mem_for_created_forms_insert_question(form_id: int, inser_after_id: int, data):
    """ Вставляет вопрос после выбранного id"""
    mem_for_created_forms[form_id].insert(inser_after_id + 1, data[0])


def mem_for_created_forms_set_new_form_name(form_id: int, new_form_name: str):
    """ Изменяет название формы из mem_for_created_forms"""
    mem_for_created_forms[form_id][-1]['form_name'] = new_form_name


def mem_for_created_forms_set_new_question_name(form_id: int, question_id: int, new_question_name: str):
    """ Изменяет название вопроса формы из mem_for_created_forms"""
    mem_for_created_forms[form_id][question_id]['question'] = new_question_name


def mem_for_created_forms_edit_poll_options(form_id: int, question_id: int, new_poll_options: list):
    """ Изменяет опции опроса формы из mem_for_created_forms"""
    mem_for_created_forms[form_id][question_id]['options'] = new_poll_options


def send_forms_mem_add_sent_form(sent_form_id: int, form_id: int, form_creator_user_id: int, send_to_users_ids: list):
    """ Добавляет 1 форму в список с отправленными формами"""
    send_forms_mem[sent_form_id] = {'form_id': form_id, 'info': {'form_creator_user_id': form_creator_user_id, 'send_to_users_ids': send_to_users_ids, 'got_answers_from': []}}


def send_forms_mem_add_completed_user(sent_form_id: int, user_id: int):
    """ Добавляет пользователя в список пользователей прошедших форму"""
    send_forms_mem[sent_form_id]['info']['got_answers_from'].append(user_id)


def completing_forms_dispatcher_add_session(chat_id: int, unique_form_id: int, unique_sent_form_id: int):
    """ Добавляет 1 сессию в список активных сессий"""
    completing_forms_dispatcher[chat_id] = {
        'chat_id': chat_id, 'unique_form_id': unique_form_id, 'unique_sent_form_id': unique_sent_form_id, 'current_question_num': 0,'form_copy': mem_for_created_forms[unique_form_id]}
    

def completing_forms_dispatcher_add_1_to_question_num(user_id: int):
    """ Увеличивает на 1 номер текущего задаваемого вопроса"""
    completing_forms_dispatcher[user_id]['current_question_num'] += 1


def completing_forms_dispatcher_set_question_id(user_id: int, question_num: int, question_id: int):
    """ Задает id для сообщения формы"""
    completing_forms_dispatcher[user_id]['form_copy'][question_num]['message_id'] = question_id
    print(completing_forms_dispatcher[user_id]['form_copy'][question_num])    


def registerData_add_user(user_id: int, chosen_fio: str, chosen_group: str, chosen_role: str):
    """ Добавляет рег. данные пользователя"""
    registerData[user_id] = {'chosen_fio': chosen_fio, 'chosen_group': chosen_group, 'chosen_role': chosen_role}


def registerData_change_group_data(user_id: int, new_group: str):
    """ Изменяет группу пользователя"""
    registerData[user_id]['chosen_group'] = new_group
    

def registerData_change_fio_data(user_id: int, new_fio: str):
    """ Изменяет ФИО пользователя"""
    registerData[user_id]['chosen_fio'] = new_fio


def unique_form_id_plus_one():
    """ Увеличивает счетчик созданных вопросов на 1"""
    bot_elements.storages.all_storages.unique_form_id += 1
    
    print('\n\ni daaaan ', bot_elements.storages.all_storages.unique_form_id)


def unique_sent_form_id_plus_one():
    """ Увеличивает счетчик отправленных вопросов на 1"""
    bot_elements.storages.all_storages.unique_sent_form_id += 1
    print(bot_elements.storages.all_storages.unique_sent_form_id)


def sendPollAnswer(pollAnswer: types.PollAnswer, question_number: int, unique_form_id: int, unique_sent_form_id: int, pollCopy):
    """ Получает ответ на опрос"""
    # print('\n',pollAnswer, question_number, unique_form_id, unique_sent_form_id, pollCopy)

    if not pollAnswer.user.id in temp_mem_for_answers.keys():
        temp_mem_for_answers[pollAnswer.user.id] = []
    
    temp_mem_for_answers[pollAnswer.user.id].append({'pollAnswer': pollAnswer, 'question_number': question_number, 'unique_form_id': unique_form_id, 'unique_sent_form_id': unique_sent_form_id, 'pollCopy': pollCopy})
    

def sendMsgAnswer(messageAnswer: types.Message, question_number: int, unique_form_id: int, unique_sent_form_id: int, messageCopy):
    """ Получает ответ на текстовый вопрос"""
    # print('\n', messageAnswer, question_number, unique_form_id, unique_sent_form_id, messageCopy)
    if not messageAnswer.chat.id in temp_mem_for_answers.keys():
        temp_mem_for_answers[messageAnswer.chat.id] = []
    
    temp_mem_for_answers[messageAnswer.chat.id].append({'messageAnswer': messageAnswer, 'question_number': question_number, 'unique_form_id': unique_form_id, 'unique_sent_form_id': unique_sent_form_id, 'messageCopy': messageCopy})


def sendFormAnswer(formAnswer: dict):
    """ Сюда приходит форма со всеми ответами на форму"""
    print(formAnswer)
    pass