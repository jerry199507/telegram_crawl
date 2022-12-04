from telethon import TelegramClient
from telethon.tl.types import UserStatusOffline, UserStatusRecently, UserStatusLastMonth, UserStatusLastWeek
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest
import time
import asyncio
import numpy as np


api_id = 12345678
api_hash = "xxxxx"
session = "xxxxx"


async def main():
    client = TelegramClient(session, api_id, api_hash)
    await client.start()
    channel_name = input("Please enter the group connection that needs to collect group members：")
    channel = await client.get_entity(channel_name)

    int_time = int(time.time()) - 259200  # 3 days ago
    letters = [chr(i) for i in np.arange(97, 123)]
    all_participants = []

    print(f"Collecting members of group {channel_name}")
    for letter in letters:
        offset = 0
        while True:
            participants = await client(GetParticipantsRequest(channel=channel, offset=offset,
                                                               filter=ChannelParticipantsSearch(letter),
                                                               limit=200, hash=0))
            all_participants.extend(participants.users)
            offset += len(participants.users)
            if len(participants.users) == 0:
                break

    results = []
    path_file = f"{channel.username}.txt"

    for user in all_participants:
        # Filter users without username
        if user.username is None:
            continue
        if isinstance(user.status, UserStatusRecently):
            # last seen recently
            pass
        elif isinstance(user.status, UserStatusLastMonth):
            # last seen last month
            continue
        elif isinstance(user.status, UserStatusLastWeek):
            # last seen last week
            continue
        elif user.status is None:
            # last seen long time ago
            continue
        elif isinstance(user.status, UserStatusRecently):
            # online
            pass
        elif isinstance(user.status, UserStatusOffline):
            # Online within 3 days
            date_online = user.status.was_online
            if int(date_online.timestamp()) < int_time:
                continue
        # filter bot
        if "bot" in str(user.username) or "Bot" in str(user.username):
            continue
        if user.username not in results:
            # Deduplication
            results.append(user.username)
    with open(path_file, 'a', encoding='utf-8') as f:
        for i in results:
            f.write(str(i) + "\n")
    print(f"Collecting members of group {channel_name} completed")

if __name__ == '__main__':
    asyncio.run(main())
