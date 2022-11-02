from flask_login import UserMixin

#Получение пользователя из базы данных
class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.GetUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])
