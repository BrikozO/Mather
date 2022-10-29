import sqlite3


class AddDataBase:

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def AddUser(self, name, pswrd):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM accounts WHERE name LIKE '{name}'")
            res = self.__cur.fetchone()
            if res["count"] > 0:
                return False

            self.__cur.execute("INSERT INTO accounts VALUES(NULL, ?, ?)", (name, pswrd))
            self.__db.commit()
        except:
            return False

        return True

    def GetUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM accounts WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except:
            print("Ошибка получения данных из БД")

        return False

    def GetUserByLogin(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM accounts WHERE name = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except:
            print("Ошибка получения данных из БД")

        return False