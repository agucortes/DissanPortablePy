"""
Dissan app to view prices
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from controller.dbcontroller import DbController
from controller.odoocontroller import OdooController



class DissanDistribuidora(toga.App):


    odoo=OdooController("sergiov_1974@hotmail.com","espinillo212215")
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN))

        usr_label = toga.Label("Email: ", style=Pack(padding=(0, 5)))
        self.usr=toga.TextInput(style=Pack(flex=1))

        psw_label = toga.Label("Contraseña", style=Pack(padding=(0, 5)))
        self.psw=toga.PasswordInput(style=Pack(flex=1))

        usr_box = toga.Box(style=Pack(direction=ROW, padding=5))
        usr_box.add(usr_label)
        usr_box.add(self.usr)

        psw_box = toga.Box(style=Pack(direction=ROW, padding=5))
        psw_box.add(psw_label)
        psw_box.add(self.psw)

        login = toga.Button("Iniciar Sesión", on_press=self.login_usr,  style=Pack(padding=5))

        main_box.add(usr_box)
        main_box.add(psw_box)
        main_box.add(login)



        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
    def login_usr(self, args):
        print(self.usr.value)
        print(self.psw.value)
        print(DbController().get_products())


def main():
    return DissanDistribuidora()

