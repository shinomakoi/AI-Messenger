import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QFileDialog
from PySide6.QtCore import QThread, Signal, Slot, QSize
from pathlib import Path
from PySide6.QtGui import QIcon, QTextCursor
from qt_material import apply_stylesheet
import glob
import base64
import platform
import asyncio
import json
import random

from chat_window import Ui_ChatWindow

import cpp_server_gen
import exllamav2_server_gen

# Constants for the directories and file names
APP_ICON = Path("assets/icons/appicon.png")
INSTRUCT_PRESETS_DIR = Path("presets/Assistants/")
CHARACTER_PRESETS_DIR = Path("presets/Characters/")
CARDS_PRESETS_DIR = Path("presets/Cards/")
SETTINGS_FILE = Path("saved/settings.json")
SESSION_FILE = Path("saved/session.json")


class SettingsManager:
    def __init__(self):
        pass

    def save_settings(self, ui):
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
                "bos_id": ui.bosIdText.text(),
                "backend": "exllamav2"
                if ui.backendExllamaCheck.isChecked()
                else "llama.cpp",
            },
            "cpp_params": {
                "preset": ui.paramPresets_comboBox.currentText(),
                "max_new_tokens": ui.max_new_tokensSpin.value(),
                "repeat_last_n": ui.repeatLastSpin.value(),
                "n_keep": ui.keepLastNSpin.value(),
            },
        }
        try:
            with open(SETTINGS_FILE, "w") as file:
                json.dump(settings, file)
            print("--- Saved settings")
        except FileNotFoundError:
            print("Settings file not found.")

    def load_settings(self, ui):
        try:
            with open(SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                self._update_ui(ui, settings)
                print("--- Loaded settings")
        except FileNotFoundError:
            print("Settings file not found.")

    def _update_ui(self, ui, settings):
        prefs = settings["prefs"]
        ui.streamCheck.setChecked(prefs["stream"])
        ui.cacheCheck.setChecked(prefs["cache"])
        ui.usernameLine.setText(prefs["user_name"])
        ui.botnameLine.setText(prefs["bot_name"])
        ui.custStopStringLine.setText(prefs["stop_strings"])
        ui.customSysPromptCheck.setChecked(prefs["system_prompt_check"])
        ui.bosIdText.setText(prefs["bos_id"])
        ui.customSysPromptText.setPlainText(prefs["system_prompt"])
        ui.autoSaveSessionCheck.setChecked(prefs["auto_save_session"])
        ui.stopStringAutoCheck.setChecked(prefs["auto_add_stopstring"])
        backend = prefs["backend"]
        if backend == "exllamav2":
            ui.backendExllamaCheck.setChecked(True)
        else:
            ui.backendCppCheck.setChecked(True)

        basic_params = settings["cpp_params"]
        ui.paramPresets_comboBox.setCurrentText(basic_params["preset"])
        ui.max_new_tokensSpin.setValue(basic_params["max_new_tokens"])
        ui.repeatLastSpin.setValue(basic_params["repeat_last_n"])
        ui.keepLastNSpin.setValue(basic_params["n_keep"])


class CharacterCard:
    def __init__(self):
        pass

    def get_card_data(self, card_file, user_name):
        try:
            from PIL import Image

            print("--- Reading character card...")
            img = Image.open(f"{CARDS_PRESETS_DIR}/{card_file}.png")
            exif_data = img.info
            print(exif_data)
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
            f"{result['first_mes']}"
        )

        def replace_placeholders(temp):
            temp = (
                str(temp)
                .replace("{{char}}", result["name"])
                .replace("{{user}}", user_name)
                .replace("{{Char}}", result["name"])
                .replace("{{User}}", user_name)
            )
            return temp

        template["display_text"] = replace_placeholders(result["first_mes"])
        template["system_message"] = replace_placeholders(template["system_message"])

        template["user_name_prefix"] = f"{user_name}:"
        template["bot_name_prefix"] = f"{result['name']}:"

        return template


