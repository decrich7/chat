# -*- coding: utf-8 -*-

import asyncio
from RSA import Rsa
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js

chat_msgs = []
chat_msgs_enc = []
online_users = set()
rsa = Rsa('математика')
keys = rsa.generate_enc_message()
MAX_MESSAGES_COUNT = 100




async def main():
    global chat_msgs, keys, chat_msgs_enc
    img = open('джейсон.png', 'rb').read()
    put_image(img, width='350px', height='350px')
    put_markdown("# 🥳 Добро пожаловать в Зашифрованный чат 🥳\n"
                 "### В этом чате используются следуюшие ключи шифрования\n"
                 f"**Открытый ключ - {keys[0][0]}**\n"
                 f"**Закрытый ключ - {keys[0][1]}**")

    put_markdown("## 👇🏻 Здесь вы можете увидеть зашифрованные сообщения 👇🏻")

    msg_box = output()
    msg_box_enc = output()


    put_scrollable(msg_box_enc, height=200, keep_bottom=True)
    put_markdown("## А здесь Обычные сообщения")
    put_scrollable(msg_box, height=200, keep_bottom=False, border=True, scope=None, position=-1)

    nickname = await input("Войти в чат", required=True, placeholder="Ваше имя",
                           validate=lambda n: "Такой ник уже используется!" if n in online_users or n == '📢' else None)
    online_users.add(nickname)

    chat_msgs.append(('📢', f'`{nickname}` присоединился к чату!'))
    msg_box.append(put_markdown(f'📢 `{nickname}` присоединился к чату'))

    refresh_task = run_async(refresh_msg(nickname, msg_box, msg_box_enc))

    while True:
        data = await input_group("💭 Новое сообщение", [
            input(placeholder="Текст сообщения ...", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label': "Выйти из чата", 'type': 'cancel'}])
        ], validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)
        enc_data = rsa.encript(keys[-1][0], data['msg'])

        if data is None:
            break

        msg_box_enc.append(put_markdown(f"`{nickname}`: {enc_data}"))
        msg_box.append(put_markdown(f"`{nickname}`: {data['msg']}"))
        chat_msgs_enc.append((nickname, enc_data))
        chat_msgs.append((nickname, data['msg']))

    refresh_task.close()

    online_users.remove(nickname)
    toast("Вы вышли из чата!")
    msg_box.append(put_markdown(f'📢 Пользователь `{nickname}` покинул чат!'))
    chat_msgs.append(('📢', f'Пользователь `{nickname}` покинул чат!'))

    put_buttons(['Перезайти'], onclick=lambda btn: run_js('window.location.reload()'))


async def refresh_msg(nickname, msg_box, msg_box_enc):
    global chat_msgs, chat_msgs_enc
    last_idx = len(chat_msgs)
    idx = len(chat_msgs_enc)

    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:  # if not a message from current user
                msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))

        for i in chat_msgs_enc[idx:]:
            if i[0] != nickname:  # if not a message from current user
                msg_box_enc.append(put_markdown(f"`{i[0]}`: {i[1]}"))

        # remove expired
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

            # remove expired
        if len(chat_msgs_enc) > MAX_MESSAGES_COUNT:
            chat_msgs_enc = chat_msgs_enc[len(chat_msgs_enc) // 2:]

        last_idx = len(chat_msgs)
        idx = len(chat_msgs_enc)


if __name__ == "__main__":
    start_server(main, debug=True, port=80, cdn=False)