from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from kivymd.uix.list.list import OneLineListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from Database import Connection
from utils import string_to_bytes
from AES import AESEncryptor
from textwrap import dedent
from TextStorage import TextStorage
from kivymd.app import MDApp


db = Connection()

class MenuScreen(MDScreen):
    website_screen_layout = ObjectProperty(None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Clock.schedule_interval(self.populate_website_list, 5)
        
    def populate_website_list(self):
        website_names = db.get_website_names()
        self.website_screen_layout.results_list.clear_widgets()
        if not website_names:
            return
        for id, website_name in website_names:
            if website_name is None:
                continue
            list_text = f'{id}. {website_name}'
            result_widget = OneLineListItem(text=list_text, on_release=self.show_options)
            self.website_screen_layout.results_list.add_widget(result_widget)
        
    def on_pre_enter(self):
        self.populate_website_list()
        
    def show_options(self, widget):
        # Get the website name from the id number and website name
        id_number, *website = widget.text.split('.')
        # Clear the whitespaces
        website = [value.strip() for value in website]
        full_website_name = '.'.join(website)
        
        # Update the website_name string so that we can use it in another function.
        self.current_website = full_website_name
        self.current_id = id_number
        TextStorage.id = id_number
        
        self.options_dialog = MDDialog(
            title=f'{self.current_id}. {self.current_website}',
            text=f'Pick an option.',
            buttons=[MDFlatButton(text='View login details', on_release=self.display_details),
                    MDFlatButton(text='Change details', on_release=lambda x:self.update_details(self.current_id, self.current_website)),
                    MDFlatButton(text='Delete details', on_release=self.show_delete_dialog),
                    MDFlatButton(text='Nevermind...', on_release=self.dismiss_options_dialog)]
        )
        
        self.options_dialog.open()
        
    def update_details(self, id, website_name):
        print(id, website_name)
        manager = self.parent
        self.dismiss_options_dialog(None)
        manager.current = 'data_update_screen'
        
    def show_delete_dialog(self, obj):
        self.delete_dialog = MDDialog(
            title='WARNING!',
            text=f'ARE YOU SURE YOU WANT TO DELETE THE DETAILS FOR {self.current_id}. {self.current_website}??',
            buttons=[
                MDFlatButton(text='YES', on_release=self.delete_details),
                MDFlatButton(text='On second thought...', on_release=self.dismiss_delete_dialog)
            ]
        )
        self.delete_dialog.open()
        
    def delete_details(self, obj):
        db.delete_entry(id=self.current_id, website_name=self.current_website)
        self.delete_done_dialog = MDDialog(
            title='Deletion complete.',
            text=f'Details for {self.current_id}. {self.current_website} have been deleted.',
            buttons=[
                MDFlatButton(text='Alright', on_release=self.dismiss_delete_done_dialog),
            ]
        )
        MDApp.get_running_app().update_website_list()
        self.delete_done_dialog.open()
            
    def display_details(self, widget):
        login_details = db.get_information(self.current_id, self.current_website)
        print(TextStorage.text)
        AES = AESEncryptor(TextStorage.text)
        id, website, URL, email, username, encrypted_password = login_details
        encrypted_password_bytes = string_to_bytes(encrypted_password)
        actual_password = AES.decrypt(encrypted_password_bytes)
        
        message = dedent(f"""
            [b]ID:[/b] {id}\n
            [b]Website:[/b] {website}\n
            [b]URL:[/b] {URL}\n
            [b]Email:[/b] {email}\n
            [b]Username:[/b] {username}\n
            [b]Password:[/b] {actual_password}\n
            
            Your password has also been copied to the clipboard.
        """)
        # copy(actual_password)
        self.information_dialog = MDDialog(
            title=f'Login details for \'{self.current_website}\'',
            text=message,
            buttons=[MDFlatButton(text='OKAY', on_release=self.dismiss_dialog)]
        )
        self.information_dialog.open()
        self.options_dialog.open()
        
    def dismiss_dialog(self, obj):
        self.information_dialog.dismiss()   
        
    def dismiss_options_dialog(self, obj):
        self.options_dialog.dismiss()   
        
    def dismiss_update_dialog(self, obj):
        self.update_dialog.dismiss()      

    def dismiss_delete_dialog(self, obj):
        self.delete_dialog.dismiss()
        
    def dismiss_delete_done_dialog(self, obj):
        self.delete_done_dialog.dismiss()
        self.dismiss_delete_dialog(0)
        self.dismiss_options_dialog(0)
