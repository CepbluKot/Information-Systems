import sys

sys.path.append('/Users/igormalysh/Documents/codes/telegram_bot/db_setting')
import db_setting.us_connect_db as us_db
import db_setting.poll_connect_db as poll_db


###########################  БЛОК ДЛЯ РАБОТЫ С ПОЛЬЗОВАТЕЛЯМИ ################


def add_prepod(fio, rg_id , role): ####### Добавление препода
    us_db.reg_us(fio, id ,role)


def add_st(fio, tg_id, role, group): ####### Добавление студента
    us_db.reg_us(fio, tg_id, role, group_stud = group)


def list_all_group(): ####### Выводит списком все группы
    return us_db.pars_data_spisok('group')


def check_valid_us(tg_id): ####### Проверка на то зарегестрирован ли пользователь
   return us_db.ck_data_db(tg_id)



def find_role_us(tg_id): ####### Возвращает роль пользователя
    return us_db.bf.db.select_db_where('global_tb', ['gl_role'], ['gl_teleg_id'], [str(tg_id)], 'where')[0][0]


def find_fio_us(tg_id): ####### Возвращает ФИО пользователя
    return us_db.bf.db.select_db_where('student_tb', ['student_name'], ['gl_id'], [str(tg_id)], 'where')[0][0]


def find_us_for_survay(groups): ####### Проверка на то зарегестрирован ли пользователь
    users_id_list = us_db.find_teleg_group(groups)


def update_data_user(role ,command, new_data, id_us_tg): #####role: prepod / student; command: group / name
    us_db.update_data_user(role ,command, new_data, id_us_tg)


def update_sub_news(id_us_tg, status): ##### механизм для редактирования подписки на рассылку #####
    us_db.update_sub_news(id_us_tg, status)


def delete_user(tg_id): ####### Удаление пользователя
    us_db.del_us(tg_id)



###########################  БЛОК ДЛЯ РАБОТЫ С ФОРМАМИ ###################


def create_new_form(from_id, to_group, data_survay): ####### Создание новой формы
    poll_db.add_survay(from_id, to_group, data_survay)


def add_new_answer(new_answer): ####### Добавление нового результата опроса
    poll_db.add_answer_for_survay(new_answer)


print(find_fio_us(123))