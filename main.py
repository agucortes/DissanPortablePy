from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

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
    DissanApp().run()




