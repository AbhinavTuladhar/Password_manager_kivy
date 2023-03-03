from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from pyperclip import copy
from config_pass import MasterPasswordConfig
from Database import Connection
from layouts.DatabaseEntryLayout import DatabaseEntryLayout
from layouts.DataUpdateLayout import DataUpdateLayout
from layouts.IntroScreenLayout import IntroScreenLayout
from layouts.LoginScreenLayout import LoginScreenLayout
from layouts.MasterPasswordUpdateLayout import MasterPasswordUpdateLayout
from layouts.MenuScreenLayout import MenuScreenLayout
from layouts.PasswordGeneratorScreenLayout import PasswordGeneratorScreenLayout
from layouts.WebsiteScreenLayout import WebsiteScreenLayout
from screens.MenuScreen import MenuScreen
from screens.OneUseScreens import *
from itertools import cycle

master_password_configurer = MasterPasswordConfig()
db = Connection()

password = 'The Legend of Heroes Trails of Cold Steel IV'
copy(password)

class AppScreenManager(MDScreenManager):
    pass
            
class PasswordManager(MDApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.theme_cycler = cycle(['Dark', 'Light'])
        
    def callback(self):
        self.theme_cls.theme_style = next(self.theme_cycler)
    
    def build(self):
        # self.theme_cls.theme_style = next(self.theme_cycler)
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = "Blue"
        self.screen_manager = Builder.load_file('design.kv')
        self.screen_manager.master_exists = master_password_configurer.check_master_password_exists()
        self.screen_manager.something_variable = 'One'
        return self.screen_manager
    
    def update_website_list(self):
        app = MDApp.get_running_app()
        manager = app.screen_manager
        menu_screen = manager.current_screen
        menu_screen.populate_website_list()
        
if __name__ == "__main__":
    app = PasswordManager()
    app.run()