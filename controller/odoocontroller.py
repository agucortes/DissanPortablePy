import xmlrpc.client
from controller.dbcontroller import DbController
class OdooController():
    __dbconection= DbController()
    __url="http://dissansa.no-ip.biz:8069"
    __db="dissandb"
    __uid=None
    __common=None
    __pswd=None
    def connect(self):
        try:
            self.__common=xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            return True
        except xmlrpc.client.Fault as e:
            print(e.faultString)
            return False

    def authenticate(self, user, password):
        self.__uid = self.__common.authenticate(self.__db, user, password,  {})
        if self.__uid is not None:
            self.__pswd = password
            return True
        else:
            return False

    def update_products(self, with_img=False):
        #search for products in odoo database and update sqlite db
        count = self.__common.execute_kw(self.__db, self.__uid, self.__pswd, 'products.products', 'search_count', [[['1', '=', '1']]])
        products = []
        offset = 0
        pagination = 200
        while count > 0:
            res = self.__common.execute_kw(self.__db, self.__uid, self.__pswd, 'products.products', 'search', [[['1', '=', '1']]], {'offset': offset, 'limit': pagination})
            offset += pagination

            if offset > count:
                offset -= pagination
                pagination = count - offset
                count = 0
            for prod in res:
                products.append(prod)










