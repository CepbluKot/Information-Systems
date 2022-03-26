from bot_elements.storages.all_storages import temp_form_recipient_data 
from bot_elements.storages.all_storages  import temp_mem_for_form_creator
from bot_elements.storages.all_storages  import mem_for_created_forms
from bot_elements.storages.all_storages  import send_forms_mem
from bot_elements.storages.all_storages import completing_forms_dispatcher 
from bot_elements.storages.all_storages import registerData
from bot_elements.storages.all_storages import temp_mem_for_answers
import bot_elements.storages.all_storages

def temp_form_recipient_data_get_data(user_id: int):
    """ Возвращает временную ячейку памяти хранящую служебные данные (temp_form_recipient_data)"""
    return temp_form_recipient_data[user_id]


def temp_mem_for_form_creator_get_data(user_id: int):
    """ Возвращает временную ячейку памяти хранящую данные создаваемой формы (temp_mem_for_form_creator)"""
    return temp_mem_for_form_creator[user_id]


def temp_mem_for_form_creator_get():
    """ Возвращает словарь с инфой о формах которые юзеры создают в наст. момент (temp_mem_for_form_creator)"""
    return temp_mem_for_form_creator


def temp_form_recipient_data_get_form_id(user_id: int):
    """  Возвращает айди формы из временного словаря со служебной инфой"""
    return temp_form_recipient_data[user_id]['form_id']


def temp_form_recipient_data_get_recip_data(user_id: int):
    """  Возвращает временный словарь со служебной инфой"""
    return temp_form_recipient_data[user_id]


def temp_form_recipient_data_get():
    """  Возвращает temp_form_recipient_data (словарь создаваемых в наст. момент форм)"""
    return temp_form_recipient_data


def mem_for_created_forms_get():
    """ Возвращает mem_for_created_forms"""
    return mem_for_created_forms


def mem_for_created_forms_get_data(form_id: int):
    """ Возвращает ячейку памяти хранящую данные созданной формы (mem_for_created_forms)"""
    return mem_for_created_forms[form_id]


def mem_for_created_forms_get_form_name(form_id: int):
    """ Возвращает название созданной формы из mem_for_created_forms"""
    return mem_for_created_forms[form_id][-1]['form_name']


def mem_for_created_forms_get_creator_id(form_id: int):
    """ Возвращает айди создателя формы из mem_for_created_forms"""
    return mem_for_created_forms[form_id][-1]['creator_id']


def completing_forms_dispatcher_get_form_copy(user_id: int):
    """ Возвращает копию формы из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['form_copy']


def completing_forms_dispatcher_get_form_question_copy(user_id: int, question_num: int):
    """ Возвращает копию вопроса из формы"""
    return completing_forms_dispatcher[user_id]['form_copy'][question_num]


def completing_forms_dispatcher_get_form_question_message_id(user_id: int, question_num: int):
    """ Возвращает айди сообщения(опроса) по номеру вопроса из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['form_copy'][question_num]['message_id']


def completing_forms_dispatcher_get_current_question_num(user_id: int):
    """ Возвращает номер текущего вопроса из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['current_question_num']


def completing_forms_dispatcher_get_question_by_num(user_id: int, question_num: int):
    """ Возвращает вопрос по номеру вопроса из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['form_copy'][question_num]


def completing_forms_dispatcher_get_form_id(user_id: int):
    """ Возвращает айди сохраненной формы по юзер айди из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['unique_form_id']


def completing_forms_dispatcher_get_sent_form_id(user_id: int):
    """ Возвращает айди отправленной формы по юзер айди из completing_forms_dispatcher"""
    return completing_forms_dispatcher[user_id]['unique_sent_form_id']


def completing_froms_dispatcher_is_user_in_list(user_id: int):
    """ Проверяет, заполняет ли сейчас пользователь форму"""
    return user_id in completing_forms_dispatcher.keys()

def completing_forms_dispatcher_get():
    """ Возвращает completing_forms_dispatcher (список с юзерами и  формами которые они сейчас заполняют)"""
    return completing_forms_dispatcher

def registerData_get_fio(user_id: int):
    """ Возвращает ФИО юзера из registerData"""
    return registerData[user_id]['chosen_fio']


def registerData_get_group(user_id: int):
    """ Возвращает группу юзера из registerData"""
    return registerData[user_id]['chosen_group']


def registerData_get_role(user_id: int):
    """ Возвращает роль юзера из registerData"""
    return registerData[user_id]['chosen_role']


def registerData_check_is_registered(user_id: int):
    """ Проверяет есть ли юзер в registerData"""
    return user_id in registerData.keys()


def send_forms_mem_get():
    """ Возвращает send_forms_mem (память с отправленынми формами)"""
    return send_forms_mem


def send_forms_mem_get_form(sent_form_id: int):
    """ Возвращает форму из send_forms_mem (память с отправленынми формами)"""
    return send_forms_mem[sent_form_id]


def send_forms_mem_get_form_sent_users(sent_form_id: int):
    """ Возвращает айди пользователей, которым отослана форма"""
    return send_forms_mem[sent_form_id]['info']['send_to_users_ids']


def send_forms_mem_get_form_completed_users(sent_form_id: int):
    """ Возвращает айди пользователей, которые прошли форму"""
    return send_forms_mem[sent_form_id]['info']['got_answers_from']


def unique_form_id_get():
    """ Возвращает счетчик созданных форм"""
    # print(' \n\nloool unique_form_id ', bot_elements.storages.all_storages.unique_form_id)
    return bot_elements.storages.all_storages.unique_form_id


def unique_sent_form_id_get():
    """ Возвращает счетчик отправленных форм"""
    # print('unique_sent_form_id ',bot_elements.storages.all_storages.unique_sent_form_id)
    return bot_elements.storages.all_storages.unique_sent_form_id


def temp_mem_for_answers_get():
    """ Возвращает все ответы на вопросы формы"""
    return temp_mem_for_answers
