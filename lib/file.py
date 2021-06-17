import requests


class File:
    def __init__(self, api):
        self.OBJ = api

    # Для сохранения файла с серверов телеграмма
    def save(self, path, file_id):
        telegram_file_path = self.OBJ.call("getFile", params={"file_id": file_id})['result']['file_path']
        img = requests.get(f"https://api.telegram.org/file/bot{self.OBJ.TOKEN}/{telegram_file_path}")
        out = open(path, "wb")
        out.write(img.content)
        out.close()

    # Для отправки файла в диалог с пользователем
    def send_document(self, chat_id, path_string):
        url = f"https://api.telegram.org/bot{self.OBJ.TOKEN}/sendDocument"
        files = {'document': open(path_string, 'rb')}
        data = {'chat_id': chat_id}
        return requests.post(url, files=files, data=data).json()

    # Для отправки фотографии в диалог с пользователем
    def send_photo(self, chat_id, path_string):
        url = f"https://api.telegram.org/bot{self.OBJ.TOKEN}/sendPhoto"
        files = {'photo': open(path_string, 'rb')}
        data = {'chat_id': chat_id}
        return requests.post(url, files=files, data=data).json()