from db_connect import DataConnect
import json

import sys
sys.path.append('/Users/igormalysh/Documents/codes/telegram_bot/')
import full_pars as fl

db = DataConnect()


def correct_str(t_item):
    t_item = "'" + t_item +"'" 
    return t_item 


##### add questions in DBase #####
def add_questions(question_n):
    question_n = correct_str(question_n)
    ques_ck = db.select_db_where('question_tb', ['id'], ['question_name'], [question_n], 'check')

    if ques_ck:
        db.insert_db('question_tb', ['question_name'], [question_n])


##### add GROUP questions in DBase #####
def add_group_questions(question_n, group_id):
    ques_ck = db.select_db_where('groupquestion_tb', ['q_id'], ['q_id', 'gp_question_id' ],[str(find_id_question(question_n)), group_id], 'check')

    if ques_ck:
        db.insert_db('groupquestion_tb', ['q_id', 'gp_question_id' ],[str(find_id_question(question_n)), group_id])


        ################## insurt_modul ##################
def add_us(id_us, role):
    id_us = correct_str(str(id_us))
    role = correct_str(str(role))

    id_us_ck = db.select_db_where('global_tb', ['id'], ['gl_teleg_id'], [id_us],'check')
    if id_us_ck:
        db.insert_db('global_tb', ['gl_teleg_id', 'gl_role'], [id_us, role])
        return True
    else:
        print(id_us, ' уже существует')
        return False


def add_lesson(name_lesson):
    name_lesson = correct_str(str(name_lesson))

    lesson_ck = db.select_db_where('lesson_tb', ['id'], ['lesson_name'] ,[name_lesson],'check')
    if lesson_ck:
        db.insert_db('lesson_tb', ['lesson_name'], [name_lesson])
    else:
        print(name_lesson, ' уже существует')


def _correct_data_prepod(name_prepod, id_us_tg):
    con_data =[correct_str(str(name_prepod)), find_id_global(1)]
    prepod_ck = db.select_db_where('prepod_tb', ['id'], ['prepod_name', 'gl_id'], con_data, 'check')

    if not prepod_ck:
        db.update_db('prepod_tb', ['gl_id'], [correct_str(str(id_us_tg))], ['prepod_name'], [correct_str(str(name_prepod))])


def add_prepod(name_prepod, id_us_tg = 1):
    con_data =[correct_str(str(name_prepod)), find_id_global(id_us_tg)]
    prepod_ck = db.select_db_where('prepod_tb', ['id'], ['prepod_name', 'gl_id'], con_data, 'check')

    if prepod_ck:
        print()
        db.insert_db('prepod_tb', ['prepod_name', 'gl_id'], con_data)
    else:
        print(name_prepod, ' уже существует')

def add_group(name_group, status):
    name_group = correct_str(str(name_group))
    status = correct_str(str(status))

    if db.select_db_where('group_tb', ['id'], ['group_name', 'group_approved']  ,[name_group, status], 'check'):
        db.insert_db('group_tb', ['group_name', 'group_approved'] , [name_group, status])
    else:
        print(name_group, ' уже существует')


def add_student(name_student, teleg_id, name_group):
    name_student = correct_str(str(name_student))
    con_data =[name_student, find_id_group(name_group)]

    if db.select_db_where('student_tb', ['id'], ['student_name', 'group_id' ]  ,con_data, 'check'):
        con_data.append(find_id_global(teleg_id))
        db.insert_db('student_tb', ['student_name', 'group_id', 'gl_id'], con_data)
    else:
        print(name_student, name_group,' уже существует')


        ################## select_modul ##################
def find_id_group(name_group):
    name_group = correct_str(str(name_group))
    return str(db.select_db_where('group_tb', ['id'], ['group_name'], [name_group], 'where')[0][0])


def find_id_lesson(name_lesson):
    name_lesson = correct_str(str(name_lesson))
    return str(db.select_db_where('lesson_tb', ['id'], ['lesson_name'], [name_lesson], 'where')[0][0])


def find_id_prepod(name_prepod):
    name_prepod = correct_str(str(name_prepod))
    print(str(db.select_db_where('prepod_tb', ['id'], ['prepod_name'], [name_prepod], 'where')))
    return str(db.select_db_where('prepod_tb', ['id'], ['prepod_name'], [name_prepod], 'where')[0][0])


def find_id_global(teleg_id):
    teleg_id = correct_str(str(teleg_id))
    data = db.select_db_where('global_tb', ['id'], ['gl_teleg_id'], [teleg_id],'where')
    print(data)
    if data != []: 
        return str(db.select_db_where('global_tb', ['id'], ['gl_teleg_id'], [teleg_id], 'where')[0][0])
    else:
        return '0'


###### select for polls ######
def find_id_survay(survay_code):
    try:
        return db.select_db_where('survay_tb', ['id'], ['survay_code'], [survay_code], 'where')[0][0]
    except:
        print('index error')


def find_id_question(question_n):
    question_n = correct_str(question_n)
    try:
        return db.select_db_where('question_tb', ['id'], ['question_name'], [question_n], 'where')[0][0]
    except:
        print('index error')


def max_index_group_question():
    try:
        max_el = db.select_db_where('groupquestion_tb', ['gp_question_id'], [], [] ,'max')[0][0]

        if max_el == None:
            return 0
        else:
            return max_el
    except:
        print('index error')


def max_index_survay():
    try:
        return db.select_db_where('survay_tb', ['survay_code'], [], [] ,'max')[0][0]
    except:
        print('index error')

def connect_gr_th(name_group, t_item):
    con_data = [find_id_group(name_group), find_id_prepod(t_item['prepod']), find_id_lesson(t_item['lesson']), correct_str(t_item['role'])]
    
    name_group = correct_str(str(name_group))
    t_item['role'] = correct_str(str(t_item['role']))
    t_item['lesson'] = correct_str(str(t_item['lesson']))
    t_item['prepod'] = correct_str(str(t_item['prepod']))

    if db.select_db_where('connect_tb', ['id'], ['group_id','prepod_id', 'lesson_id', 'teach_role'], con_data, 'check'):
        db.insert_db('connect_tb', ['group_id','prepod_id', 'lesson_id', 'teach_role'], con_data)
    

def data_for_group(name_group,t_item):
    add_lesson(t_item['lesson'])
    add_prepod(t_item['prepod'], 1)

    connect_gr_th(name_group,t_item)


def data_for_prepod(t_item):
    add_group(t_item['group'])
    add_lesson(t_item['lesson'])
    
    connect_gr_th(t_item['group'], t_item)


def start_pr(name_prepod):
    print('hey')
    data = fl.parse_prepod(name_prepod)
    print(data)
    for item in data:
        data_for_prepod(item)

def start_gr(name_group):
    data = fl.parse_group(name_group.upper())
    add_group(name_group, True)
    print(data)
    for item in data:
        data_for_group(name_group, item)

if __name__ == '__main__':
    start_gr('М3О-221Б-20')