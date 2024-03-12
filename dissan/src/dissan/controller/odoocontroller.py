import xmlrpc.client
import toga
import requests


class OdooController():
    __url = "http://server.dissansa.com.ar:8069"
    __db = "dissan"

    # def __init__(self, user="", password=""):
    #    if len(user) > 0 and len(password) > 0:
    #       return self.authenticate(user, password)
    #    else:
    #        return AttributeError
    #    return None

    # Connect to odoo 8 api
    def __connect(self):
        try:
            self.__common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.__url))
            return True
        except xmlrpc.client.Fault as e:
            return False

    # Authenticate user, if correct, connect with api and retrive user name
    def authenticate(self, user, password):
        try:
            requests.get("http://www.google.com", timeout=3)
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.__url))
            self.__uid = common.authenticate(self.__db, user, password, {})

            if self.__uid is not False:
                self.__pswd = password
                self.__user = user
                self.__connect()
                self.__name = self.__common.execute_kw(self.__db, self.__uid, self.__pswd, 'res.users', 'search_read',
                                                       [[('id', '=', self.__uid)]], {'fields': ['name']})[0]['name']
                return True
            else:
                raise OdooException("Login Error")
        except xmlrpc.client.Fault:
            raise OdooException("Server Error")
        except requests.ConnectionError:
            raise OdooException("Conection Error")

    # Generic get model
    def __get_model(self, model, filter, fields, progressBar=None):
        count = self.__common.execute_kw(self.__db, self.__uid, self.__pswd, model, 'search_count', [filter])
        res = []
        offset = 0
        pagination = 80
        # PROGRESS BAR FOR TOGA
        if progressBar is not None:
            progressionStep = 100 / count

        while count > 0:
            ids = self.__common.execute_kw(self.__db, self.__uid, self.__pswd, model, 'search', [filter],
                                           {'offset': offset, 'limit': pagination})
            offset += pagination
            # update progressbar
            if progressBar is not None:
                progressBar.value = progressionStep * offset
            res.extend(self.__common.execute_kw(self.__db, self.__uid, self.__pswd, model, 'read', [ids], fields))
            if offset > count:
                offset -= pagination
                pagination = count - offset
                count = 0
        return res

    # Get all products from database
    def get_all_products(self, progressBar=None, with_img=False):
        fields = {'fields': ['id', 'default_code', 'name_template', 'list_price', 'write_date']}
        if with_img:
            fields['fields'].append('image_small')
        return self.__get_model('product.product', [['active', '=', 'true'], ['sale_ok', '=', 'true']], fields,
                                progressBar)

    # Get products updated from date provided
    def get_products_to_update(self, date_from, progressBar=None, with_img=False):
        print(date_from)
        fields = {'fields': ['id', 'default_code', 'name_template', 'list_price', 'write_date']}
        if with_img:
            fields['fields'].append('image_small')

        return self.__get_model('product.product',
                                [['active', '=', 'true'], ['sale_ok', '=', 'true'], ['write_date', '>', date_from]],
                                fields, progressBar)


class OdooException(Exception):
    __error = ""

    def __init__(self, error=""):
        self.__error = error

    def get_error(self):
        return self.__error
