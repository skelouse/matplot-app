from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
import matplotlib.pyplot as plt


class TestApp(App):
    def build(self):
        self.filename = (self.user_data_dir + "/test.png")
        plt.plot([1, 2, 3], [1, 2, 3])
        plt.savefig(self.filename)
        plt.clf()  # cla for multiple subplots
        layout = RelativeLayout()
        self.img = AsyncImage(source=self.filename, nocache=True)
        layout.add_widget(self.img)

        self.btn = Button(
            text='change',
            size_hint=(None, None))
        self.btn.bind(on_press=self.callback)
        layout.add_widget(self.btn)

        return layout

    def callback(self, event):
        plt.plot([1, 2, 3], [5, 9, 12])
        plt.savefig(self.filename)
        plt.clf()  # cla for multiple subplots
        self.img.source = self.filename
        self.img.reload()


TestApp().run()
