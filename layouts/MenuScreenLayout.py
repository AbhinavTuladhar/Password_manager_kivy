from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, BooleanProperty


class MenuScreenLayout(MDBoxLayout):
    authenticated = BooleanProperty()
    website_screen_layout = ObjectProperty(None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)     
        