class TextGenThread(QThread):
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
        for response in cpp_server_gen.generate_with_streaming(self.params):
            if self.stop_flag:
                break
            # Append the response to the final text and emit the result ready signal
            final_text += response["content"]
            self.resultReady.emit(response["content"])
        self._emit_final_result(final_text, response=None)

    def _generate_nostream(self):
        # Get generated text without streaming
        response = cpp_server_gen.generate_nostream(self.params)
        self._emit_final_result(response["content"], response=None)

    def _exllamav2_generate(self):
        if self.stream_enabled:
            self._exllamav2_streaming()
        else:
            self._exllamav2_generate_nostream()

    def _exllamav2_streaming(self):
        async def get_response():
            final_text = ""
            async for response in exllamav2_server_gen.generate_streaming(self.params):
                if self.stop_flag:
                    break
                final_text += response
                self.resultReady.emit(response)
            return final_text, response

        final_text, response = asyncio.run(get_response())
        self._emit_final_result(final_text, response=None)

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
        self.add_contacts(0, INSTRUCT_PRESETS_DIR)
        self.add_contacts(1, CHARACTER_PRESETS_DIR)
        self.add_contacts(2, CARDS_PRESETS_DIR)
        self.load_params_presets()
        self.settings_manager.load_settings(self)
        self.apply_params_preset()
        self.connect_signals()
        self.contactsTree.expandAll()
        self.session_dict = {}
        self.bot_prompt = ""
        self.chat_input_history = []
        self.textgenThread = None

    def set_window_icon(self):
        icon = QIcon()
        icon.addFile(str(APP_ICON), QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.status_bar_msg("Status: Ready")

    def connect_signals(self):
        # Connect buttons to their respective functions
        self.generateButton.clicked.connect(self.launch_page_mode)
        self.actionAbout.triggered.connect(app.aboutQt)
        self.actionSave_settings.triggered.connect(
            lambda: self.settings_manager.save_settings(self)
        )
        self.clearButton.clicked.connect(self.history_clear)
        self.stopButton.clicked.connect(self.stop_textgen)
        self.rewindButton.clicked.connect(self.rewind_history)
        self.retryButton.clicked.connect(self.retry_launcher)
        self.continueButton.clicked.connect(self.continue_launcher)

        self.themeDarkRadio.clicked.connect(lambda: self.set_themes("dark"))
        self.themeLightRadio.clicked.connect(lambda: self.set_themes("light"))
        self.themeNativeRadio.clicked.connect(lambda: self.set_themes("native"))

        self.actionExit.triggered.connect(self.close)
        self.actionSave_session.triggered.connect(self.save_session)

        # Connect comboboxes to their respective functions
        self.inputHistoryCombo.activated.connect(self.set_chat_input_history)
        self.paramPresets_comboBox.activated.connect(self.apply_params_preset)
        self.contactsTree.itemDoubleClicked.connect(self.manage_page_mode)
        self.leftToolbox.currentChanged.connect(self.manage_page_mode)

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

    def add_contacts(self, chat_mode_index, directory):
        file_extension = "json" if chat_mode_index < 2 else "png"
        presets = glob.glob(f"{directory}/*.{file_extension}")
        presets.sort()  # sort the list of files alphabetically

        for preset in presets:
            preset_stem = Path(preset).stem
            item = QTreeWidgetItem([preset_stem])
            self.contactsTree.topLevelItem(chat_mode_index).addChild(item)

    def load_params_presets(self):
        param_preset_load = glob.glob("presets/model_params/*.settings")
        param_preset_load.sort()

        for param_preset in param_preset_load:
            param_preset_stem = Path(param_preset).stem
            self.paramPresets_comboBox.addItem(param_preset_stem)

        self.paramPresets_comboBox.setCurrentText("Default")

    def apply_params_preset(self):
        current_preset = self.paramPresets_comboBox.currentText()
        preset_file = f"presets/model_params/{current_preset}.settings"

        with open(preset_file, "r") as file:
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

    # Set themes
    def set_themes(self, theme):
        extra = {"pyside6": True, "density_scale": "-1", "font_family": ""}

        if theme == "dark":
            apply_stylesheet(
                app,
                theme="dark_amber.xml",
                css_file="assets/dark_theme.css",
                extra=extra,
            )
        if theme == "light":
            apply_stylesheet(
                app,
                theme="light_amber.xml",
                css_file="assets/light_theme.css",
                extra=extra,
                invert_secondary=True,
            )
        if theme == "native":
            if platform.system() == "Windows":
                app.setStyle("Fusion")
            app.setStyleSheet("")
        print("--- Set theme to:", theme)

    def manage_page_mode(self, contact=None):
        # Get current index from leftToolbox
        toolbox_index = self.leftToolbox.currentIndex()

        # Check the value of toolbox and update page mode accordingly
        if toolbox_index == 0:
            self.continue_chat = False
            self.page_mode = "Chat"

            # If a contact is provided, get related info and set window title
            if contact:
                self.final_prompt_template = {}
                self.bot_name = contact.text(0)
                self.contact_parent = contact.parent().text(0)
                self.history_display(not bool(self.session_dict.get(contact.text(0))))

                if contact.parent().text(0) == "Cards":
                    self.get_template()
                    if not self.session_dict[self.bot_name]["context"]:
                        self.outputText.setMarkdown(
                            self.final_prompt_template["display_text"]
                        )
                self.setWindowTitle(f"AI Messsenger - {self.bot_name}")

        elif toolbox_index == 1:
            self.page_mode = "Simple"
            self.outputText.clear()  # temp

        else:  # index is either 2 or something different, so we're in Notebook mode here
            self.page_mode = "Notebook"
            self.outputText.clear()  # temp

        # Update whether text output and input are enabled based on notebook value
        self.outputText.setReadOnly(toolbox_index != 2)
        self.inputText.setEnabled(toolbox_index != 2)

        if not (self.generateButton.isEnabled() and bool(self.textgenThread)):
            self.generateButton.setEnabled(True)  # Enable generate button as needed

    def launch_page_mode(self, btn=None, retry_textgen=False):
        if self.textgenThread:
            return

        currentIndex = (
            self.leftToolbox.currentIndex()
        )  # Store the index in a variable for readability

        if currentIndex == 0:
            user_input = retry_textgen or self.inputText.toPlainText().strip()
            self._handle_mode(user_input)

        elif currentIndex == 1:
            self._set_bot_name("Simple")

        elif currentIndex == 2:
            self._set_bot_name("Notebook")

    def _handle_mode(self, user_input):
        if self.inputText.toPlainText() and self.page_mode == "Chat":
            self.add_chat_input_history(self.inputText.toPlainText())
        self.add_chat_messages("user_msgs", user_input)
        self.add_chat_messages("bot_msgs", "")  # Placeholder
        self.update_context()
        self.restore_display_history()
        self.inputText.clear()
        self.launch_backend()
        self.session_dict[self.bot_name]["bot_msgs"].pop()

    def _set_bot_name(self, bot_name):
        user_input = (
            (self.outputText if bot_name == "Notebook" else self.inputText)
            .toPlainText()
            .strip()
        )
        self.bot_name = bot_name
        self.user_name_prefix = None
        self.session_dict[bot_name] = {"context": user_input}
        self.outputText.clear() if bot_name == "Simple" else self.outputText.setMarkdown(
            user_input
        )  # Clear outputText for Simple mode, display text otherwise
        self.inputText.clear()
        self.launch_backend()

    # Define a helper function to get the directory path from a dialog
    def save_session(self, title):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            None, "Save File", "", "YAML Files (*.json)", options=options
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
        self.chat_input_history.append(chat_input)
        chat_input = chat_input.replace("\n", "")[:128]
        self.inputHistoryCombo.addItem(str(chat_input))

    def status_bar_msg(self, msg):
        self.statusbar.showMessage(msg)

    def update_generation_status(self, generation_enabled, results):
        info_message = ""

        if results and not generation_enabled:
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
                print(f"No data for: {str(e)}")

        status = "Generating..." if generation_enabled else f"Completed{info_message}"
        self.status_bar_msg("Status: " + status)

    def button_manager(self, enable_mode):
        inverted_button_state = not enable_mode

        buttons = [
            self.continueButton,
            self.clearButton,
            self.rewindButton,
            self.retryButton,
            self.generateButton,
        ]

        for button in buttons:
            button.setEnabled(
                inverted_button_state
            )  # Enable/disable all the buttons based on mode

        self.stopButton.setEnabled(enable_mode)  # Use _ to indicate private method

    def history_reset(self):
        self.session_dict[self.bot_name] = {
            "user_msgs": [],
            "bot_msgs": [],
            "context": "",
        }
        self.outputText.clear()

    def history_clear(self):
        self.history_reset()
        if self.page_mode == "Chat":
            self.write_history_file(SESSION_FILE)

    def history_display(self, first_launch):
        if first_launch:
            self.load_history_file()
            if self.bot_name not in self.session_dict:
                self.history_reset()
            self.restore_display_history()
        else:
            self.restore_display_history()

    def write_history_file(self, file_name, manual=False):
        if self.autoSaveSessionCheck.isChecked() or manual:
            # Write to .json
            session_history = dict(self.session_dict)
            with open(file_name, "w") as file:
                json.dump(session_history, file)

    def load_history_file(self):
        if Path(SESSION_FILE).exists():
            with open(SESSION_FILE, "r") as file:
                session_history = json.load(file)
                if self.bot_name in session_history:
                    self.session_dict = session_history
                    self.button_manager(False)

    def reset_history(self):
        self.session_dict[self.bot_name] = {
            "user_msgs": [],
            "bot_msgs": [],
            "context": "",
        }
        if self.outputText.toPlainText():
            self.outputText.clear()
            self.generateButton.setEnabled(True)

    def restore_display_history(self):
        display_text = ""
        # Iterate over user and bot messages and append them to the display text
        for user_msg, bot_msg in zip(
            self.session_dict[self.bot_name]["user_msgs"],
            self.session_dict[self.bot_name]["bot_msgs"],
        ):
            display_text += f"""**<span style="color:#a92828">{self.usernameLine.text()}</span>**

{user_msg}

**<span style="color:#3194d0">{self.botnameLine.text()}</span>**

{bot_msg}

"""
        # Clear the output text field and append the display text
        self.outputText.clear()
        display_text = (
            display_text.replace("</s>", "").replace("<START>", "").replace("<END>", "")
        )
        self.outputText.setMarkdown(display_text)
        if self.bot_prompt == "\n":
            self.outputText.append("")
        self.scroll_to_bottom()

    def get_chat_presets(self, contact_mode):
        final_template = {}

        with open(f"{contact_mode}/{self.bot_name}.json", "r") as file:
            print("--- Getting chat preset...")
            chat_preset = json.load(file)
        character_template = "<|user|> <|user-message|>\n<|bot|> <|bot-message|>\n"

        if contact_mode == "presets/Characters":
            chat_preset["example_dialogue"] = chat_preset["example_dialogue"]

            chat_preset["system_message"] = (
                chat_preset["context"] + "\n" + chat_preset["example_dialogue"]
            )
            chat_preset["context"] = "<|system-message|>\n\n"

        final_template["sys_template"] = chat_preset["context"]
        final_template["turn_template"] = (
            chat_preset["turn_template"]
            if self.contact_parent == "Assistants"
            else character_template
        )
        final_template["user_name_prefix"] = (
            chat_preset["user"]
            if self.contact_parent == "Assistants"
            else self.usernameLine.text() + ":"
        )
        final_template["bot_name_prefix"] = (
            chat_preset["bot"]
            if self.contact_parent == "Assistants"
            else chat_preset["name"] + ":"
        )

        final_template["system_message"] = chat_preset["system_message"]

        return final_template

    def get_template(self):
        contact_mode = {
            "Assistants": "presets/Assistants",
            "Characters": "presets/Characters",
            "Cards": "presets/Cards",
        }[self.contact_parent]

        if contact_mode != "presets/Cards":
            self.final_prompt_template = self.get_chat_presets(contact_mode)
        else:
            self.final_prompt_template = CharacterCard().get_card_data(
                self.bot_name, self.usernameLine.text()
            )

    def update_context_char(self):
        self.final_prompt_template["user_name_prefix"] = self.usernameLine.text() + ":"
        self.final_prompt_template["sys_template"] = (
            self.final_prompt_template["sys_template"]
            .replace("{{char}}", self.final_prompt_template["bot_name_prefix"])
            .replace("{{user}}", self.usernameLine.text() + ":")
        )

    def update_context(self):
        if not self.final_prompt_template:
            self.get_template()
        self.final_prompt_template["sys_template"] = self.final_prompt_template[
            "sys_template"
        ].replace("<|system-message|>", self.final_prompt_template["system_message"])
        self.user_name_prefix = self.final_prompt_template["user_name_prefix"].strip()
        self.final_prompt_template["system_message"] = (
            self.customSysPromptText.toPlainText()
            if self.customSysPromptCheck.isChecked()
            else self.final_prompt_template["system_message"]
        )
        user_template, bot_prompt = self.final_prompt_template["turn_template"].split(
            "<|bot-message|>"
        )
        user_prompt = user_template.replace(
            "<|user|>", self.final_prompt_template["user_name_prefix"]
        ).replace("<|bot|>", self.final_prompt_template["bot_name_prefix"])
        self.bot_prompt = bot_prompt
        updated_context = "".join(
            [
                (user_prompt.replace("<|user-message|>", user_msg))
                + (str(bot_msg) + bot_prompt)
                for user_msg, bot_msg in zip(
                    self.session_dict[self.bot_name]["user_msgs"],
                    self.session_dict[self.bot_name]["bot_msgs"],
                )
            ]
        )

        self.session_dict[self.bot_name]["context"] = (
            self.final_prompt_template["sys_template"] + updated_context
        ).strip()

        if self.contact_parent == "Characters":
            self.update_context_char()

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
        self.restore_display_history()

    def retry_launcher(self):
        if self.leftToolbox.currentIndex() == 0:
            self.retry_textgen_chat()
        else:
            self.retry_textgen_nonchat()

    def retry_textgen_chat(self):
        last_user_msg = self.session_dict[self.bot_name]["user_msgs"][-1]
        self.rewind_history()
        self.launch_page_mode(None, last_user_msg)

    def retry_textgen_nonchat(self):
        self.outputText.setMarkdown(self.session_dict[self.bot_name]["context"])
        self.launch_backend()

    def continue_launcher(self):
        if self.leftToolbox.currentIndex() == 0:
            self.continue_chat = True
            self.launch_backend()
        else:
            self.session_dict[self.bot_name]["context"] = self.outputText.toPlainText()
            self.launch_backend()

    # Stop button logic
    def stop_textgen(self):
        self.textgenThread.stop()

    def launch_backend(self):
        # Add user message to session dictionary only if not empty
        self.button_manager(True)
        self.update_generation_status(True, None)
        cpp_params = self.get_llama_cpp_params()
        backend = "exllamav2" if self.backendExllamaCheck.isChecked() else "llama.cpp"
        # Start text generation thread and connect signals to slots
        self.textgenThread = TextGenThread(cpp_params, backend)
        self.textgenThread.resultReady.connect(self.handle_result)
        self.textgenThread.final_resultReady.connect(self.handle_final_result)
        self.textgenThread.finished.connect(self.textgenThread.deleteLater)

        # Start the thread
        self.textgenThread.start()

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
        image_data = (
            self.get_image()
            if self.imgFileLine.text() and Path(self.imgFileLine.text()).exists()
            else None
        )
        stop_strings = (
            [
                self.user_name_prefix,
                f"\n{self.user_name_prefix[:-1]}",
                "\n:",
                "<START>",
                "<END>",
            ]
            if self.stopStringAutoCheck.isChecked() and self.page_mode == "Chat"
            else []
        )
        stop_strings += (
            self.custStopStringLine.text().split(", ")
            if self.custStopStringLine.text()
            else []
        )
        prompt = (
            [2, self.session_dict[self.bot_name]["context"]]
            if self.bosIdText.text() and self.backendCppCheck.isChecked()
            else self.session_dict[self.bot_name]["context"]
        )

        seed = (
            random.randint(1, 4294967295)
            if self.seedSpin.value() == -1
            else self.seedSpin.value()
        )

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
        if self.autoscrollCheck.isChecked():
            self.outputText.verticalScrollBar().setValue(
                self.outputText.verticalScrollBar().maximum()
            )

    def display_text_nonstream(self, final_text):
        if self.page_mode == "Notebook":
            self.outputText.setMarkdown(
                self.session_dict[self.bot_name]["context"] + final_text
            )
        else:
            self.outputText.setMarkdown(final_text)

    @Slot(str)
    def handle_result(self, text):
        cursor = self.outputText.textCursor()
        cursor.movePosition(QTextCursor.End)  # Move it to the end
        text = text.replace(" ", "&nbsp;").replace("\n", "<br />")
        cursor.insertMarkdown(text)
        self.scroll_to_bottom()

    def handle_final_result(self, success, final_result):
        if not success:
            # If only FALSE is returned from failure
            self.status_bar_msg("Error: Generation failed...")
            print('fail')
        else:
            self.update_generation_status(False, final_result[1])
            final_text = final_result[0]

            if self.page_mode == "Chat":
                self._handle_result_chat(final_text)
            elif (
                not self.stream and not self.session_dict[self.bot_name]["user_msgs"]
            ):  # If not chat and stream disabled
                self.display_text_nonstream(final_text)
            # print("---" + self.session_dict[self.bot_name]["context"] + "---")

        self.button_manager(False)
        self.textgenThread = None
        app.alert(self.centralwidget)

    def _handle_result_chat(self, final_text):
        if self.continue_chat:
            self.session_dict[self.bot_name]["bot_msgs"][-1] += final_text
            self.continue_chat = False
        else:
            self.add_chat_messages("bot_msgs", final_text)

        self.update_context()
        self.restore_display_history()
        self.write_history_file(SESSION_FILE)

    def _update_generation_status(self, status, result):
        self.update_generation_status(status, result)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    extra = {"pyside6": True, "density_scale": "-1", "font_family": ""}
    apply_stylesheet(
        app,
        theme="dark_amber.xml",
        css_file="assets/dark_theme.css",
        extra=extra,
    )

    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
