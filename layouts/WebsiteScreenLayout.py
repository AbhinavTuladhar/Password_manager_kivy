from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list.list import OneLineListItem
from kivy.properties import ObjectProperty
from Database import Connection

db = Connection()

class WebsiteScreenLayout(MDBoxLayout):
    results_list = ObjectProperty(None)
    search_bar = ObjectProperty(None)
    count = 1
    
    def test_function(self):
        results = db.get_information(self.search_bar.text)
        self.results_list.clear_widgets()
        if results:
            website_name = results[1]
            result_widget = OneLineListItem(text=website_name)
            self.results_list.add_widget(result_widget)
 