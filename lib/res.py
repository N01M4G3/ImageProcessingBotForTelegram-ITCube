# Класс для обработки сообщения
class Result:
    def __init__(self, result_data):
        self.SUCCESS = result_data['ok']
        self.RESULT = result_data['result'][0]

    def success(self):
        return self.SUCCESS

    def result(self):
        return self.RESULT

    def update_id(self):
        if 'update_id' in self.RESULT:
            return self.RESULT['update_id']
        return -1

    def message(self):
        if 'message' in self.RESULT:
            return self.RESULT['message']
        return -1

    def chat_id(self):
        if 'message' in self.RESULT:
            if 'from' in self.RESULT['message']:
                if 'id' in self.RESULT['message']['from']:
                    return self.RESULT['message']['from']['id']
        return -1

    def text(self):
        if 'message' in self.RESULT:
            if 'text' in self.RESULT['message']:
                return self.RESULT['message']['text']
            elif 'caption' in self.RESULT['message']:
                return self.RESULT['message']['caption']
        return -1

    def bot(self):
        if 'message' in self.RESULT:
            if 'from' in self.RESULT['message']:
                if 'is_bot' in self.RESULT['message']['from']:
                    return self.RESULT['message']['from']['is_bot']
        return -1

    def name(self):
        if 'message' in self.RESULT:
            if 'from' in self.RESULT['message']:
                if 'first_name' in self.RESULT['message']['from']:
                    return self.RESULT['message']['from']['first_name']
        return -1

    def username(self):
        if 'message' in self.RESULT:
            if 'from' in self.RESULT['message']:
                if 'username' in self.RESULT['message']['from']:
                    return self.RESULT['message']['from']['username']
        return -1

    def command(self, prefix):
        if str(self.text()).startswith(prefix):
            return True
        return False
