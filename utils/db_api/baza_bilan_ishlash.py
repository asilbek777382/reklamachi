import sqlite3

class Database:
    def __init__(self, path_to_db="users.db"):
        self.path_to_db = path_to_db


    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE myfiles_teacher (
            id int NOT NULL,
            NAME varchar(255) NOT NULL,
            email varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())



    def select_all_user(self):
        sql = """
        SELECT * FROM myfiles_teacher
        """
        return self.execute(sql, fetchall=True)

    def select_user23(self, **kwargs):
        sql = 'SELECT * FROM myfiles_kirish WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_maxsulot(self):
        return self.execute('SELECT COUNT(*) FROM myfiles_hisobot;',fetchall=True)
    def count_maxsulot2(self):
        return self.execute('SELECT COUNT(*) FROM myfiles_baza_hisobot;',fetchall=True)
#--------------------------------------------------------------------------
    # def user(self, username: str, tg_id: int):
    #     sql = """
    #     INSERT INTO users (username, tg_id,) VALUES(?, ?)
    #     """
    #     self.execute(sql, parameters=(id, username, tg_id), commit=True)

#--------------------------------------------------------------------------

    def update_user_email(self, email, id):

        sql = f"""
        UPDATE myfiles_teacher SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def update_baza(self, max_sol_narx,max_kg, id):

        sql = f"""
        UPDATE myfiles_baza SET max_sol_narx=?,max_kg=? WHERE id=?
        """
        return self.execute(sql, parameters=(max_sol_narx,max_kg, id), commit=True)

    def update_xabar(self, xolati, id):

        sql = f"""
           UPDATE myfiles_set_message SET xolati=? WHERE id=?
           """
        return self.execute(sql, parameters=(xolati,id), commit=True)


    def update_xabar_matn(self, matn, id):

        sql = f"""
           UPDATE myfiles_set_message SET matn=? WHERE id=?
           """
        return self.execute(sql, parameters=(matn,id), commit=True)

    def update_xabar_rasm(self, rasm, id):

        sql = f"""
           UPDATE myfiles_set_message SET rasm=? WHERE id=?
           """
        return self.execute(sql, parameters=(rasm,id), commit=True)


    def update_xabar_video(self, video, id):

        sql = f"""
           UPDATE myfiles_set_message SET video=? WHERE id=?
           """
        return self.execute(sql, parameters=(video,id), commit=True)


    def update_songgi_xabarni_ochirish(self, songgi_xabarni_ochirish, id):

        sql = f"""
           UPDATE myfiles_set_message SET songgi_xabarni_ochirish=? WHERE id=?
           """
        return self.execute(sql, parameters=(songgi_xabarni_ochirish,id), commit=True)


    def update_xabarni_qadash(self, xabarni_qadash, id):

        sql = f"""
           UPDATE myfiles_set_message SET xabarni_qadash=? WHERE id=?
           """
        return self.execute(sql, parameters=(xabarni_qadash,id), commit=True)

#--------------------------------------------------------------------
    def user_qoshish(self,username:str,tg_id:int):
        sql = """
        INSERT INTO users (username,tg_id) VALUES(?, ?)
        """
        self.execute(sql, parameters=(username, tg_id), commit=True)
#--------------------------------------------------------------------
    def select_all_foydalanuvchilar(self):
        sql = """
        SELECT * FROM users
        """
        return self.execute(sql, fetchall=True)

    def delete_sh(self, **kwargs):
        sql = 'DELETE FROM myfiles_kirish WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, commit=True)

    def delete_message(self, **kwargs):
        sql = 'DELETE FROM myfiles_set_message WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, commit=True)

    def select_maxsulot(self, **kwargs):
        sql = 'SELECT * FROM myfiles_hisobot WHERE True'
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def export(self, **kwargs):
        sql = 'SELECT * FROM myfiles_baza_hisobot WHERE True'
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)
    def export2(self, **kwargs):
        sql = 'SELECT * FROM myfiles_baza WHERE True'
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)
    def export_ol(self, **kwargs):
        sql = 'SELECT * FROM myfiles_baza WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    # def filter_maxsulot(self, **kwargs):
    #     sql = 'SELECT * FROM users WHERE '
    #     sql, parameters = self.format_args(sql, kwargs)

    #     return self.execute(sql, parameters=parameters, fetchall=True)



    def max_q(self, max_kg:int,jami_narxi:int,sana:str,max_ismi: str, max_ol_narx: int, max_sol_narx: int):
        sql = """
        INSERT INTO myfiles_baza(max_sol_narx,max_ol_narx,max_ismi,jami_narxi,max_kg,sana) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(max_kg,max_sol_narx,max_ol_narx,max_ismi,jami_narxi,sana), commit=True)


    def max_q_hisobot(self, max_kg:int,jami_narxi:int,sana:str,max_ismi: str, max_ol_narx: int, max_sol_narx: int):
        sql = """
        INSERT INTO myfiles_baza_hisobot(max_sol_narx,max_ol_narx,max_ismi,jami_narxi,max_kg,sana) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(max_kg,max_sol_narx,max_ol_narx,max_ismi,jami_narxi,sana), commit=True)



    def max_hisobot(self,klient:str,max_ismi: str,  max_sol_narx: int,max_kg:int,jami_narxi:int,sana:str,max_ol_narx:int):
        sql = """
        INSERT INTO myfiles_hisobot(max_sol_narx,max_ismi,jami_narxi,max_kg,sana,klient,max_ol_narx) VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(max_kg,max_sol_narx,max_ismi,jami_narxi,sana,klient,max_ol_narx), commit=True)

    def add_user(self,login: str, parol: int,user_id:int):
        sql = """
        INSERT INTO myfiles_kirish(login,parol,user_id) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(login,parol,user_id), commit=True)
    def select_message(self, **kwargs):
        sql = 'SELECT * FROM myfiles_set_message WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_channels(self, **kwargs):
        sql = 'SELECT * FROM myfiles_set_message WHERE TRUE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_message_one(self, **kwargs):
        sql = 'SELECT * FROM myfiles_set_message WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)
    def add_message(self,gurux_id: str, users_id: int,xolati: str,matn: str,rasm: str,video: str,url_tugmachalar: str,vaqt: int,tugash_sanasi: str,xabarni_qadash: str,songgi_xabarni_ochirish: str):
        sql = """
        INSERT INTO myfiles_set_message(gurux_id,users_id,xolati,matn,rasm,video,url_tugmachalar,vaqt,tugash_sanasi,xabarni_qadash,songgi_xabarni_ochirish) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(gurux_id,users_id,xolati,matn,rasm,video,url_tugmachalar,vaqt,tugash_sanasi,xabarni_qadash,songgi_xabarni_ochirish), commit=True)

    def add_taksi(self,nomer: int, user_id: int, mal: str):
        sql = """
        INSERT INTO myfiles_taksi(nomer,user_id,mal) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(nomer,user_id,mal), commit=True)
    def add_rekmala(self,vaqt: int, rasm: int,id=int):
        sql = """
        INSERT INTO myfiles_reklama(vaqt,rasm,id) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(vaqt,rasm,id), commit=True)


    def add_foydalanuvchi(self,user_id: int, telefon: int):
        sql = """
        INSERT INTO myfiles_foydalanuvchi(user_id,telefon) VALUES(?, ?)
        """
        self.execute(sql, parameters=(user_id,telefon), commit=True)


    def select_id(self, **kwargs):
        sql = 'SELECT * FROM myfiles_yolovchi WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)


    def select_max_q(self, **kwargs):
        sql = 'SELECT * FROM myfiles_baza WHERE TRUE'
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)
    def select_user(self, **kwargs):
        sql = 'SELECT * FROM myfiles_kirish WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_max_id(self, **kwargs):
        sql = 'SELECT * FROM myfiles_baza WHERE id=?'
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)
    def delete_reklama(self):
        self.execute('DELETE FROM myfiles_reklama WHERE TRUE', commit=True)

    def delete_user(self):
        self.execute('DELETE * FROM myfiles_kirish WHERE ', commit=True)

    def select_mal(self, **kwargs):
        sql = 'SELECT * FROM myfiles_yolovchi WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)
    def select_reklama(self, **kwargs):
        sql = 'SELECT * FROM myfiles_reklama WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)
def logger(statement):
    print(f"""
-------------------------------------------------------
Executing:
{statement}
-------------------------------------------------------
""")

