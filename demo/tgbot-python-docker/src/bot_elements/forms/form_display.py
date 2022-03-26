from aiogram import types
from bot_elements.getter.all_getters import temp_form_recipient_data_get_data, temp_mem_for_form_creator_get_data, mem_for_created_forms_get_creator_id, mem_for_created_forms_get_data, mem_for_created_forms_get_form_name, mem_for_created_forms_get


async def display_current_temp_mem_status(message: types.Message):
    """ Выводит сообщением содержимое создаваемого опроса"""
    form_mem = temp_mem_for_form_creator_get_data(user_id=message.chat.id)
    print('form_mem ', form_mem)
    recip_mem = temp_form_recipient_data_get_data(user_id=message.chat.id)
    print('recip_mem ', recip_mem)
    parsed_msg = "name: " + recip_mem['form_name'] + \
        ' ' + 'form_id: ' + str(recip_mem['form_id']) + "\n"
    if form_mem:
        question_number = 0
        for inside_mem in form_mem:
            if inside_mem['type'] == 'poll':
                parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + ' ' + '['+', '.join(
                    str(e) for e in inside_mem['options']) + ']' + ' ' + '/del' + str(question_number) + '\n')

            elif inside_mem['type'] == 'msg':
                parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] +
                                  ' ' + '/del' + str(question_number) + '\n')

            question_number += 1

        await message.answer(parsed_msg, reply_markup=types.ReplyKeyboardRemove())
    
    else:
        message.answer('Все плохо')


async def display_current_mem_status(message: types.Message):
    """ Выводит сообщением меню для работы с сохраненными опросами (id клиента определяет по message)"""
    full_message = ""
    memory = mem_for_created_forms_get()
    if memory:
        for index in memory:
            
            print(mem_for_created_forms_get_creator_id(form_id=index))

            if mem_for_created_forms_get_creator_id(form_id=index) == message.chat.id:
                selected_form = mem_for_created_forms_get_data(form_id=index)
                form_mem = selected_form
                print('form_mem ', form_mem)
                info = selected_form[-1]
                print('recip_mem ', info)
                
                parsed_msg = "\n ----- \nname: " + info['form_name'] + ' '+ 'form_id: ' + str(info['form_id']) + ' /send_' + str(index) + ' /rename_' + str(index) + ' /edit_'+ str(index)+ ' /del_' + str(index) +"\n"

                if form_mem:
                    
                    for inside_mem in form_mem:
                        if inside_mem['type'] == 'poll':
                            parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + ' ' + '['+', '.join(
                                str(e) for e in inside_mem['options']) + ']' + '\n')

                        elif inside_mem['type'] == 'msg':
                            parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + '\n')

                full_message += parsed_msg
        
        await message.answer(full_message, reply_markup=None)

    else:
        await message.answer('Хранилище форм пусто', reply_markup=None)


async def display_form(message: types.Message, form_id: int):
    """ Выводит в чат инфу о форме"""

    if message.chat.id == mem_for_created_forms_get_creator_id(form_id=form_id):
        memory = mem_for_created_forms_get_data(form_id=form_id)
        if memory:
            form_mem = memory

            parsed_msg = "name: " + mem_for_created_forms_get_form_name(form_id=form_id) + \
                ' ' + 'form_id: ' + str(form_id) + "\n"
            if form_mem:
                question_number = 0
                for inside_mem in form_mem:
                    if inside_mem['type'] == 'poll':
                        parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + ' ' + '['+', '.join(
                            str(e) for e in inside_mem['options']) + ']' + ' /rename' + str(form_id) + '_' + str(question_number) + ' /add_after' +  str(form_id) + '_' + str(question_number) + ' /edit' +  str(form_id) + '_' + str(question_number) + ' /del' +  str(form_id) + '_' + str(question_number) + '\n')

                    elif inside_mem['type'] == 'msg':
                        parsed_msg += str(inside_mem['type'] + ' ' + inside_mem['question'] + ' /rename' + str(form_id) + '_' + str(question_number) + ' /add_after' +  str(form_id) + '_' + str(question_number) + ' /del' +  str(form_id) + '_' + str(question_number) + '\n')

                    question_number += 1

                await message.answer(parsed_msg, reply_markup=types.ReplyKeyboardRemove())

        else:
            await message.answer("Хранилище форм пусто", reply_markup=types.ReplyKeyboardRemove())

    else:
        await message.answer("Вы не являетесь создателем формы", reply_markup=types.ReplyKeyboardRemove())
