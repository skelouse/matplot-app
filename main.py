from sys import platform as sysplatform
from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
import matplotlib.pyplot as plt


if sysplatform == 'linux' or sysplatform == 'win32':
    from kivy.config import Config
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'left', 0)
    Config.set('graphics', 'top', 0)
    Config.set('graphics', 'height', 496)
    Config.set('graphics', 'width', 800)
    Config.write()


class LoadPopup(ModalView):

    def __init__(self, **kwargs):
        super(LoadPopup, self).__init__(**kwargs)
        self.size_hint = (.5, .3)
        self.build()

    def build(self):
        self.load_grid = GridLayout(cols=1)
        # button for loading test data
        test_btn = Button(text="Load from test datasets")
        self.load_grid.add_widget(test_btn)
        test_btn.bind(on_press=self.load_test_data)

        # button for loading own data
        data_btn = Button(text="Load from storage")
        self.load_grid.add_widget(data_btn)
        data_btn.bind(on_press=self.load_from_storage)

        # button for loading from URL
        url_btn = Button(text="Load from URL")
        self.load_grid.add_widget(url_btn)
        url_btn.bind(on_press=self.load_from_url)

        self.add_widget(self.load_grid)

    def load_test_data(self, event):
        print("Loading data from app storage")

    def load_from_storage(self, event):
        print("Loading data from phone storage")

    def load_from_url(self, event):
        print("Loading data from URL")


class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.load_popup = LoadPopup()

    def build(self):
        fig, ax = plt.subplots(figsize=(8, 3.9))
        self.filename = (self.user_data_dir + "/test.png")
        plt.plot([1, 2, 3], [1, 2, 3])
        plt.savefig(self.filename)
        plt.clf()  # cla for multiple subplots

        layout = GridLayout(rows=3, padding=[0, 0, 0, -1])

        # grid on top 1 row
        self.top_grid = GridLayout(
            cols=5,
            size_hint_y=(.15),
            padding=[0, 0, 0, -1]
        )
        # Button for loading data
        load_btn = Button(text="Load Data")
        load_btn.bind(on_press=self.load)
        self.top_grid.add_widget(load_btn)

        # Button for setting x column

        # Button for setting y column multi-line selection

        # Button for 

        # Button for

        layout.add_widget(self.top_grid)

        self.img = AsyncImage(source=self.filename, nocache=True)
        layout.add_widget(self.img)

        # grid on bottom 1 row
        self.bottom_grid = GridLayout(
            cols=5,
            size_hint_y=(.15),
            padding=[0, 0, 0, -1]
        )
        
        # Button for share button

        # Button for color scheme


        layout.add_widget(self.bottom_grid)

        # self.btn = Button(
        #     text='change',
        #     size_hint=(None, None))
        # self.btn.bind(on_press=self.callback)
        # layout.add_widget(self.btn)

        return layout

    def load(self, event):
        self.load_popup.open()

    def callback(self, event):
        plt.plot([1, 2, 3], [5, 9, 12])
        plt.savefig(self.filename)
        plt.clf()  # cla for multiple subplots
        self.img.source = self.filename
        self.img.reload()


TestApp().run()
