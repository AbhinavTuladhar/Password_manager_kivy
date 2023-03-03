from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from config_pass import MasterPasswordConfig
from Database import Connection
from AES import AESEncryptor
from TextStorage import TextStorage

master_password_configurer = MasterPasswordConfig()
db = Connection()


class MasterPasswordUpdateLayout(MDBoxLayout):
    original_password = ObjectProperty(None)
    new_password = ObjectProperty(None)
    new_password_confirmation = ObjectProperty(None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.org_error_dialog = MDDialog(
                text='Your original password does not match!',
                buttons=[MDRectangleFlatButton(text='OK!', on_release=self.dismiss_org_error_dialog)]
        )
        self.error_dialog = MDDialog(
                text='Your new password does not match!',
                buttons=[MDRectangleFlatButton(text='OK!', on_release=self.dismiss_error_dialog)]
        )
        self.success_dialog = MDDialog(
                text='Your master password has been successfully updated. The passwords in the database have also been updated.',
                buttons=[MDRectangleFlatButton(text='OK!', on_release=self.dismiss_success_dialog)]
        )
        
    def _clear_fields(self):
        # self.original_password.text = ''
        self.new_password.text = ''
        self.new_password_confirmation.text = ''
        
    
    def update_password(self):
        new_password_match = self.new_password.text == self.new_password_confirmation.text
        if new_password_match:
            _, _ = master_password_configurer.update_master_password(
                original_password=TextStorage.text,
                new_password=self.new_password.text
            )
            AES1 = AESEncryptor(TextStorage.text)
            AES2 = AESEncryptor(self.new_password.text)
            try:
                db.update_passwords(AES1, AES2)
            except:
                pass
            TextStorage.text = self.new_password.text
            self._clear_fields()
            self.success_dialog.open()
        else:
            self._clear_fields()
            self.error_dialog.open()
            
    def dismiss_success_dialog(self, obj):
        self.success_dialog.dismiss()
        
    def dismiss_error_dialog(self, obj):
        self.error_dialog.dismiss()
        
    def dismiss_org_error_dialog(self, obj):
        self.org_error_dialog.dismiss()
