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


class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.build_load_popup()

    def build_load_popup(self):
        self.load_popup = ModalView(
            size_hint=(.5, .3)
        )

        self.grid = GridLayout()
        # button for loading test data

        # button for loading own data

        # button for loading from URL



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
