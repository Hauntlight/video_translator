import kivy
from kivy.app import App
from src.gui.main_window import MainWindow
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

class VideoTranslatorApp(App):
    """
    Classe principale dell'applicazione Kivy.
    """
    def build(self):
        """
        Costruisce l'interfaccia utente.
        """
        self.title = "Video Translator"
        return MainWindow()

if __name__ == '__main__':
    VideoTranslatorApp().run()