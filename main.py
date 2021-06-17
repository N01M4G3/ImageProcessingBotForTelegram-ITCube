from lib import api, res, msg, file, pic
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os

TOKEN = "TOKEN_HERE"                                            # Токен бота
LINK = "BOT_LINK_HERE"                                          # Ссылка на бота
CREATOR_ID = 834765903                                          # ID создателя
IN_FILE = "i_file"                                              # Название всех сохраняемых файлов
OUT_FILE = "o_file"                                             # Название всех отправляемых файлов
PREFIX = '$'                                                    # Префикс начала любой команды

COMMANDS = [
    'img::conv::',                  # Для конвертирования
    'img::form::',                  # Для изменения/формирования изображения
    'rot',                          # Повернуть
    'crot',                         # Повернуть и обрезать
    'hdust',                        # "Распылить" по горизонтали
    'vdust',                        # "Распылить" по вертикали
    'bound',                        # Сильно выделить границы
    'blur',                         # Размыть изображение
    'colors',                       # Изменить количество цветов в изображении
    'curve',                        # Выделить тёмные участки
    'negative',                     # Инвертировать цвета изображения
    'cch',                          # Поменять местами красный и зелёный цвета
    'bag',                          # Сделать изображение чёрно-белым
    'glitch',                       # Применить эффект глитча к изображению
    'pixelize',                     # Сделать из изображения мозаику и раздвоить её
    'quote'                         # Цитировать картинку
]

api_obj = api.Api(TOKEN, LINK, CREATOR_ID)                      # Объект класса Api
msg_obj = msg.Message(api_obj)                                  # Объект класса Message
file_obj = file.File(api_obj)                                   # Объект класса File
update_obj = ''

