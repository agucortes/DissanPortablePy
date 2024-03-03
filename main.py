import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from controller.dbcontroller import DbController
from controller.odoocontroller import OdooController

class LoginScreen(Screen):


    def on_press_button(self, instance):
        print(self.usr.text)
        print(self.pswd.text)
        self.parent.transition.direction = 'left'
        self.parent.current = 'products'
        print('You pressed the button!')

class ProductsScreen(Screen):
    pass

class DissanApp(App):



    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(ProductsScreen(name='products'))

        return self.sm




if __name__ == '__main__':
   db=DbController()
   db.create_data_structure()
   odoo= OdooController("sergiov_1974@hotmail.com","espinillo212215")

   p=odoo.get_all_products()
   db.load_products(p)
#DissanApp().r

   #print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))




