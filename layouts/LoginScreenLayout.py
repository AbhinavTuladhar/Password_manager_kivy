from .CustomBoxLayout import CustomBoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from config_pass import MasterPasswordConfig
from TextStorage import TextStorage

master_password_configurer = MasterPasswordConfig()

class LoginScreenLayout(CustomBoxLayout):
    password_entered = ObjectProperty(None)
    authentication_status = BooleanProperty(False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_dialog = MDDialog(
                text='The password is incorrect.',
                buttons=[MDRectangleFlatButton(text='Enter again', on_release=self.dismiss_error_dialog)]
        )
        self.success_dialog = MDDialog(
                text='The password is correct! Welcome back!',
                buttons=[MDRectangleFlatButton(text='Yay', on_release=self.dismiss_success_dialog)]
        )
        
    def validate_password(self):
        self.authentication_status, _ = master_password_configurer.authenticate(self.password_entered.text)
        if not self.authentication_status:
            self.error_dialog.open()
            self.password_entered.text = ''
        else:
            self._update_master_password()
            self.success_dialog.open()
            
    def dismiss_success_dialog(self, obj):
        self.success_dialog.dismiss()
        
    def dismiss_error_dialog(self, obj):
        self.error_dialog.dismiss()
        
    def _update_master_password(self):
        TextStorage.text = self.password_entered.text
