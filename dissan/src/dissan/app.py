"""
Dissan app to view prices
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from controller.dbcontroller import DbController
from controller.odoocontroller import OdooController, OdooException



class DissanDistribuidora(toga.App):



    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        self.main_window = toga.MainWindow(title="DISSAN - Lista de precios")



        if DbController().is_first_run():
            main_box = toga.Box(style=Pack(direction=COLUMN))
            usr_label = toga.Label("Email: ", style=Pack(padding=(0, 5)))
            self.usr = toga.TextInput(style=Pack(flex=1))

            psw_label = toga.Label("Contraseña", style=Pack(padding=(0, 5)))
            self.psw = toga.PasswordInput(style=Pack(flex=1))

            usr_box = toga.Box(style=Pack(direction=ROW, padding=5))
            usr_box.add(usr_label)
            usr_box.add(self.usr)
            psw_box = toga.Box(style=Pack(direction=ROW, padding=5))
            psw_box.add(psw_label)
            psw_box.add(self.psw)
            login = toga.Button("Iniciar Sesión", on_press=self.login_usr, style=Pack(padding=5))
            main_box.add(usr_box)
            main_box.add(psw_box)
            main_box.add(login)
            self.error_label= toga.Label(text="", style=Pack(padding=(0, 5)))

            
            self.main_window.title="DISSAN - Iniciar Sesion"
            self.main_window.content = main_box
            self.main_window.show()

        else:
            self.listpriceWindow(self)





    def login_usr(self, args):
        self.odoo = OdooController()
        try:
            if self.odoo.authenticate(self.usr.value, self.psw.value):
                DbController().save_user_data(self.usr.value, self.psw.value)
                progessBar = toga.ProgressBar(max=100, value=1)
                progessBar.start()
                DbController().load_products(self.odoo.get_all_products(progressBar=progessBar))
                progessBar.stop()
                self.listpriceWindow(self)

        except OdooException as e:
            self.error_label.text=e.get_error()
            self.main_window.content.add(self.error_label)



    def listpriceWindow(self, widget):
        try:
            self.main_window.content.clear()
        except:
            pass
        options = toga.Group("Opciones", order=1)
        update = toga.Command(self.update_prices, "Actualizar lista",
                              tooltip="Actualiza los precios con el servidor", group=options)
        self.main_window.toolbar.add(update)
        main_box = toga.Box(style=Pack(direction=COLUMN))
        search_label = toga.Label("Buscar: ", style=Pack(padding=(0, 5)))
        self.search = toga.TextInput(style=Pack(flex=1), on_change=self.search_product)
        search_box = toga.Box(style=Pack(direction=ROW, padding=5))
        search_box.add(search_label)
        search_box.add(self.search)
        main_box.add(search_box)


        self.listprice=toga.Table(headings=["Codigo", "Descripcion", "Precio"], data=DbController().get_products(0,80), style=Pack(
                flex=1,
                padding_right=5,
                font_family="monospace",
                font_size=10,
                font_style="italic",
            ))

        main_box.add(self.listprice)

        self.main_window.content = main_box

        self.main_window.show()


    def search_product(self,args):
        self.listprice.data=DbController().search_product(self.search.value)

    def update_prices(self, args):
        self.odoo = OdooController()
        if(self.odoo.authenticate(DbController().get_user(),DbController().get_pswd())):
            progessBar = toga.ProgressBar(max=100, value=1)
            progessBar.start()
            DbController().load_products(self.odoo.get_products_to_update(date_from=DbController().get_last_update()), progessBar)
            progessBar.stop()
        else:
            pass
            #self.main_window.info_dialog("Error al autenticar el usuario")

def main():
    return DissanDistribuidora()

