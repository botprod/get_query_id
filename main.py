from utils.core.telegram import Accounts
from utils.starter import start
import asyncio
from data import config

import os


async def main():
    print("Soft's author: @botpr0d\n")
    username = input("Enter bot's username: ")
    short_name = input("Enter bot's short name: ")
    if input('Do you have referral code? (y/n) ').lower() == 'y':
        referral_code = input('Enter referral code (all after start_app= ): ')
    else:
        referral_code = ""
    if not os.path.exists('sessions'):
        os.mkdir('sessions')

    if config.PROXY['USE_PROXY_FROM_FILE']:
        if not os.path.exists(config.PROXY['PROXY_PATH']):
            with open(config.PROXY['PROXY_PATH'], 'w') as f:
                f.write("")
    else:
        if not os.path.exists('sessions/accounts.json'):
            with open("sessions/accounts.json", 'w') as f:
                f.write("[]")
    accounts = await Accounts().get_accounts()

    tasks = []

    for thread, account in enumerate(accounts):
        session_name, phone_number, proxy = account.values()
        tasks.append(asyncio.create_task(
            start(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy, username=username,
                  short_name=short_name, referral_code=referral_code)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
