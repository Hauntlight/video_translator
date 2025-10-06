import os
import yaml
import threading
from kivy.clock import Clock
from src.core import audio_processing, speech_to_text, text_processing, translation, text_to_speech
from src.core.utils import setup_directories, get_output_paths
from src.io import file_saver, file_loader
from src.io.logs import get_logger

logger = get_logger(__name__)


class GuiController:
    def __init__(self, view):
        self.view = view
        self.video_path = None
        self.output_paths = None
        self.current_stage = None

        with open('config/settings.yaml', 'r') as f:
            self.config = yaml.safe_load(f)

        setup_directories(self.config)

    def select_file(self, filechooser, selection):
        if not selection:
            self.view.popup.dismiss()
            return

        self.video_path = selection[0]
        self.view.file_label.text = os.path.basename(self.video_path)
        self.output_paths = get_output_paths(self.video_path, self.config)
        logger.info(f"File selezionato: {self.video_path}")

        self.view.popup.dismiss()

        translated_path = self.output_paths['translated_transcription']
        if os.path.exists(translated_path):
            logger.info(f"Trovato file di traduzione esistente: {translated_path}")
            content = file_loader.read_text_file(translated_path)
            if content:
                self.current_stage = 'translation'
                self.view.set_state_ready_to_generate(content)
                self.view.update_status("Caricata traduzione esistente. Pronto per generare il video.")
                return

        transcribed_path = self.output_paths['transcription']
        if os.path.exists(transcribed_path):
            logger.info(f"Trovato file di trascrizione esistente: {transcribed_path}")
            content = file_loader.read_text_file(transcribed_path)
            if content:
                self.current_stage = 'transcription'
                self.view.set_state_ready_to_translate(content)
                self.view.update_status("Caricata trascrizione esistente. Pronto per la traduzione.")
                return

        logger.info("Nessun file di testo trovato. Si parte dalla trascrizione.")
        self.view.set_state_ready_to_transcribe()

    def start_transcription(self, instance):
        if not self.video_path:
            self.view.update_status("Errore: Selezionare prima un file video.")
            return

        instance.disabled = True
        thread = threading.Thread(target=self._run_transcription_flow)
        thread.start()

    def _run_transcription_flow(self):
        try:
            Clock.schedule_once(lambda dt: self.view.update_status("1/3 - Estrazione audio...", 10))
            audio_path = audio_processing.extract_audio(self.video_path, self.output_paths['audio'])
            if not audio_path: raise Exception("Estrazione audio fallita")

            Clock.schedule_once(lambda dt: self.view.update_status("2/3 - Segmentazione audio...", 40))
            segments = audio_processing.segment_audio(audio_path)
            if not segments: raise Exception("Segmentazione audio fallita")

            Clock.schedule_once(
                lambda dt: self.view.update_status("3/3 - Trascrizione in corso (potrebbe richiedere tempo)...", 70))
            temp_dir = self.config['output']['temp_dir']
            transcribed_lines = speech_to_text.transcribe_audio_segments(segments, temp_dir)

            transcribed_text = "\n".join(transcribed_lines)
            self.current_stage = 'transcription'
            file_saver.save_text_file(transcribed_text, self.output_paths['transcription'])

            Clock.schedule_once(lambda dt: self.view.set_state_ready_to_translate(transcribed_text))
            Clock.schedule_once(
                lambda dt: self.view.update_status("Trascrizione completata. Puoi modificare il testo.", 100))
        except Exception as e:
            logger.error(f"Errore nel flow di trascrizione: {e}")
            Clock.schedule_once(lambda dt: self.view.update_status(f"Errore: {e}"))
            Clock.schedule_once(lambda dt: self.view.transcribe_button.setter('disabled')(self.view, False))

    def save_current_text(self, instance):
        content = self.view.text_editor.text
        if self.current_stage == 'transcription':
            path = self.output_paths['transcription']
            logger.info(f"Trascrizione (IT) modificata e salvata in {path}")
        elif self.current_stage == 'translation':
            path = self.output_paths['translated_transcription']
            logger.info(f"Traduzione (EN) modificata e salvata in {path}")
        else:
            return

        file_saver.save_text_file(content, path)
        self.view.update_status("Modifiche salvate con successo.")

    def start_translation(self, instance):
        instance.disabled = True
        self.view.update_status("Traduzione in corso...", 0)
        thread = threading.Thread(target=self._run_translation_flow)
        thread.start()

    def _run_translation_flow(self):
        try:
            transcription_content = self.view.text_editor.text
            parsed_data = text_processing.parse_transcription_file(transcription_content)
            original_sentences = [item['text'] for item in parsed_data]

            Clock.schedule_once(lambda dt: self.view.update_status("Traduzione delle frasi...", 30))
            target_lang = self.config['languages']['target']
            translated_texts = translation.translate_sentences(original_sentences, target_lang)

            translated_lines = []
            for i, data in enumerate(parsed_data):
                line = f"[{data['timestamp']}][{data['duration']}] \"{translated_texts[i]}\""
                translated_lines.append(line)

            translated_text = "\n".join(translated_lines)
            self.current_stage = 'translation'
            file_saver.save_text_file(translated_text, self.output_paths['translated_transcription'])

            Clock.schedule_once(lambda dt: self.view.set_state_ready_to_generate(translated_text)) # <-- RIGA CORRETTA

        except Exception as e:
            logger.error(f"Errore nel flow di traduzione: {e}")
            Clock.schedule_once(lambda dt: self.view.update_status(f"Errore: {e}"))
            Clock.schedule_once(lambda dt: self.view.translate_button.setter('disabled')(self.view, False))

    def start_generation(self, instance):
        instance.disabled = True
        self.view.save_button.disabled = True
        thread = threading.Thread(target=self._run_generation_flow)
        thread.start()

    def _run_generation_flow(self):
        try:
            Clock.schedule_once(lambda dt: self.view.update_status("1/3 - Analisi del testo tradotto...", 10))
            translated_content = self.view.text_editor.text
            parsed_data = text_processing.parse_transcription_file(translated_content)
            translated_texts = [item['text'] for item in parsed_data]

            Clock.schedule_once(lambda dt: self.view.update_status("2/3 - Generazione audio...", 40))
            target_lang = self.config['languages']['target']
            temp_dir = self.config['output']['temp_dir']
            final_audio_track = text_to_speech.create_final_audio_track(parsed_data, translated_texts, temp_dir,
                                                                        target_lang)
            file_saver.save_audio_file(final_audio_track, self.output_paths['translated_audio'])

            Clock.schedule_once(lambda dt: self.view.update_status("3/3 - Assemblaggio video finale...", 80))
            file_saver.combine_video_and_audio(
                self.video_path,
                self.output_paths['translated_audio'],
                self.output_paths['final_video']
            )

            Clock.schedule_once(
                lambda dt: self.view.update_status(f"Completato! Video salvato in {self.output_paths['final_video']}",
                                                   100))

        except Exception as e:
            logger.error(f"Errore nel flow di generazione: {e}")
            Clock.schedule_once(lambda dt: self.view.update_status(f"Errore: {e}"))
        finally:
            Clock.schedule_once(lambda dt: self.view.generate_button.setter('disabled')(self.view, False))
            Clock.schedule_once(lambda dt: self.view.save_button.setter('disabled')(self.view, False))