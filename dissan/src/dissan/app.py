"""
Dissan app to view prices
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from controller.dbcontroller import DbController
from controller.odoocontroller import OdooController



class DissanDistribuidora(toga.App):


    #odoo=OdooController("sergiov_1974@hotmail.com","espinillo212215")
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN))
        self.main_window = toga.MainWindow(title="DISSAN - Lista de precios")
        options = toga.Group("Opciones", order=1)
        update = toga.Command(self.update_prices, "Actualizar lista",
                              tooltip="Actualiza los precios con el servidor", group=options)
        self.main_window.toolbar.add(update)

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

        self.login_window = toga.Window(title="DISSAN - Iniciar Sesion")
        self.login_window.content = main_box
        self.windows.add(self.login_window)
        if DbController().is_first_run():
            self.login_window.show()
        else:
            self.listpriceWindow(self)





    def login_usr(self, args):
        self.odoo = OdooController()
        try:
            if self.odoo.authenticate(self.usr.value,self.psw.value):
                DbController().save_user_data(self.usr.value, self.psw.value)
                progessBar = toga.ProgressBar(max=100, value=1)
                progessBar.start()
                DbController().load_products(self.odoo.get_all_products(progressBar=progessBar))
                progessBar.stop()
                self.listpriceWindow(self)

        except Exception as e:
            self.main_window.info_dialog(e)


    def listpriceWindow(self, widget):

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
        self.login_window.close()

    def search_product(self,args):
        self.listprice.data=DbController().search_product(self.search.value)

    def update_prices(self, args):
        self.odoo = OdooController()
        if(self.odoo.authenticate(DbController().get_user(),DbController().get_pswd())):
            DbController().load_products(self.odoo.get_products_to_update(date_from=DbController().get_last_update()))
        else:
            self.main_window.info_dialog("Error al autenticar el usuario")

def main():
    return DissanDistribuidora()

