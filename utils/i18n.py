import json


class Translator:
    def __init__(self, lang_code="en"):
        self.lang_code = lang_code
        self.strings = {}
        self.load_language(lang_code)

    def load_language(self, lang_code):
        try:
            with open(f"assets/lang/{lang_code}.json", encoding="utf-8") as f:
                self.strings = json.load(f)
                self.lang_code = lang_code
        except FileNotFoundError:
            print(f"Language file for '{lang_code}' not found. Falling back to empty translations.")
            self.strings = {}

    def t(self, key):
        return self.strings.get(key, f"[{key}]")

_instance = None

def init_translator(lang_code="en"):
    global _instance
    _instance = Translator(lang_code)

def t(key):
    if _instance:
        return _instance.t(key)
    return f"[{key}]"

def change_language(lang_code):
    if _instance:
        _instance.load_language(lang_code)