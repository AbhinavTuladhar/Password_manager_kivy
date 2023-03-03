from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from password_generation import generate_password


class PasswordGeneratorScreenLayout(MDBoxLayout):
    password_field = ObjectProperty(None)
    uppercase_flag = BooleanProperty()
    lowercase_flag = BooleanProperty()
    symbol_flag = BooleanProperty()
    number_flag = BooleanProperty()
    password_length = NumericProperty()
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = MDDialog(
            text='Your password has been copied to the clipboard!',
            buttons=[MDRectangleFlatButton(text='OK!', on_release=self.dismiss_dialog)]
        )
        self.error_dialog = MDDialog(
            text='Please choose at least one option!',
            buttons=[MDRectangleFlatButton(text='OK!', on_release=self.dismiss_error_dialog)]
        )
        
    def dismiss_dialog(self, obj):
        self.dialog.dismiss()
        
    def generate_password_and_copy_to_clipboard(self):
        try:
            password = generate_password(
                lowercase_flag=self.lowercase_flag, uppercase_flag=self.uppercase_flag,
                symbol_flag=self.symbol_flag,digit_flag=self.number_flag,
                length=self.password_length
            )
            self.password_field.text = password
            # copy(password)
        except IndexError:
            self.error_dialog.open()
            
    def dismiss_error_dialog(self, obj):
        self.error_dialog.dismiss()
