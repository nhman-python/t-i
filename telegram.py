from pyrogram.client import Client
from rich.prompt import IntPrompt
import random
import time
api_hash = ''
api_id = ''
phone_number = '+972xxxx'


def random_message():
    with open('fack_arab.txt', 'r') as file:
        all_lines = file.readlines()
        return random.choice(all_lines)


with Client('test',
            api_id=api_id,
            api_hash=api_hash,
            app_version="1.0.0",
            device_model="PC",
            system_version="Linux", phone_number=phone_number) as client:
    index = 0
    grop_info = {}
    for dialog in client.get_dialogs():
        if str(dialog.chat.type) == 'ChatType.SUPERGROUP':
            print(index, dialog.chat.title)
            index += 1
            grop_info.setdefault(index, dialog.chat.id)
    for i, d in grop_info.items():
        print(i, d)

    select = IntPrompt.ask(f'select the number of chat to send message to: 0-{len(grop_info)}')
    num_send = IntPrompt.ask('how match time to send recommended 50')

    grop_to = grop_info.get(select)
    if grop_to:
        for i in range(num_send + 1):
            client.send_message(grop_to, random_message() + "تحيا إسرائيل 🇮🇱")
            time.sleep(2)
