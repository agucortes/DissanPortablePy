'''
model for products
'''

class Product ():
    __id = None
    __code = None
    __name = None
    __price = None
    __image = None

    def __init__(self, id, code, name, price, image=None):
        self.__id, self.__code, self.__name, self.__price, self.__image = id, code, name, price, image

