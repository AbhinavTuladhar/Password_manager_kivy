from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from Database import Connection
from AES import AESEncryptor
from TextStorage import TextStorage
from kivymd.app import MDApp
from utils import bytes_to_string

db = Connection()

class DataUpdateLayout(MDBoxLayout):
    name_field = ObjectProperty(None)
    website_URL_field = ObjectProperty(None)
    email_field = ObjectProperty(None)
    username_field = ObjectProperty(None)
    password_field = ObjectProperty(None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _clear_fields(self):
        self.name_field.text = ''
        self.website_URL_field.text = ''
        self.email_field.text = ''
        self.username_field.text = ''
        self.password_field.text = ''
    
    def update_information(self):
        self.success_dialog = MDDialog(
            title='[b]Success![/b]',
            text='Details have been updated!',
            buttons=[
                MDFlatButton(text='ok', on_release=self.dismiss_success_dialog)
            ]
        )
        AES = AESEncryptor(password=TextStorage.text)
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
        db.update_all_information(ID=TextStorage.id, data=data)

        self._clear_fields()
        MDApp.get_running_app().update_website_list()
        self.success_dialog.open()
        
    def dismiss_success_dialog(self, obj):
        self.success_dialog.dismiss()
