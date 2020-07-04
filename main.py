import os

from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from classClient import ClientSocket
from kivy.properties import ListProperty, StringProperty

from kivymd.color_definitions import colors
from kivymd.uix.tab import MDTabsBase


class ContentNavigationDrawer(BoxLayout):
    pass


class Registration(Screen):
    text = StringProperty()
    color = ListProperty()

    def connect(self):
        if self.hostname:
            self.client = ClientSocket(self.hostname.text, 1802, self.login.text, self.passw.text)
        self.potok = threading.Thread(target=self.client.run)
        self.potok.start()
        return self.client

    erros_label = ObjectProperty(None)

    def test(self):
        self.manager.current = 'screen2'
        self.erros_label.text = 'Dctkdw'
        # WakeApp().test()

    def test2(self):
        # print(WakeApp().connect(self.hostname.text, self.login.text, self.passw.text))
        if WakeApp().connect(self.hostname.text):
            if WakeApp().checked(self.login.text, self.passw.text):
                self.manager.current = 'screen2'


class Manager(ScreenManager):
    pass


class Game(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class WakeApp(MDApp):
    screen_manager = ObjectProperty

    def __init__(self, **kwargs):
        # self.client = None
        self.title = "KivyMD Examples - Rectangle Text Field"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "900"
        self.client = ClientSocket()
        super().__init__(**kwargs)
        path_to_crop_image = "{}/demos/kitchen_sink/assets/crop-blur.jpg".format(
            self.directory
        )
        path_to_origin_image = "{}/demos/kitchen_sink/assets/blur.jpg".format(
            self.directory
        )

        if not os.path.exists(path_to_crop_image):
            crop_image(
                (Window.width, Window.height), path_to_origin_image, path_to_crop_image
            )

    def build(self):
        return Manager()

    def connect(self, hostname):
        self.client.connect(hostname)
        print(self.client.check)
        if self.client.check:
            return True
        else:
            return False

    def checked(self, login, passw):
        print(self.client)
        self.client.checked(login, passw)
        print(self.client.registred)
        if self.client.registred:
            return True
        else:
            return False


if __name__ == "__main__":
    WakeApp().run()
