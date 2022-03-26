from bot_elements.storages.all_storages import temp_form_recipient_data 
from bot_elements.storages.all_storages import temp_mem_for_form_creator
from bot_elements.storages.all_storages import mem_for_created_forms
from bot_elements.storages.all_storages import send_forms_mem # todo!
from bot_elements.storages.all_storages import completing_forms_dispatcher 
from bot_elements.storages.all_storages import registerData # хз

# temp_mem_for_form_creator + temp_poll_recip_data -> mem_for_created_forms -> send_forms_mem -> completing_forms_dispatcher

def temp_form_recipient_data_remove_element(user_id: int):
    """ Убирает 1 элемент из temp_form_recipient_data"""
    temp_form_recipient_data.pop(user_id, None)


def temp_mem_for_form_creator_remove_form(user_id: int):
    """ Убирает 1 форму из temp_mem_for_form_creator"""
    temp_mem_for_form_creator.pop(user_id, None)


def temp_mem_for_form_creator_remove_form_element(user_id: int, delete_id: int):
    """ Убирает 1 элемент формы по delete_id из temp_mem_for_form_creator"""
    temp_mem_for_form_creator[user_id].pop(delete_id)


def mem_for_created_forms_delete_question(form_id: int, question_id: int):
    """ Убирает 1 элемент формы по question_id из mem_for_created_forms"""
    mem_for_created_forms[form_id].pop(question_id)


def mem_for_created_forms_delete_question(form_id: int):
    """ Убирает 1 форму из mem_for_created_forms"""
    mem_for_created_forms.pop(form_id, None)


def completing_forms_dispatcher_remove_session(user_id: int):
    """ Убирает 1 активную сессию  из completing_forms_dispatcher"""
    completing_forms_dispatcher.pop(user_id)
