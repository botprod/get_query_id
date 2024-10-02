from utils.get_query import GetQuery
from asyncio import sleep
from random import uniform
from data import config
from utils.core import logger
import asyncio


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None], username: str, short_name: str,
                referral_code: str):
    query = GetQuery(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy,
                     username=username, short_name=short_name, referral_code=referral_code)
    account = session_name + '.session'

    await sleep(uniform(*config.DELAYS['ACCOUNT']))

    attempts = 3
    while attempts:
        try:
            if await query.write_into_json():
                logger.success(f"Thread {thread} | {account} | Writed into json")
            else:
                logger.error(f"Thread {thread} | {account} | Couldn't write into json")
            break
        except Exception as e:
            logger.error(f"Thread {thread} | {account} | Left login attempts: {attempts}, error: {e}")
            await asyncio.sleep(uniform(*config.DELAYS['RELOGIN']))
            attempts -= 1
    else:
        logger.error(f"Thread {thread} | {account} | Couldn't login")
        await query.logout()
        return
