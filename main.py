import os
import pandas as pd
from sys import platform as sysplatform
from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.factory import Factory
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
import matplotlib.pyplot as plt


if sysplatform == 'linux' or sysplatform == 'win32':
    from kivy.config import Config
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'left', 0)
    Config.set('graphics', 'top', 0)
    Config.set('graphics', 'height', 496)
    Config.set('graphics', 'width', 800)
    Config.write()


class FileChooserWindow(ModalView):
    def __init__(self, load_callback, **kwargs):
        self.load_callback = load_callback
        super(FileChooserWindow, self).__init__(**kwargs)
        self.layout = RelativeLayout()

        fc = FileChooserListView(
            filters=["*.csv", "*.xlsx", "*.txt"],
            size_hint=(.8, 1)
        )
        fc.bind(on_submit=self.file_chosen)
        self.layout.add_widget(fc)

        exit_btn = Button(
            text='Exit',
            size_hint=(.1, .1),
            pos_hint={'center_x': .9, 'center_y': .9}
            )
        exit_btn.bind(on_press=self.dismiss)
        self.layout.add_widget(exit_btn)

        self.add_widget(self.layout)

    def file_chosen(self, event, filename, *args):
        self.load_callback(filename[0])


class LoadPopup(ModalView):

    def __init__(self, **kwargs):
        super(LoadPopup, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self._type = ""
        self.size_hint = (.5, .3)
        self.build()
        self.modals = {
            'test': 0,
            'storage': 0,
            'url': 0
        }

    def get_modal(self, _type):
        # Create modals if not already created
        if _type == "test" and not self.modals[_type]:
            test_modal = ModalView()
            self.test_grid = GridLayout(cols=1)
            test_datasets = os.listdir("./test-data")
            for _set in test_datasets:
                btn = Button(text=_set)
                btn.bind(on_press=self.load_data)
                self.test_grid.add_widget(btn)
            test_modal.add_widget(self.test_grid)
            self.modals[_type] = test_modal

        elif _type == "storage":
            if not self.modals[_type]:
                fc = FileChooserWindow(
                    load_callback=self.load_data
                )
                self.modals[_type] = fc

        elif _type == "url":
            pass
        
        self._type = _type
        return self.modals[_type]

    def load_data(self, event):
        # Deal with csv, txt, or xlsx differences here
        if self._type == "test":
            df = pd.read_csv("./test-data/%s" % str(event.text))
        elif self._type == "storage":
            df = pd.read_csv(event)
        self.app.data = df
        self.modals[self._type].dismiss()
        self.dismiss()

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
        self.get_modal("test").open()


    def load_from_storage(self, event):
        self.get_modal("storage").open()

    def load_from_url(self, event):
        print("Loading data from URL")


class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.load_popup = LoadPopup()
        self.load_popup.bind(on_dismiss=self.load_data)
        self.data = None
        self.x_dropdown = None
        self.y_dropdown = None
        self.x_cols = []
        self.y_cols = []

    def load_data(self, event):
        print(self.data.head())
        cols = self.data.columns
        self.x_cols = []
        if self.x_dropdown:
            self.x_btn.unbind(on_release=self.x_dropdown.open)
        del self.x_dropdown
        self.x_dropdown = DropDown(dismiss_on_select=False)
        for col in cols:
            btn = ToggleButton(
                text=col,
                size_hint_y=None,
                height=44
            )
            btn.bind(on_release=lambda btn: self.x_dropdown.select(btn.text))
            self.x_dropdown.add_widget(btn)
        self.x_btn.bind(on_release=self.x_dropdown.open)
        self.x_dropdown.bind(on_select=self.select_xcol)

        self.y_cols = []
        if self.y_dropdown:
            self.y_btn.unbind(on_release=self.y_dropdown.open)
        del self.y_dropdown
        self.y_dropdown = DropDown(dismiss_on_select=False)
        for col in cols:
            btn = ToggleButton(
                text=col,
                size_hint_y=None,
                height=44
            )
            btn.bind(on_release=lambda btn: self.y_dropdown.select(btn.text))
            self.y_dropdown.add_widget(btn)
        self.y_btn.bind(on_release=self.y_dropdown.open)
        self.y_dropdown.bind(on_select=self.select_ycol)

    def select_xcol(self, event, col):
        if col in self.x_cols:
            self.x_cols.remove(col)
        else:
            self.x_cols.append(col)

    def select_ycol(self, event, col):
        if col in self.y_cols:
            self.y_cols.remove(col)
        else:
            self.y_cols.append(col)

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
        self.x_btn = Button(text="x column")
        self.top_grid.add_widget(self.x_btn)

        # Button for setting y column multi-line selection
        self.y_btn = Button(text="y column")
        self.top_grid.add_widget(self.y_btn)

        # Button for plotting

        self.plot_btn = Button(text="Plot it")
        self.plot_btn.bind(on_press=self.plot)
        self.top_grid.add_widget(self.plot_btn)

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
        if self.x_dropdown:
            self.x_dropdown.dismiss()
        if self.y_dropdown:
            self.y_dropdown.dismiss()
        self.load_popup.open()

    def plot(self, event):
        X = self.data[self.x_cols]
        y = self.data[self.y_cols]
        plt.plot(X, y)
        plt.legend()
        plt.savefig(self.filename)
        plt.clf()  # cla for multiple subplots
        self.img.source = self.filename
        self.img.reload()


TestApp().run()
