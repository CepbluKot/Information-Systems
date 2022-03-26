import psycopg2 as ps2

class DataConnect:
    def __init__(self):
        try:
            self.con = ps2.connect(
                dbname = 'global_con_db',
                user = 'postgres',
                password = '752505',
                host = '127.0.0.1',
                port = 5432 
                )
            self.con.autocommit = True
            self.cursor = self.con.cursor()
        except:
            print("error")

    
    def __del__(self):
        self.cursor.close()
        self.con.close()
        print("Соединение закрыто")


    def par_and_in_tb(self, str1, list1):
        str1 += " ("
        for item in list1:
            str1 += item +','

        str1 = str1.rstrip(str1[-1])
        str1 += ") " 
        return str1


    def delete_db(self, name_tb, equality_cl, con_data):
        if len(equality_cl) != len(con_data):
            print("ERROR блять")
            return

        delete_com = 'delete from ' + name_tb + ' where '
        for i in range(0, len(equality_cl)):
            delete_com += equality_cl[i] + ' = ' + con_data[i]
        print(delete_com)

        try:
            self.cursor.execute(delete_com)
        except:
            "ERROR: delete_db"


    def update_db(self, name_tb, name_cl, new_data, equality_cl = [], con_data = []):
        if len(name_cl) != len(new_data)  and  len(equality_cl) != len(con_data):
            print("ERROR блять")
            return
        
        update_com = 'update ' + name_tb + ' set '
        for i in range(0, len(name_cl)):
            update_com += name_cl[i] + ' = ' + new_data[i]
        update_com += ' where '

        for i in range(0, len(equality_cl)):
            update_com += equality_cl[i] + ' = ' + con_data[i]
        print(update_com)

        try:
            self.cursor.execute(update_com)
        except:
            "ERROR: update_db"


    def insert_db(self, name_tb, name_cl, new_data):
        insert_com = "insert into "+ name_tb
        insert_com = self.par_and_in_tb(insert_com, name_cl) + "values"
        insert_com = self.par_and_in_tb(insert_com, new_data)
        

        print(insert_com)
        try:
            self.cursor.execute(insert_com)
        except:
            "ERROR: insert_db"
    

    def custom_insert(self, com = None):
        if com ==  None:
            com = str(input())
        
        print(com)
        self.cursor.execute(com)
        
        try:
            self.cursor.execute(com)
        except:
            print('ERROR: custom_insert')


    def __select_where(self, name_tb, name_cl):
        select_com = 'select '
        select_com = self.par_and_in_tb(select_com, name_cl) + ' from ' + name_tb + ' where '
        return select_com


    def __select_count(self, name_tb, name_cl):
        select_com = 'select count'
        select_com = self.par_and_in_tb(select_com, name_cl) + ' from ' + name_tb + ' where '
        return select_com


    def __select_max(self, name_tb, name_cl):
        select_com = 'select max'
        select_com = self.par_and_in_tb(select_com, name_cl) + ' from ' + name_tb
        return select_com


    def __select_choice(self, name_tb, name_cl, status):
        if status == 'where':
            return self.__select_where(name_tb, name_cl)
        elif status == 'count' or status == 'check':
            return self.__select_count(name_tb, name_cl)
        elif status == 'max':
            return self.__select_max(name_tb, name_cl)

    def select_db_where(self, name_tb, name_cl, equality_cl, con_data, status):
        if len(equality_cl) != len(con_data):
            print("ERROR блять")
            return

        select_com = self.__select_choice(name_tb,name_cl, status)
        for i in range (0, len(equality_cl)):
            select_com += str(equality_cl[i]) + ' = ' + str(con_data[i])  
            if i < len(equality_cl) - 1:
                select_com +=  ' and '

        print(select_com)
        try:
            self.cursor.execute(select_com)
        except:
            print('ERROR: select_db_where')
            return
        
        if status == 'check':
            if self.cursor.fetchone() == (0,):
                return True
            else:
                return False

        return self.cursor.fetchall()
    
    def select_db(self, name_tb, name_cl, add_com = ''):
        select_com = 'select '
        select_com = self.par_and_in_tb(select_com, name_cl) + ' from ' + name_tb + add_com
        print(select_com)

        try:
            self.cursor.execute(select_com)
        except:
            print('ERROR: select_db')
            return

        return self.cursor.fetchall()


    def custom_select(self, com = None):
        if com == None:
            com = str(input())
        print(com)

        self.cursor.execute(com)

        try:
            self.cursor.execute(com)
        except:
            print('ERROR: custom_select')
            return
        
        return self.cursor.fatchall()