while 1:
    upt = api_obj.call("getUpdates", params={"offset": -1})     # Получаем последний Update
    if upt != update_obj and upt and len(upt['result']) > 0:    # Сверяем с предыдущим, чтобы не было спама
        update_obj = upt
        modified = False

        res_obj = res.Result(upt)                               # Объект класса Result

        if res_obj.command(PREFIX):                             # Проверка, что это команда
            cmd = str(res_obj.text()[1:])                       # Обработка данных
            while cmd[0] == ' ':                                # Удаление пробела в начале
                cmd = cmd[1:]
            while '  ' in cmd:                                  # Удаление лишних пробелов
                cmd = cmd.replace('  ', ' ')
            while cmd[len(cmd) - 1] == ' ':                     # Удаление пробела в конце
                cmd = cmd[len(cmd) - 2]

            if cmd.startswith(COMMANDS[0]):
                i_format = cmd[cmd.rfind(':') + 1:cmd.rfind('2')]
                o_format = cmd[cmd.rfind('2') + 1:]
                msg_obj.send(res_obj.chat_id(), "Подождите, выполняется конвертирование фото...")
                if 'photo' in res_obj.message():
                    file_obj.save(
                        f"{IN_FILE}.{i_format}",
                        res_obj.message()['photo'][len(res_obj.message()['photo']) - 1]['file_id']
                    )
                    try:
                        Image.open(f"{IN_FILE}.{i_format}").save(f"{OUT_FILE}.{o_format}")
                    except ValueError:
                        msg_obj.send(res_obj.chat_id(), "Невозможно конвертировать фото: неизвестный формат!")
                        os.remove(f"{IN_FILE}.{i_format}")
                        continue
                    msg_obj.send(res_obj.chat_id(), "Фото конвертировано! Выполняется загрузка, ожидайте...")
                    file_obj.send_document(res_obj.chat_id(), f"{OUT_FILE}.{o_format}")
                    os.remove(f"{IN_FILE}.{i_format}")
                    os.remove(f"{OUT_FILE}.{o_format}")
                else:
                    msg_obj.send(res_obj.chat_id(), "Вы не отправили фото!")
            elif cmd.startswith(COMMANDS[1]):
                cmd_method = cmd[11:]
                msg_obj.send(res_obj.chat_id(), "Подождите, выполняется преобразование фото...")
                if 'photo' in res_obj.message():
                    file_obj.save(
                        f"{IN_FILE}.png",
                        res_obj.message()['photo'][len(res_obj.message()['photo']) - 1]['file_id']
                    )
                    if cmd_method.startswith(COMMANDS[2]):
                        try:
                            Image.open(f"{IN_FILE}.png").rotate(int(cmd_method[4:]), expand=1).save(f"{OUT_FILE}.png")
                            modified = True
                        except ValueError:
                            msg_obj.send(res_obj.chat_id(), "Неверный аргумент!")
                    elif cmd_method.startswith(COMMANDS[3]):
                        Image.open(f"{IN_FILE}.png").rotate(int(cmd_method[4:]), expand=0).save(f"{OUT_FILE}.png")
                        modified = True

                    elif cmd_method.startswith(COMMANDS[4]):
                        img = Image.open(f"{IN_FILE}.png")
                        pixels = img.load()
                        try:
                            pic.Picture.horizontal_dust(pixels, img.size, int(cmd_method[6:]))
                            img.save(f"{OUT_FILE}.png")
                            modified = True
                        except ValueError:
                            msg_obj.send(res_obj.chat_id(), "Неверный аргумент!")

                    elif cmd_method.startswith(COMMANDS[5]):
                        img = Image.open(f"{IN_FILE}.png")
                        pixels = img.load()
                        try:
                            pic.Picture.vertical_dust(pixels, img.size, int(cmd_method[6:]))
                            img.save(f"{OUT_FILE}.png")
                            modified = True
                        except ValueError:
                            msg_obj.send(res_obj.chat_id(), "Неверный аргумент!")

                    elif cmd_method.startswith(COMMANDS[6]):
                        img = Image.open(f"{IN_FILE}.png")
                        pixels = img.load()
                        try:
                            pic.Picture.bound(pixels, img.size)
                            img.save(f"{OUT_FILE}.png")
                            modified = True
                        except ValueError:
                            msg_obj.send(res_obj.chat_id(), "Неверный аргумент!")

                    elif cmd_method.startswith(COMMANDS[7]):
                        try:
                            factor = int(cmd_method[5:])
                            Image.open(f"{IN_FILE}.png").filter(ImageFilter.GaussianBlur(factor)).save(f"{OUT_FILE}.png")
                            modified = True
                        except ValueError:
                            msg_obj.send(res_obj.chat_id(), "Неверный аргумент!")
                    elif cmd_method.startswith(COMMANDS[8]):
                        try:
                            factor = int(cmd_method[7:])
                            if factor > 256:
                                factor = 256
                            Image.open(f"{IN_FILE}.png").quantize(factor).save(f"{OUT_FILE}.png")
                            modified = True
                        except ValueError:
                            msg_obj.send(res_obj.chat_id(), "Неверный аргумент!")

                    elif cmd_method.startswith(COMMANDS[9]):
                        img = Image.open(f"{IN_FILE}.png")
                        pixels = img.load()
                        pic.Picture.curve(pixels, img.size)
                        img.save(f"{OUT_FILE}.png")
                        modified = True

                    elif cmd_method.startswith(COMMANDS[10]):
                        img = Image.open(f"{IN_FILE}.png")
                        pixels = img.load()
                        pic.Picture.negative(pixels, img.size)
                        img.save(f"{OUT_FILE}.png")
                        modified = True

                    elif cmd_method.startswith(COMMANDS[11]):
                        img = Image.open(f"{IN_FILE}.png")
                        pixels = img.load()
                        pic.Picture.change_colors(pixels, img.size)
                        img.save(f"{OUT_FILE}.png")
                        modified = True

                    elif cmd_method.startswith(COMMANDS[12]):
                        img = Image.open(f"{IN_FILE}.png")
                        pixels = img.load()
                        pic.Picture.black_and_gray(pixels, img.size)
                        img.save(f"{OUT_FILE}.png")
                        modified = True

                    elif cmd_method.startswith(COMMANDS[13]):
                        img = Image.open(f"{IN_FILE}.png")
                        pixels = img.load()
                        pic.Picture.glitch(pixels, img.size)
                        img.save(f"{OUT_FILE}.png")
                        modified = True

                    elif cmd_method.startswith(COMMANDS[14]):
                        img = Image.open(f"{IN_FILE}.png")
                        pixels = img.load()
                        try:
                            pic.Picture.pixelize(pixels, img.size, int(cmd_method[9:]))
                            img.save(f"{OUT_FILE}.png")
                            modified = True
                        except ValueError:
                            msg_obj.send(res_obj.chat_id(), "Неверный аргумент!")

                    elif cmd_method.startswith(COMMANDS[15]):
                        sz_font = 0
                        try:
                            sz_font = int(cmd_method[cmd_method.rfind(' ') + 1:])
                        except ValueError:
                            sz_font = 20
                        text = cmd_method[cmd_method.find(' ') + 1:cmd_method.rfind(str(sz_font)) - 1]
                        img_paste = Image.open(f"{IN_FILE}.png")
                        img_paste = img_paste.resize((349, 349), Image.ANTIALIAS)
                        img = Image.new("RGB", (500, 500), 0x000000)
                        draw = ImageDraw.Draw(img)
                        draw.rectangle([75, 75, 425, 425], 0x000000, 0xffffff)
                        img.paste(img_paste, (76, 76))
                        font = ImageFont.truetype('arial.ttf', sz_font)
                        i = 0
                        for string in text.split('\n'):
                            draw.text((250 - (len(string) * sz_font / 4), 430 + (sz_font * i)),
                                      text=string, font=font, align="left")
                            i += 1
                        img.save(f"{OUT_FILE}.png", "PNG")
                        modified = True
                    else:
                        msg_obj.send(res_obj.chat_id(), "Неизвестное преобразование!")
                    if modified:
                        msg_obj.send(res_obj.chat_id(), "Фото создано/обработано! Ожидайте загрузки...")
                        file_obj.send_photo(res_obj.chat_id(), f"{OUT_FILE}.png")
                    os.remove(f"{OUT_FILE}.png")
                    os.remove(f"{IN_FILE}.png")
                else:
                    msg_obj.send(res_obj.chat_id(), "Вы не отправили фото!")
        # Список команд
        elif str(res_obj.text()).startswith("help") or str(res_obj.text()).startswith("info") or \
                str(res_obj.text()).startswith("?") or str(res_obj.text()).startswith(f"{PREFIX}help") or \
                str(res_obj.text()).startswith(f"{PREFIX}info") or str(res_obj.text()).startswith(f"{PREFIX}?"):
            info = f"Добрый день, {res_obj.name()}.\n" \
                   f"Перед командой ставьте {PREFIX}.\n" \
                   "На данный момент в боте присутствуют данные команды:\n" \
                   "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
                   "Для конвертирования форматов картинок:\n" \
                   "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
                   "1)img::conv::(входящий_формат)2(выходящий_формат)\n" \
                   "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
                   "Для изменения картинок:\n" \
                   "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
                   "2)img::form::rot (кол-во_градусов_для_поворота_картинки)\n" \
                   "3)img::form::crot (кол-во_градусов_для_поворота_картинки)\n" \
                   "4)img::form::hdust (через_какое_кол-во_пикселей_брать_пиксель)\n" \
                   "5)img::form::vdust (через_какое_кол-во_пикселей_брать_пиксель)\n" \
                   "6)img::form::bound\n" \
                   "7)img::form::blur (интенсивность)\n" \
                   "8)img::form::colors (кол-во_цветов_в_картинке)\n" \
                   "9)img::form::curve\n" \
                   "10)img::form::negative\n" \
                   "11)img::form::cch\n" \
                   "12)img::form::bag\n" \
                   "13)img::form::glitch\n" \
                   "14)img::form::pixelize (интенсивность)\n" \
                   "15)img::form::quote (текст) (размер текста)\n" \
                   "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
                   "Справка по командам:\n" \
                   "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
                   "1)\"входящий формат\" - формат картинки, которую вы отправляете(к примеру, png), " \
                   "\"выходящий формат\" - формат, в который вы хотите преобразовать картинку(к примеру, gif)\n" \
                   "2)\"кол-во_градусов_для_поворота_картинки\" - количество градусов для поворота картинки" \
                   "(она не обрезается)\n" \
                   "3)\"кол-во_градусов_для_поворота_картинки\" - количество градусов для поворота картинки" \
                   "(картинка обрезается)\n" \
                   "4)Выполняется смешивание пикселей по горизонтали." \
                   " \"через_какое_кол-во_пикселей_брать_пиксель\" означает," \
                   " что данный пиксель будет равен пикселю через определённый вами промежуток пикселей\n" \
                   "5)Выполняется смешивание пикселей по вертикали." \
                   " \"через_какое_кол-во_пикселей_брать_пиксель\" означает," \
                   " что данный пиксель будет равен пикселю через определённый вами промежуток пикселей\n" \
                   "6)Сильно выраженные грани выделяются и смещаются\n" \
                   "7)Выполняется размытие картинки. Сила эффекта зависит от параметра \"интенсивность\"\n" \
                   "8)Изменяется количество цветов в картинке на \"кол-во_цветов_в_картинке\"\n" \
                   "9)Затемнённые участки картинки выделяются различными цветами\n" \
                   "10)Инвертируются цвета на картинке\n" \
                   "11)Меняются местами значение красного и зелёного цветов в каждом пикселе изображения\n" \
                   "12)Картинка становится чёрно-белой\n" \
                   "13)Не требует объяснения\n" \
                   "14)некоторые пиксели очень сильно выделяются и их цвет изменяется\n" \
                   "15)Создаётся изображение, внутри которого" \
                   " рисуется приложенная картинка в белой рамке," \
                   " под котрой написан (текст) написанного (размера)\n" \
                   "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            msg_obj.send(res_obj.chat_id(), info)