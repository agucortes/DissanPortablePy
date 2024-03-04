from dissan.src.dissan.controller import DbController
from dissan.src.dissan.controller.odoocontroller import OdooController




if __name__ == '__main__':
   db=DbController()
   db.create_data_structure()
   odoo= OdooController("sergiov_1974@hotmail.com","espinillo212215")

   p=odoo.get_all_products()
   db.load_products(p)


   #print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))




