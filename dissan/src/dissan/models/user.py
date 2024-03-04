'''
model for user, to manage the data
'''

class User ():
    __uid = None
    __user = None
    __pwd = None
    __name = None

    def __init__(self, uid, usr, pwd):
        self.__uid, self.__user, self.__pwd = uid, usr, pwd

    def get_usr(self):
        return self.__user
    def get_name(self):
        return self.__name

    def get_uid(self):
        return self.__uid

    def get_pwd(self):
        return self.__pwd