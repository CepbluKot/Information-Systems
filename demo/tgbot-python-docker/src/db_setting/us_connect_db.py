import back_function_db as bf


##### update data user #####
def del_prepod(tg_id):
    id_prepod = bf.db.select_db_where('prepod_tb', ['id'], ['gl_id'], [bf.find_id_global(str(tg_id))],'where')

    for item_pr in id_prepod:
        bf.db.delete_db('connect_tb', ['prepod_id'], [str(item_pr[0])])
    
    bf.db.delete_db('prepod_tb', ['gl_id'], [bf.find_id_global(str(tg_id))])
    bf.db.delete_db('global_tb', ['gl_teleg_id'], [bf.correct_str(str(tg_id))])


def del_student(tg_id):
    bf.db.delete_db('student_tb', ['gl_id'], [bf.find_id_global(tg_id)])
    bf.db.delete_db('global_tb', ['gl_teleg_id'], [bf.correct_str(str(tg_id))])

def del_us(tg_id):
    find_tg_role = bf.db.select_db_where('global_tb', ['gl_role'], ['gl_teleg_id'], [bf.correct_str(str(tg_id))], 'where')[0][0]
    
    if find_tg_role != (0,):
        if find_tg_role == 'prepod':
            del_prepod(tg_id)
        elif find_tg_role == 'student':
            del_student(tg_id)
    else:
        print(tg_id, ' ещё не существует, зарегистрируйтесь')


##### механизм для редактирования подписки на рассылку #####
def update_sub_news(id_us_tg, status):
    bf.db.update_db('global_tb', ['sub_newslet'], [str(status)], ['gl_teleg_id'], [bf.correct_str(str(id_us_tg))])


#####role: prepod / student; command: group / name 
def update_data_user(role ,command, new_data, id_us_tg):
    id_global = bf.find_id_global(id_us_tg)

    if command == 'name':
        bf.db.update_db(role + '_tb', role + '_' + command, [new_data], ['gl_tb'], [str(id_global)])
    elif command == 'group' and role == 'student':
        id_group = bf.find_id_group(new_data)
        bf.db.update_db(role + '_tb', role + '_' + command, [id_group], ['gl_tb'], [str(id_global)])


def find_teleg_group(list_name_group):
    group_us = []

    for name_group in list_name_group:
        name_group[0] = name_group[0].upper()

        data = bf.db.select_db_where('student_tb', ['gl_id'], ['group_id'], [bf.find_id_group(name_group[0])], 'where')
        for i in data:
            group_us.append(bf.db.select_db_where('global_tb', ['gl_teleg_id'], ['id'], [i[0]], 'where')[0][0])

    print(group_us)
    return group_us


def student_start(name_user, id_us_tg,name_group):
    bf.add_group(name_group, True)
    bf.add_student(name_user, id_us_tg, name_group)
    #bf.start_gr(name_group)

def prepod_start(name_user, id_us_tg):
    
    bf._correct_data_prepod(name_user, id_us_tg)
    bf.add_prepod(name_user, id_us_tg  = id_us_tg)
    bf.start_pr(input("введите ссылку на препода: "))


def reg_us(name_user, id_us_tg, role, group_stud = None):
    print(group_stud, role)

    if bf.add_us(id_us_tg, role):
        if role == 'student' and group_stud != None:
            student_start(name_user, id_us_tg, group_stud)
        elif role == 'prepod' and group_stud == None:
            prepod_start(name_user, id_us_tg)
    
    else:
        #update_us(id_us_tg)
        print(id_us_tg ,' ты уже зареган')


def pars_data_spisok(command):
    all_data = bf.db.select_db(command + '_tb', [command + '_name'])
    all_data_norm = []
    for item in all_data:
        all_data_norm.append(item[0])

    return all_data_norm 


def ck_data_db(teleg_id):
    id = bf.find_id_global(teleg_id)

    if int(id) == 0:
        return False
    else:
        return True

if __name__ == '__main__':
    pass