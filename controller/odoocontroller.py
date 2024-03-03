import xmlrpc.client

class OdooController ():

    __url = "http://dissansa.no-ip.biz:8069"
    __db = "Dissan"

    def __init__(self, user="", password=""):
        if len(user) > 0 and len(password) > 0:
            self.authenticate(user, password)

    #Connect to odoo 8 api
    def __connect(self):
        try:
            self.__common=xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.__url))
            return True
        except xmlrpc.client.Fault as e:
            print(e.faultString)
            return False

    #Authenticate user, if correct, connect with api and retrive user name
    def authenticate(self, user, password):
        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.__url))
            self.__uid = common.authenticate(self.__db, user, password,  {})
            if self.__uid is not None:
                self.__pswd = password
                self.__user = user
                self.__connect()
                self.__name = self.__common.execute_kw(self.__db, self.__uid, self.__pswd, 'res.partner', 'search_read', [[('email', '=', self.__user)]], {'fields': ['name']})[0]['name']
                return True
            else:
                return False
        except xmlrpc.client.Fault as e:
            print(e.faultString)
            return False

    #Generic get model
    def __get_model(self, model, filter, fields):
        count = self.__common.execute_kw(self.__db, self.__uid, self.__pswd, model, 'search_count', [filter])
        res = []
        offset = 0
        pagination = 80
        while count > 0:
            ids = self.__common.execute_kw(self.__db, self.__uid, self.__pswd, model, 'search', [filter], {'offset': offset, 'limit': pagination})
            offset += pagination
            res.extend(self.__common.execute_kw(self.__db, self.__uid, self.__pswd, model, 'read', [ids], fields))
            if offset > count:
                offset -= pagination
                pagination = count - offset
                count = 0
        return res

    #Get all products from database
    def get_all_products(self, with_img=False):
        fields = {'fields': ['id', 'default_code', 'name_template', 'list_price', 'write_date']}
        if with_img:
            fields['fields'].append('image_small')
        return self.__get_model('product.product', [['active', '=', 'true'], ['sale_ok', '=', 'true']], fields)


    #Get products updated from date provided
    def get_products_to_update(self, date_from, with_img=False):

        fields = {'fields': ['id', 'default_code', 'name_template', 'list_price', 'write_date']}
        if with_img:
            fields['fields'].append('image_small')

        return self.__get_model('product.product', [['active', '=', 'true'], ['sale_ok', '=', 'true'], ['write_date', '>', date_from]], fields)









