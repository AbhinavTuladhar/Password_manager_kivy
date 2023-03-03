from kivymd.uix.boxlayout import MDBoxLayout


class CustomBoxLayout(MDBoxLayout):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'vertical'
        self.pos_hint = {'center_y': 0.5}
        self.spacing = "50dp"
        self.valign = 'center'
        self.padding = ["10dp", "10dp", "10dp", "10dp"]