from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from Database import Connection
from AES import AESEncryptor
from TextStorage import TextStorage
from kivymd.app import MDApp
from utils import bytes_to_string

db = Connection()

class DatabaseEntryLayout(MDBoxLayout):
    name_field = ObjectProperty(None)
    website_URL_field = ObjectProperty(None)
    email_field = ObjectProperty(None)
    username_field = ObjectProperty(None)
    password_field = ObjectProperty(None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = MDDialog(
                text='Your information has been inserted into the database.',
                buttons=[MDRectangleFlatButton(text='OK!', on_release=self.dismiss_dialog)]
        )
        self.empty_dialog = MDDialog(
            text='The website field cannot be empty.',
            buttons=[MDRectangleFlatButton(text='OK!', on_release=self.dismiss_empty_dialog)]
        )
    
    def _clear_fields(self):
        self.name_field.text = ''
        self.website_URL_field.text = ''
        self.email_field.text = ''
        self.username_field.text = ''
        self.password_field.text = ''
    
    def insert_information(self):
        AES = AESEncryptor(password=TextStorage.text)
        if self.name_field.text == '':
            self.empty_dialog.open()
            return
        data = {
            'website': self.name_field.text,
            'URL': self.website_URL_field.text,
            'email': self.email_field.text,
            'username': self.username_field.text,
            'password': self.password_field.text
        }
        encrypted_password = AES.encrypt(data['password'])
        encrypted_password = bytes_to_string(encrypted_password)
        data['password'] = encrypted_password
        db.insert_data_from_input(data)
        
        self.dialog.open()
        self._clear_fields()
        MDApp.get_running_app().update_website_list()
        
    def dismiss_dialog(self, obj):
        self.dialog.dismiss()
        
    def dismiss_empty_dialog(self, obj):
        self.empty_dialog.dismiss()
 