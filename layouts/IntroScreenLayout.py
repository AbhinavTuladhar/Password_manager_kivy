from .CustomBoxLayout import CustomBoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from config_pass import MasterPasswordConfig


master_password_configurer = MasterPasswordConfig()

class IntroScreenLayout(CustomBoxLayout):
    password_entered = ObjectProperty(None)
    password_confirmation = ObjectProperty(None)
    match_status = BooleanProperty(False)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_dialog = MDDialog(
                text='The passwords do not match',
                buttons=[MDRectangleFlatButton(text='Enter again', on_release=self.dismiss_dialog)]
        )
        self.success_dialog = MDDialog(
                text='The passwords match! Welcome!',
                buttons=[MDRectangleFlatButton(text='Enter again', on_release=self.dismiss_dialog)]
        )
        
    def register_password(self):
        self.match_status =  self.password_entered.text == self.password_confirmation.text
        if self.match_status:
            master_password_configurer.update_master_password(
                original_password=self.password_entered.text,
                new_password=self.password_confirmation.text    
            )   
        else:
            self.password_entered.text = ''
            self.password_confirmation.text = ''
            self.dialog = MDDialog(
                text='The password is incorrect.',
                buttons=[MDRectangleFlatButton(text='Enter again', on_release=self.dismiss_dialog)]
            )
            self.dialog.open()   
            
    def dismiss_dialog(self, obj):
        self.dialog.dismiss()
