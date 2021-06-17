class Message:
    def __init__(self, api):
        self.OBJ = api

    # Для отправки сообщения
    def send(self, chat_id, text="Hello!", parse_mode="HTML", entities=[],
             disable_web_page_preview=False, disable_notification=False, reply_to_message_id=0,
             allow_sending_without_reply=True, reply_markup=0):
        link_dictionary = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
            "allow_sending_without_reply": allow_sending_without_reply,
        }

        if entities:
            link_dictionary['entities'] = entities
        elif reply_to_message_id:
            link_dictionary['reply_to_message_id'] = reply_to_message_id
        elif reply_markup:
            link_dictionary['reply_markup'] = reply_markup

        self.OBJ.call("sendMessage", link_dictionary)