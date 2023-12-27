import asyncio
import base64
import glob
import json
import platform
import random
import sys
from pathlib import Path

from PIL import Image
from PySide6.QtCore import QSize, Qt, QThread, Signal, Slot
from PySide6.QtGui import QIcon, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPlainTextEdit,
    QTreeWidgetItem,
    QWidget,
)
from qt_material import apply_stylesheet

import cpp_server_gen
import exllamav2_server_gen
from character_window import Ui_CharacterForm
from chat_window import Ui_ChatWindow

# Constants for the directories and file names
APP_ICON = Path("assets/icons/appicon.png")
INSTRUCT_PRESETS_DIR = Path("presets/Assistants")
CHARACTER_PRESETS_DIR = Path("presets/Characters")
CARDS_PRESETS_DIR = Path("presets/Cards")
SETTINGS_FILE = Path("saved/settings.json")
SESSION_FILE = Path("saved/session.json")
PARAMS_DIR = Path("presets/model_params")


class CharacterWindow(QWidget, Ui_CharacterForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_window_icon()
        self.saveButton.clicked.connect(self.save)

    def save(self):
        # Check if character name is not empty
        if not self.is_character_name_filled():
            print("--- Must fill in character name")
            return

        turn_template = self.get_turn_template()
        char_dict = self.get_character_data(turn_template)
        self.write_to_file(char_dict)
        print("--- Saved character file")

    def set_window_icon(self):
        icon = QIcon()
        icon.addFile(str(APP_ICON), QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

    def is_character_name_filled(self):
        return bool(self.charName.text().strip())

    def get_turn_template(self):
        return (
            self.charTemplate.text()
            if self.charTemplate.text().strip()
            else "<|user|> <|user-message|>\n<|bot|> <|bot-message|>\n"
        )

    def get_character_data(self, turn_template):
        return {
            "name": self.charName.text(),
            "persona": self.charPersona.toPlainText(),
            "scenario": self.charScenario.toPlainText(),
            "example_dialog": self.charExampleDialog.toPlainText(),
            "tags": self.charTags.text(),
            "turn_template": turn_template,
        }

    def write_to_file(self, char_dict):
        file_name = f"{CHARACTER_PRESETS_DIR}/{self.charName.text()}.json"
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(char_dict, file, indent=4)


class InputTextEdit(QPlainTextEdit):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.last_key = 0

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Return and self.last_key != 16777248:
            self.ui.generateButton.click()
        self.last_key = int(event.key())


class SettingsManager:
    def __init__(self):
        pass

    def _get_theme(self, ui):
        if ui.themeDarkRadio.isChecked():
            return "dark"
        elif ui.themeLightRadio.isChecked():
            return "light"
        elif ui.themeNativeRadio.isChecked():
            return "native"

    def save_settings(self, ui):
        theme = self._get_theme(ui)
        settings = {
            "prefs": {
                "stream": ui.streamCheck.isChecked(),
                "cache": ui.cacheCheck.isChecked(),
                "user_name": ui.usernameLine.text(),
                "bot_name": ui.botnameLine.text(),
                "stop_strings": ui.custStopStringLine.text(),
                "system_prompt_check": ui.customSysPromptCheck.isChecked(),
                "system_prompt": ui.customSysPromptText.toPlainText(),
                "auto_save_session": ui.autoSaveSessionCheck.isChecked(),
                "auto_add_stopstring": ui.stopStringAutoCheck.isChecked(),
                "backend": "exllamav2"
                if ui.backendExllamaCheck.isChecked()
                else "llama.cpp",
                "theme": theme,
            },
            "cpp_params": {
                "preset": ui.paramPresets_comboBox.currentText(),
                "max_new_tokens": ui.max_new_tokensSpin.value(),
                "repeat_last_n": ui.repeatLastSpin.value(),
                "n_keep": ui.keepLastNSpin.value(),
            },
        }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
                json.dump(settings, file, indent=4)
            print("--- Saved settings")
        except FileNotFoundError as error:
            print(f"--- Could not save settings:\n{error}")

    def load_settings(self, ui):
        try:
            with open(
                SETTINGS_FILE,
                "r",
                encoding="utf-8",
            ) as file:
                settings = json.load(file)
                self._update_ui(ui, settings)
                print("--- Loaded settings")
        except FileNotFoundError:
            print("--- Could not load settings")
            ui.set_themes("dark")

    def _update_ui(self, ui, settings):
        prefs = settings["prefs"]
        ui.streamCheck.setChecked(prefs["stream"])
        ui.cacheCheck.setChecked(prefs["cache"])
        ui.usernameLine.setText(prefs["user_name"])
        ui.botnameLine.setText(prefs["bot_name"])
        ui.custStopStringLine.setText(prefs["stop_strings"])
        ui.customSysPromptCheck.setChecked(prefs["system_prompt_check"])
        ui.customSysPromptText.setPlainText(prefs["system_prompt"])
        ui.autoSaveSessionCheck.setChecked(prefs["auto_save_session"])
        ui.stopStringAutoCheck.setChecked(prefs["auto_add_stopstring"])
        backend = prefs["backend"]
        if backend == "exllamav2":
            ui.backendExllamaCheck.setChecked(True)
        else:
            ui.backendCppCheck.setChecked(True)

        if prefs["theme"] == "dark":
            ui.themeDarkRadio.setChecked(True)
        elif prefs["theme"] == "light":
            ui.themeLightRadio.setChecked(True)
        elif prefs["theme"] == "native":
            ui.themeNativeRadio.setChecked(True)
        ui.set_themes(prefs["theme"])

        basic_params = settings["cpp_params"]
        ui.paramPresets_comboBox.setCurrentText(basic_params["preset"])
        ui.max_new_tokensSpin.setValue(basic_params["max_new_tokens"])
        ui.repeatLastSpin.setValue(basic_params["repeat_last_n"])
        ui.keepLastNSpin.setValue(basic_params["n_keep"])


class CharacterCard:
    """Get character card"""

    def __init__(self):
        pass

    def get_card_data(self, card_file, user_name):
        try:
            print("--- Reading character card...")
            img = Image.open(f"{CARDS_PRESETS_DIR}/{card_file}.png")
            exif_data = img.info
            decoded_data = base64.b64decode(exif_data["chara"])
        except FileNotFoundError:
            return "File not found."

        final = decoded_data.decode("utf-8")

        try:
            result = json.loads(final)
            result = result["data"]
        except KeyError:
            return "Invalid data format."

        template = {
            "turn_template": "<|user|> <|user-message|>\n<|bot|> <|bot-message|>\n",
            "sys_template": "<|system-message|>\n\n",
            "system_message": "",
            "user_name_prefix": "",
            "bot_name_prefix": "",
        }

        personality = f"Personality: {result['personality'].strip()}\n\n"
        scenario = f"Scenario: {result['scenario'].strip()}\n\n"

        template["system_message"] = (
            f"Name: {result['name']}\n\n"
            f"Persona: {result['description']}\n\n"
            f"{personality if result['personality'].strip() else ''}"
            f"{scenario if result['scenario'].strip() else ''}"
            f"Tags: {', '.join(result['tags']) if 'tags' in result else ''}\n\n"
            f"{result['mes_example'] if result['mes_example'].strip() else ''}\n\n"
            f"{result['first_mes']}\n\n"
        ).replace("<START>", "")

        def replace_placeholders(message):
            message = (
                str(message)
                .replace("{{char}}", result["name"])
                .replace("{{user}}", user_name)
                .replace("{{Char}}", result["name"])
                .replace("{{User}}", user_name)
            )
            return message

        template["display_text"] = replace_placeholders(result["first_mes"])
        template["system_message"] = replace_placeholders(template["system_message"])

        template["user_name_prefix"] = f"{user_name}:"
        template["bot_name_prefix"] = f"{result['name']}:"

        return template


class text_gen_thread(QThread):
    final_resultReady = Signal(bool, list)
    resultReady = Signal(str)

    def __init__(self, params: dict, backend: str):
        super().__init__()
        self.params = params
        self.stop_flag = False
        self.stream_enabled = self.params["stream"]
        self.backend = backend

    def run(self):
        try:
            if self.backend == "llama.cpp":
                self._generate()
            else:
                self._exllamav2_generate()
        except Exception as error:
            print(f"--- Error: Failed to generate:\n{error}")
            self.final_resultReady.emit(False, None)

    def _generate(self):
        if self.stream_enabled:
            self._generate_with_streaming()
        else:
            self._generate_nostream()

    def _generate_with_streaming(self):
        final_text = ""
        response = ""
        for response in cpp_server_gen.generate_with_streaming(self.params):
            if self.stop_flag:
                break
            # Append the response to the final text and emit the result ready signal
            final_text += response["content"]
            self.resultReady.emit(response["content"])
        self._emit_final_result(final_text, response)

    def _generate_nostream(self):
        # Get generated text without streaming
        response = cpp_server_gen.generate_nostream(self.params)
        self._emit_final_result(response["content"], response)

    def _exllamav2_generate(self):
        if self.stream_enabled:
            self._exllamav2_streaming()
        else:
            self._exllamav2_generate_nostream()

    def _exllamav2_streaming(self):
        async def get_response():
            final_text = ""
            response = ""
            async for response in exllamav2_server_gen.generate_streaming(self.params):
                if self.stop_flag:
                    break
                final_text += response
                self.resultReady.emit(response)
            return final_text, response

        final_text, response = asyncio.run(get_response())
        self._emit_final_result(final_text, response)

    def _exllamav2_generate_nostream(self):
        # Get generated text without streaming
        response = exllamav2_server_gen.launch(self.params)
        final_text = response["response"]
        self._emit_final_result(final_text, response=None)

    def _emit_final_result(self, final_text: str, response):
        final_result = [final_text.strip(), response]
        self.final_resultReady.emit(True, final_result)

    def stop(self):
        self.stop_flag = True


class ChatWindow(QMainWindow, Ui_ChatWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_window_icon()

        self.settings_manager = SettingsManager()
        self.character_window = CharacterWindow()

        self.add_contacts_launch()
        self.load_params_presets()
        self.settings_manager.load_settings(self)
        self.apply_params_preset()
        self.connect_signals()

        self.session_dict = {}
        self.bot_prompt = ""
        self.chat_input_history = []
        self.text_gen_thread = None
        self.page_mode = "Chat"
        self.continue_chat = False
        self.final_prompt_template = {}
        self.bot_name = None
        self.contact_parent = None

        # Add custom text input class
        self.inputText = InputTextEdit(self)
        self.inputText.setObjectName("inputText")
        self.inputText.setMaximumSize(QSize(16777215, 100))
        self.gridLayout_5.addWidget(self.inputText, 2, 0, 1, 1)

    def set_window_icon(self):
        icon = QIcon()
        icon.addFile(str(APP_ICON), QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.status_bar_msg("Status: Ready")

    def closeEvent(self, event):
        # Close the child window when the parent window is closed
        self.character_window.close()
        event.accept()

    def connect_signals(self):
        # Connect buttons to their respective functions
        self.generateButton.clicked.connect(self.launch_page_mode)
        self.actionAbout.triggered.connect(QApplication.aboutQt)
        self.actionSave_settings.triggered.connect(
            lambda: self.settings_manager.save_settings(self)
        )
        self.actionReload_contacts.triggered.connect(self.add_contacts_launch)
        self.actionCharacter.triggered.connect(self.character_window.show)

        self.clearButton.clicked.connect(self.history_clear)
        self.stopButton.clicked.connect(self.stop_textgen)
        self.rewindButton.clicked.connect(self.rewind_history)
        self.retryButton.clicked.connect(self.retry_launcher)
        self.continueButton.clicked.connect(self.continue_launcher)
        self.imgFileButton.clicked.connect(self.image_select)

        self.themeDarkRadio.clicked.connect(lambda: self.set_themes("dark"))
        self.themeLightRadio.clicked.connect(lambda: self.set_themes("light"))
        self.themeNativeRadio.clicked.connect(lambda: self.set_themes("native"))

        self.actionExit.triggered.connect(self.close)
        self.actionSave_session.triggered.connect(self.save_session)
        self.actionLoad_session.triggered.connect(self.manual_load_history_file)

        # Connect comboboxes to their respective functions
        self.inputHistoryCombo.activated.connect(self.set_chat_input_history)
        self.paramPresets_comboBox.activated.connect(self.apply_params_preset)
        self.contactsTree.itemClicked.connect(self.manage_contacts)
        self.textTabWidget.currentChanged.connect(self.manage_page_mode)

        # Connect sliders to their respective spin boxes and vice versa
        self.connect_slider_spinbox(self.temperatureSlider, self.temperatureSpin)
        self.connect_slider_spinbox(
            self.repetition_penaltySlider, self.repetition_penaltySpin
        )
        self.connect_slider_spinbox(self.top_pSlider, self.top_pSpin)
        self.connect_slider_spinbox(self.typical_pSlider, self.typical_pSpin)
        self.connect_slider_spinbox(self.freqPenaltySlider, self.freqPenaltySpin)
        self.connect_slider_spinbox(
            self.presencePenaltySlider, self.presencePenaltySpin
        )
        self.connect_slider_spinbox(self.tfszSlider, self.tfszSpin)
        self.connect_slider_spinbox(self.minPSlider, self.minpSpin)

    def connect_slider_spinbox(self, slider, spinbox):
        slider.valueChanged.connect(lambda: spinbox.setValue(slider.value() / 100))
        spinbox.valueChanged.connect(lambda: slider.setValue(spinbox.value() * 100))

    def add_contacts_launch(self):
        self.contactsTree.clear()

        # Adding top-level items
        top_level_items = ["Assistants", "Characters", "Cards"]
        self.contactsTree.addTopLevelItems(
            [QTreeWidgetItem([title]) for title in top_level_items]
        )

        self.contactsTree.headerItem().setText(0, "Contacts")

        self.add_contacts(0, INSTRUCT_PRESETS_DIR, "json")
        self.add_contacts(1, CHARACTER_PRESETS_DIR, "json")
        self.add_contacts(2, CARDS_PRESETS_DIR, "png")

        self.contactsTree.expandAll()

    def add_contacts(self, chat_mode_index, directory, file_extension):
        presets = [
            preset
            for preset in glob.glob(f"{directory}/*.{file_extension}")
            if Path(preset).exists()
        ]
        presets.sort()  # sort the list of files alphabetically

        for preset in presets:
            preset_stem = Path(preset).stem
            item = QTreeWidgetItem([preset_stem])
            self.contactsTree.topLevelItem(chat_mode_index).addChild(item)

    def load_params_presets(self):
        param_preset_load = glob.glob(f"{PARAMS_DIR}/*.settings")
        param_preset_load.sort()

        for param_preset in param_preset_load:
            param_preset_stem = Path(param_preset).stem
            self.paramPresets_comboBox.addItem(param_preset_stem)

        self.paramPresets_comboBox.setCurrentText("Default")

    def apply_params_preset(self):
        current_preset = self.paramPresets_comboBox.currentText()
        preset_file = f"{PARAMS_DIR}/{current_preset}.settings"

        with open(
            preset_file,
            "r",
            encoding="utf-8",
        ) as file:
            param_preset_name = json.load(file)

        # Set the values of the spin boxes and sliders according to the parameters
        self.temperatureSpin.setValue(float(param_preset_name["temp"]))
        self.temperatureSlider.setValue(int(param_preset_name["temp"] * 100))
        self.top_pSpin.setValue(float(param_preset_name["top_p"]))
        self.top_pSlider.setValue(int(param_preset_name["top_p"] * 100))
        self.top_kSpin.setValue(int(param_preset_name["top_k"]))
        self.top_kSlider.setValue(int(param_preset_name["top_k"]))
        self.typical_pSlider.setValue(int(param_preset_name["typical_p"]))
        self.typical_pSpin.setValue(int(param_preset_name["typical_p"] * 100))
        self.tfszSlider.setValue(float(param_preset_name["tfs"]))
        self.tfszSpin.setValue(int(param_preset_name["tfs"] * 100))
        self.repetition_penaltySpin.setValue(float(param_preset_name["rep_pen"]))
        self.repetition_penaltySlider.setValue(int(param_preset_name["rep_pen"] * 100))
        self.mirostatMode.setValue(int(param_preset_name["mirostat_mode"]))
        self.mirostatTau.setValue(int(param_preset_name["mirostat_tau"]))
        self.mirostatEta.setValue(float(param_preset_name["mirostat_eta"]))

    def get_toolbox_index(self):
        # Get current index from textTabWidget, return None if textTabWidget is None
        return self.textTabWidget.currentIndex() if self.textTabWidget else None

    def manage_contacts(self, contact):
        # If a contact is provided, get related info and set window title
        if contact.parent() and not self.text_gen_thread:
            self.bot_name = contact.text(0)
            self.contact_parent = contact.parent().text(0) if contact.parent() else None
            self.history_display(not bool(self.session_dict.get(contact.text(0))))

            if self.contact_parent == "Cards":
                self.get_template(True)

            else:
                self.get_template(False)
            self.generateButton.setEnabled(True)
            if self.session_dict[self.bot_name]["context"]:
                self.button_manager(False, False)
            else:
                self.button_manager(True, True)
                self.display_sys_prompt()

            self.setWindowTitle(f"AI Messenger - {contact.text(0)}")

            # Display system prompt

    def manage_page_mode(self, tab_index):
        # Check the value of toolbox and update page mode accordingly
        self.inputText.setEnabled(tab_index != 1 if tab_index is not None else False)

    def launch_page_mode(self, retry_textgen=None):
        if self.text_gen_thread:
            return

        self.page_mode = (
            "Chat" if self.textTabWidget.currentIndex() == 0 else "Notebook"
        )

        user_input = (
            (retry_textgen or self.inputText.toPlainText().strip())
            if self.page_mode == "Chat"
            else self.notebookTextEdit.toPlainText()
        )

        if self.page_mode == "Chat" and user_input and self.session_dict:
            self.text_chat_mode(user_input)
        elif self.page_mode == "Notebook" and user_input:
            self.text_notebook_mode(user_input)

    def text_chat_mode(self, user_input):
        self.add_chat_messages("user_msgs", user_input)
        self.add_chat_messages("bot_msgs", "")
        self.update_context()
        self.chat_display()
        self.inputText.clear()
        self.launch_backend()
        self.session_dict[self.bot_name]["bot_msgs"].pop()
        self.add_chat_input_history(user_input)

    def text_notebook_mode(self, user_input):
        self.prev_notebook_text = user_input
        self.launch_backend()

    # Define a helper function to get the directory path from a dialog
    def save_session(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            None, "Save File", "", "JSON Files (*.json)", options=options
        )

        if file_name:
            self.write_history_file(file_name, True)

    # Set the chat input field to the saved history
    def set_chat_input_history(self):
        if self.inputHistoryCombo.count() >= 1:
            self.inputText.setPlainText(
                self.chat_input_history[self.inputHistoryCombo.currentIndex()]
            )

    # Add the chat input to the combo box and the history list
    def add_chat_input_history(self, chat_input):
        if self.inputHistoryCombo.findText(chat_input) == -1:
            self.chat_input_history.append(chat_input)
            chat_input = chat_input.replace("\n", "")[:128]
            self.inputHistoryCombo.addItem(chat_input)

    def status_bar_msg(self, msg):
        self.statusbar.showMessage(msg)

    def update_generation_status(self, generation_enabled, results):
        info_message = ""

        if results and not generation_enabled and self.backendCppCheck.isChecked():
            try:
                # print(results["generation_settings"])
                tps = round(results["timings"]["predicted_per_second"], 2)
                context_size = str(results["tokens_cached"])
                max_context = results["generation_settings"]["n_ctx"]
                time_taken = round((results["timings"]["predicted_ms"] / 1000), 2)
                model = Path(results["generation_settings"]["model"]).stem

                info_message = f" [Speed: {tps} t/s | Context size: {context_size}/{max_context} | Time: {time_taken}s | Model: {model}]"
            except (
                KeyError
            ) as e:  # Better to catch specific exceptions instead of generalizing.
                print(f"--- No data for: {str(e)}")

        status = "Generating..." if generation_enabled else f"Completed{info_message}"
        self.status_bar_msg(f"Status: {status}")

    def button_manager(self, enable_mode, clear=False):
        inverted_button_state = not enable_mode
        buttons = [
            self.continueButton,
            self.clearButton,
            self.rewindButton,
            self.retryButton,
        ]
        for button in buttons:
            button.setEnabled(inverted_button_state)
        if not clear:
            self.stopButton.setEnabled(enable_mode)
            self.generateButton.setEnabled(inverted_button_state)
            self.notebookTextEdit.setReadOnly(enable_mode)

    def display_sys_prompt(self):
        display_text = (
            self.customSysPromptText.toPlainText()
            if self.customSysPromptCheck.isChecked()
            else self.final_prompt_template["display_text"]
        )

        self.chatTextEdit.setMarkdown(display_text)

    def history_reset(self):
        self.session_dict[self.bot_name] = {
            "user_msgs": [],
            "bot_msgs": [],
            "context": "",
        }

    def history_clear(self):
        self.write_history_file(SESSION_FILE, manual=True)
        self.history_reset()
        if self.page_mode == "Chat":
            self.chatTextEdit.clear()
        else:
            self.notebookTextEdit.clear()
        self.button_manager(True, True)
        self.display_sys_prompt()

    def history_display(self, first_launch=False):
        if first_launch:
            self.load_history_file(SESSION_FILE)
            if self.bot_name not in self.session_dict:
                self.history_reset()
        self.chat_display()

    def write_history_file(self, file_name, manual=False):
        if self.autoSaveSessionCheck.isChecked() or manual:
            session_history = dict(self.session_dict)
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(session_history, file, indent=4)
                # print("--- Wrote session file")

    def load_history_file(self, file_name):
        if Path(file_name).exists():
            print("--- Loading session history file")
            with open(file_name, "r", encoding="utf-8") as file:
                session_history = json.load(file)
                if self.bot_name in session_history:
                    self.session_dict = session_history

    def manual_load_history_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            None, "Session File", "", "JSON Files (*.json)", options=options
        )

        if file_name and self.session_dict:
            self.load_history_file(file_name)
            if self.page_mode == "Chat":
                self.chat_display()

    def get_file_path(self, title, filter):
        file_path = QFileDialog.getOpenFileName(self, title, "", filter)[0]
        return file_path

    # Browse for an image to load
    def image_select(self):
        image = self.get_file_path(
            "Open file", "Image Files (*.png *.jpg *.jpeg *.webp)"
        )
        if image:
            self.imgFileLine.setText(image)

    def reset_history(self):
        self.session_dict[self.bot_name] = {
            "user_msgs": [],
            "bot_msgs": [],
            "context": "",
        }
        if self.chatTextEdit.toPlainText():
            self.chatTextEdit.clear()
            self.generateButton.setEnabled(True)

    def chat_display(self):
        bot_display_name = self.get_bot_display_name()
        display_text = self.get_display_text(bot_display_name)
        self.update_chat_text_edit(display_text)

    def get_bot_display_name(self):
        if self.botnameLine.text():
            return self.botnameLine.text()
        elif self.contact_parent != "Assistants":
            return self.bot_name
        else:
            return self.botnameLine.placeholderText()

    def get_display_text(self, bot_display_name):
        display_text = ""
        for user_msg, bot_msg in zip(
            self.session_dict[self.bot_name]["user_msgs"],
            self.session_dict[self.bot_name]["bot_msgs"],
        ):
            display_text += f"""**<span style="color:#a92828">{self.usernameLine.text()}</span>**

{user_msg}

**<span style="color:#3194d0">{bot_display_name}</span>**

{bot_msg}

"""
        return (
            display_text
            # .replace("\n", "<br />")
            .replace("<START>", "").replace("<END>", "")
        )

    def update_chat_text_edit(self, display_text):
        self.chatTextEdit.clear()
        self.chatTextEdit.setMarkdown(display_text.strip())
        if self.bot_name != "\n\n":
            self.chatTextEdit.append("")
        self.scroll_to_bottom()

    def get_chat_presets(self):
        contact_mode = {
            "Assistants": "presets/Assistants",
            "Characters": "presets/Characters",
        }[self.contact_parent]

        final_template = {}

        with open(
            f"{contact_mode}/{self.bot_name}.json", "r", encoding="utf-8"
        ) as file:
            # print("--- Getting chat preset...")
            chat_preset = json.load(file)

        def get_preset(chat_preset, template_type):
            if template_type == "presets/Characters":
                character_template = (
                    "<|user|>: <|user-message|>\n<|bot|>: <|bot-message|>\n"
                )
                final_template["user_name_prefix"] = f"{self.usernameLine.text()}:"
                final_template["system_message"] = (
                    f"Name: {chat_preset['name']}\n\n"
                    f"Persona: {chat_preset['persona']}\n\n"
                    f"Scenario: {chat_preset['scenario'].strip()}\n\n"
                    f"Tags: {chat_preset['tags']}"
                    f"{chat_preset['example_dialog']}"
                )
                final_template["system_message"] = final_template[
                    "system_message"
                ].replace("{{user}}", final_template["user_name_prefix"])
                final_template["sys_template"] = "<|system-message|>\n\n"
                final_template["turn_template"] = character_template
                final_template["bot_name_prefix"] = chat_preset["name"]
                final_template["display_text"] = str(
                    chat_preset["example_dialog"]
                ).replace("{{user}}", final_template["user_name_prefix"])
            else:
                final_template["sys_template"] = chat_preset["context"]
                final_template["turn_template"] = chat_preset["turn_template"]
                final_template["user_name_prefix"] = chat_preset["user"]
                final_template["bot_name_prefix"] = chat_preset["bot"]
                final_template["system_message"] = chat_preset["system_message"]
                final_template["display_text"] = chat_preset["system_message"]
            return final_template

        final_template = get_preset(chat_preset, contact_mode)

        return final_template

    def get_template(self, cards):
        if cards:
            self.final_prompt_template = CharacterCard().get_card_data(
                self.bot_name, self.usernameLine.text()
            )
        else:
            self.final_prompt_template = self.get_chat_presets()

    def update_context(self):  ## Fix custom sys prompt
        if self.charInstructCheck.isChecked() and self.contact_parent != "Assistants":
            user_pfx = (
                f"### Instruction:\n{self.final_prompt_template['user_name_prefix']}"
            )
            bot_pfx = f"### Response:\n{self.final_prompt_template['bot_name_prefix']}"
        else:
            user_pfx, bot_pfx = (
                self.final_prompt_template["user_name_prefix"],
                self.final_prompt_template["bot_name_prefix"],
            )

        self.final_prompt_template["system_message"] = (
            self.customSysPromptText.toPlainText()
            if self.customSysPromptCheck.isChecked()
            else self.final_prompt_template["system_message"]
        )
        self.final_prompt_template["sys_template"] = self.final_prompt_template[
            "sys_template"
        ].replace("<|system-message|>", self.final_prompt_template["system_message"])
        user_template, self.bot_prompt = self.final_prompt_template[
            "turn_template"
        ].split("<|bot-message|>")
        user_prompt = user_template.replace("<|user|>", user_pfx).replace(
            "<|bot|>", bot_pfx
        )

        updated_context = "".join(
            [
                (user_prompt.replace("<|user-message|>", user_msg))
                + bot_msg
                + self.bot_prompt
                for user_msg, bot_msg in zip(
                    self.session_dict[self.bot_name]["user_msgs"],
                    self.session_dict[self.bot_name]["bot_msgs"],
                )
            ]
        )

        self.session_dict[self.bot_name]["context"] = (
            self.final_prompt_template["sys_template"] + updated_context
        )

        if self.contact_parent == "Characters":
            self.final_prompt_template[
                "user_name_prefix"
            ] = f"{self.usernameLine.text()}"

    def rewind_history(self):
        if not self.page_mode == "Chat":
            return
        if (
            "user_msgs" in self.session_dict[self.bot_name]
            and self.session_dict[self.bot_name]["user_msgs"]
        ):
            # Remove the last user message from the session dictionary
            self.session_dict[self.bot_name]["user_msgs"].pop()

        if (
            "bot_msgs" in self.session_dict[self.bot_name]
            and self.session_dict[self.bot_name]["bot_msgs"]
        ):
            # Remove the last bot message from the session dictionary
            self.session_dict[self.bot_name]["bot_msgs"].pop()
            # Update context if 'user_msgs' or/and 'bot_msgs' exist in session dictionary, else skip update
            self.update_context()

        # Restore display history always as it might be affected by above operations too
        self.chat_display()

    def retry_launcher(self):
        if self.textTabWidget.currentIndex() == 0:
            self.retry_textgen_chat()
        else:
            self.retry_textgen_notebook()

    def retry_textgen_chat(self):
        last_user_msg = self.session_dict[self.bot_name]["user_msgs"][-1]
        self.rewind_history()
        self.launch_page_mode(last_user_msg)

    def retry_textgen_notebook(self):
        self.notebookTextEdit.clear()
        self.notebookTextEdit.setPlainText(self.prev_notebook_text)
        self.launch_backend()

    def continue_launcher(self):
        if self.textTabWidget.currentIndex() == 0:
            self.continue_chat = True
        self.launch_backend()

    # Stop button logic
    def stop_textgen(self):
        self.text_gen_thread.stop()

    def launch_backend(self):
        # Add user message to session dictionary only if not empty
        self.button_manager(True, False)
        self.update_generation_status(True, None)
        cpp_params = self.get_llama_cpp_params()
        backend = "exllamav2" if self.backendExllamaCheck.isChecked() else "llama.cpp"
        # Start text generation thread and connect signals to slots
        self.text_gen_thread = text_gen_thread(cpp_params, backend)
        self.text_gen_thread.resultReady.connect(self.handle_result)
        self.text_gen_thread.final_resultReady.connect(self.handle_final_result)
        self.text_gen_thread.finished.connect(self.text_gen_thread.deleteLater)

        # Start the thread
        self.text_gen_thread.start()

    def add_chat_messages(self, mode, message):
        self.session_dict[self.bot_name][mode].append(message)

    def get_image(self):
        if self.imgFileLine.text() and Path(self.imgFileLine.text()).exists():
            # Open the image file in binary mode
            with open(self.imgFileLine.text().strip(), "rb") as image_file:
                # Read the image file
                data = image_file.read()
            # Encode the image data to base64
            encoded_image_data = base64.b64encode(data)
            # Decode the bytes to a string
            encoded_string = encoded_image_data.decode("utf-8")
            image_data = [{"data": encoded_string, "id": 7}]

        return image_data

    def get_llama_cpp_params(self):
        prompt = (
            self.session_dict[self.bot_name]["context"]
            if self.page_mode == "Chat"
            else self.notebookTextEdit.toPlainText()
        )

        image_data = (
            self.get_image()
            if self.imgFileLine.text() and Path(self.imgFileLine.text()).exists()
            else None
        )
        stop_strings = (
            [
                self.final_prompt_template["user_name_prefix"],
                f"\n{self.final_prompt_template['user_name_prefix'][:-1]}",
                self.final_prompt_template["bot_name_prefix"],
                "\n:",
                "### Instruction:",
            ]
            if self.stopStringAutoCheck.isChecked() and self.page_mode == "Chat"
            else []
        )
        stop_strings += (
            self.custStopStringLine.text().split(", ")
            if self.custStopStringLine.text()
            else []
        )

        seed = (
            random.randint(1, 4294967295)
            if self.seedSpin.value() == -1
            else self.seedSpin.value()
        )

        # print("---" + prompt + "---")

        cpp_params = {
            "prompt": prompt,
            "stop": stop_strings,
            "repeat_penalty": float(self.repetition_penaltySpin.value()),
            "top_k": int(self.top_kSpin.value()),
            "tfs_z": float(self.tfszSpin.value()),
            "typical_p": float(self.typical_pSpin.value()),
            "top_p": float(self.top_pSpin.value()),
            "temperature": float(self.temperatureSpin.value()),
            "n_predict": int(self.max_new_tokensSpin.value()),
            "min_p": float(self.minpSpin.value()),
            "repeat_last_n": int(self.repeatLastSpin.value()),
            "penalize_nl": self.penaliseNlCheck.isChecked(),
            "n_keep": self.keepLastNSpin.value(),
            "mirostat_mode": int(self.mirostatMode.value()),
            "mirostat_tau": int(self.mirostatTau.value()),
            "mirostat_eta": float(self.mirostatEta.value()),
            "frequency_penalty": float(self.freqPenaltySpin.value()),
            "presence_penalty": float(self.presencePenaltySpin.value()),
            "stream": bool(self.streamCheck.isChecked()),
            "cache_prompt": bool(self.cacheCheck.isChecked()),
            "image_data": image_data,
            "seed": seed,
        }

        self.stream = cpp_params["stream"]
        return cpp_params

    def scroll_to_bottom(self):
        widget = (
            self.chatTextEdit if self.page_mode == "Chat" else self.notebookTextEdit
        )
        if self.autoscrollCheck.isChecked():
            widget.verticalScrollBar().setValue(widget.verticalScrollBar().maximum())

    def display_text_nonstream(self, final_text):
        self.chatTextEdit.append(self.prev_notebook_text + final_text)

    def handle_result(self, text):
        cursor = (
            self.chatTextEdit.textCursor()
            if self.page_mode == "Chat"
            else self.notebookTextEdit.textCursor()
        )
        cursor.movePosition(QTextCursor.End)
        text = text.replace(" ", "&nbsp;").replace("\n", "<br />")
        cursor.insertMarkdown(text)
        self.scroll_to_bottom()

    def handle_final_result(self, success, final_result):
        if not success:
            self.status_bar_msg("Error: Generation failed...")
        else:
            self.update_generation_status(False, final_result[1])
            final_text = final_result[0]
            if self.page_mode == "Chat":
                self._handle_result_chat(final_text)
            elif not self.stream and not self.session_dict[self.bot_name]["user_msgs"]:
                self.display_text_nonstream(final_text)
            # print("---" + self.session_dict[self.bot_name]["context"] + "---")

        self.button_manager(False, False)
        self.text_gen_thread = None
        QApplication.alert(self.centralwidget)

    def _handle_result_chat(self, final_text):
        if self.continue_chat:
            self.session_dict[self.bot_name]["bot_msgs"][-1] += final_text
            self.continue_chat = False
        else:
            self.add_chat_messages("bot_msgs", final_text)

        self.update_context()
        self.chat_display()
        self.write_history_file(SESSION_FILE)

    # Set themes
    def set_themes(self, theme):
        extra = {"pyside6": True, "density_scale": "-1", "font_family": ""}

        if theme == "dark":
            apply_stylesheet(
                app,
                theme="dark_blue.xml",
                css_file="assets/dark_theme.css",
                extra=extra,
            )
        if theme == "light":
            apply_stylesheet(
                app,
                theme="light_blue.xml",
                css_file="assets/light_theme.css",
                extra=extra,
                invert_secondary=True,
            )
        if theme == "native":
            app.setStyleSheet("")
        print("--- Set theme to:", theme)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if platform.system() == "Windows":
        app.setStyle("Fusion")

    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
