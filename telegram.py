import asyncio
import os.path
import random
from pyrogram import Client
from rich.prompt import IntPrompt
from rich.console import Console
from rich.table import Table
from rich import print

"""
config info for the app to run
"""
# get you api and api hash from https://my.telegram.org/auth
API_HASH = 'hlhlhlhlhl'
API_ID = 'glglglglgl'
PHONE_NUMBER = '+972 xx xxx xxx'
SESSION_NAME = 'flooder'

FLOOD_INTERVAL = 27  # seconds
SLEEP_DURATION_MIN = 1  # seconds
SLEEP_DURATION_MAX = 5  # seconds

console = Console()


def login():
    if not os.path.exists(f'{SESSION_NAME}.session'):
        with Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER):
            pass
        print(success('login successfully'))


def error(message):
    return f'[red][!][white] {message}'


def info(message):
    return f'[white][[blue]*[white]] {message}'


def success(message):
    return f'[green on green3][[blue]+[black on green3]] {message}'


async def get_groups(client):
    groups = []
    async for dialog in client.get_dialogs():
        if str(dialog.chat.id).startswith('-'):
            chat_id, chat_title = dialog.chat.id, dialog.chat.title
            groups.append((chat_id, chat_title))
    return groups


def random_message():
    with open('fack_arab.txt', 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
        return random.choice(all_lines).strip()


async def flooder(client, num_send, group_id):
    success_flood = 0
    for _ in range(num_send):
        message = f"{random_message()}تحيا إسرائيل 🇮🇱 "
        await client.send_message(group_id, message)
        success_flood += 1
        sleep_duration = random.uniform(SLEEP_DURATION_MIN, SLEEP_DURATION_MAX)
        print(info(f"message send and sleep for {sleep_duration:.2f} seconds to avoid detection"))
        await asyncio.sleep(sleep_duration)

        if success_flood % FLOOD_INTERVAL == 0:
            print(success(f'Flooded {success_flood} messages'))
            print(error(f'Waiting for {FLOOD_INTERVAL} seconds to avoid flood detection...'))
            await asyncio.sleep(FLOOD_INTERVAL)

    return success_flood


async def main():
    success_flood = 0
    async with Client(SESSION_NAME) as client:
        groups = await get_groups(client)
        table = Table(show_header=True, header_style="bold cyan", show_lines=True)
        table.add_column("Index", style="white", justify="center")
        table.add_column("Group Name", style="green", justify="center")
        for index, (chat_id, chat_title) in enumerate(groups, start=1):
            table.add_row(str(index), chat_title or str(f"name is None chat id - {chat_id}"))

        console.print(table)
        while True:
            group_number = IntPrompt.ask(
                info(f'Select a group by index (1-{len(groups)}) - [red]press Ctrl+c to quit!'))
            if group_number in range(1, len(groups) + 1):
                break
            else:
                console.print(error('Invalid index, try again'))

        num_send = IntPrompt.ask('how many times to send', default=50)
        group_id, group_title = groups[group_number - 1]
        try:
            success_flood = await flooder(client, num_send, group_id)
        except Exception as ERR:
            print(error(f'Error: {ERR}'))
        while success_flood != num_send:
            print(error(f'sleep for 21 sec to pass detection - press Ctrl+c to quit!'))
            await asyncio.sleep(21)
            flood_left = num_send - success_flood
            try:
                success_flood += await flooder(client, flood_left, group_id)
            except Exception as ERR:
                print(error(f'Error: {ERR}'))
    print(success("the flood is complete goodbye!"))


if __name__ == '__main__':
    print(info('Starting the flood script...'))
    try:
        login()
        asyncio.run(main())
    except KeyboardInterrupt:
        print(error('Script interrupted by the user. Exiting...'))
    except Exception as err:
        print(error(f'Error: {err}'))
