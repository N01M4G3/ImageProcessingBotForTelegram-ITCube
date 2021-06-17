import requests


class Api:
    def __init__(self, token, link, creator_id=0):
        self.TOKEN = token
        self.LINK = link
        self.CREATOR_ID = creator_id
        self._class_obj = self

    # Вызов почти любой функции
    def call(self, telegram_function_name, params={}):
        link = f"https://api.telegram.org/bot{self.TOKEN}/{telegram_function_name}?"
        for param in params:
            link += f"{param}={params[param]}&"
        return requests.get(link).json()

    # Вызов любой функции, где требуется отправка чего-то(файла, картинки,...)
    def do_call(self, telegram_function_name, files={}, data={}):
        link = f"https://api.telegram.org/bot{self.TOKEN}/{telegram_function_name}"
        return requests.post(link, files=files, data=data).json()