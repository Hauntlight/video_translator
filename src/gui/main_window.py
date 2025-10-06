# In src/gui/main_window.py
import os

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from .controllers import GuiController


class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.controller = GuiController(self)

        # ... (La UI rimane visivamente la stessa) ...
        file_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.file_label = Label(text="Nessun file selezionato")
        file_button = Button(text="Seleziona Video (.mp4)", on_press=self.show_file_chooser)
        file_box.add_widget(self.file_label)
        file_box.add_widget(file_button)
        self.add_widget(file_box)

        self.text_editor = TextInput(
            text="Seleziona un video per iniziare...",
            readonly=True,
            font_size='14sp'
        )
        self.add_widget(self.text_editor)

        action_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.transcribe_button = Button(text="1. Trascrivi", on_press=self.controller.start_transcription,
                                        disabled=True)
        self.translate_button = Button(text="2. Traduci", on_press=self.controller.start_translation, disabled=True)
        self.generate_button = Button(text="3. Genera Video", on_press=self.controller.start_generation, disabled=True)

        action_box.add_widget(self.transcribe_button)
        action_box.add_widget(self.translate_button)
        action_box.add_widget(self.generate_button)
        self.add_widget(action_box)

        status_box = BoxLayout(orientation='vertical', size_hint_y=None, height=90)
        self.save_button = Button(text="Salva Modifiche al Testo Corrente", on_press=self.controller.save_current_text,
                                  disabled=True, size_hint_y=None, height=40)
        self.status_label = Label(text="Pronto.")
        self.progress_bar = ProgressBar(max=100, value=0)
        status_box.add_widget(self.save_button)
        status_box.add_widget(self.status_label)
        status_box.add_widget(self.progress_bar)
        self.add_widget(status_box)

        self.reset_ui()  # Imposta lo stato iniziale

    def show_file_chooser(self, instance):
        filechooser = FileChooserIconView(filters=['*.mp4'])
        filechooser.bind(selection=self.controller.select_file)
        self.popup = Popup(title="Seleziona un video", content=filechooser, size_hint=(0.9, 0.9))
        self.popup.open()

    def update_status(self, message, progress=None):
        self.status_label.text = message
        if progress is not None:
            self.progress_bar.value = progress

    def reset_ui(self):
        """Resetta la UI allo stato iniziale, in attesa di un file."""
        self.file_label.text = "Nessun file selezionato"
        self.text_editor.text = "Seleziona un video per iniziare..."
        self.text_editor.readonly = True
        self.transcribe_button.disabled = True
        self.translate_button.disabled = True
        self.generate_button.disabled = True
        self.save_button.disabled = True
        self.update_status("Pronto.")

    def set_state_ready_to_transcribe(self):
        """Abilita solo il pulsante di trascrizione."""
        self.text_editor.text = "Video caricato. Clicca 'Trascrivi' per iniziare."
        self.transcribe_button.disabled = False
        self.translate_button.disabled = True
        self.generate_button.disabled = True
        self.save_button.disabled = True
        self.update_status(f"File '{os.path.basename(self.controller.video_path)}' caricato.")

    def set_state_ready_to_translate(self, content):
        """Imposta la UI dopo aver caricato/creato una trascrizione."""
        self.text_editor.text = content
        self.text_editor.readonly = False
        self.transcribe_button.disabled = True
        self.translate_button.disabled = False
        self.generate_button.disabled = True
        self.save_button.disabled = False

    def set_state_ready_to_generate(self, content):
        """Imposta la UI dopo aver caricato/creato una traduzione."""
        self.text_editor.text = content
        self.text_editor.readonly = False
        self.transcribe_button.disabled = True
        self.translate_button.disabled = True
        self.generate_button.disabled = False
        self.save_button.disabled = False