from typing import Optional

from json import load


class UserLanguage:
    def __init__(self, parent: "LanguageManager", lang: str):
        self.parent = parent
        self.lang = lang

    def get(self, key: str) -> Optional[str]:
        return self.parent.data[self.lang].get(key)


class LanguageManager:
    def __init__(self, lang_file: str, users: dict = None):
        self.default_language = "en"
        self.users = users or {}

        with open(lang_file, "r", encoding="utf-8") as fil:
            self.data: dict = load(fil)

    def getUser(self, id: int) -> UserLanguage:
        if not self.users.get(id):
            self.users[id] = UserLanguage(self, self.default_language)
        return self.users[id]

    def setUser(self, id: int, lang: str = None) -> UserLanguage:
        self.users[id] = UserLanguage(self, lang or self.default_language)
        return self.users[id]

    def get(self, key: str, id: int = None) -> Optional[str]:
        if id is None:
            return self.data.get(key)
        else:
            return self.getUser(id).get(key)
