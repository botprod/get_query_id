import json
import os

from utils.core import logger
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
import asyncio
from data import config
import aiohttp
from aiohttp_socks import ProxyConnector


def retry_async(max_retries=2):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            thread, account = args[0].thread, args[0].account
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.error(f"Thread {thread} | {account} | Error: {e}. Retrying {retries}/{max_retries}...")
                    await asyncio.sleep(10)
                    if retries >= max_retries:
                        break

        return wrapper

    return decorator


class GetQuery:

    def __init__(self, thread: int, session_name: str, phone_number: str, proxy: [str, None], username: str,
                 short_name: str, referral_code):
        self.account = session_name
        self.thread = thread
        self.username = username
        self.short_name = short_name
        self.referral_code = referral_code
        self.proxy = f"{config.PROXY['TYPE']['REQUESTS']}://{proxy}" if proxy is not None else None

        if proxy:
            proxy = {
                "scheme": config.PROXY['TYPE']['TG'],
                "hostname": proxy.split(":")[1].split("@")[1],
                "port": int(proxy.split(":")[2]),
                "username": proxy.split(":")[0],
                "password": proxy.split(":")[1].split("@")[0]
            }

        self.client = Client(
            name=session_name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            workdir=config.WORKDIR,
            proxy=proxy,
            lang_code='ru'
        )

    async def write_into_json(self):
        auth_url = await self.get_tg_web_data()
        if auth_url is not None:
            data = {self.account: auth_url}
            json_file_path = os.path.join(config.JSON_WORKDIR, f'{self.username}.json')
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as file:
                    try:
                        existing_data = json.load(file)
                    except json.JSONDecodeError:
                        existing_data = {}
            else:
                existing_data = {}
            existing_data.update(data)
            with open(json_file_path, 'w') as file:
                json.dump(existing_data, file, indent=4)
            return True
        else:
            return False

    async def get_tg_web_data(self):
        try:
            await self.client.connect()
            if self.referral_code != "":
                web_view = await self.client.invoke(RequestAppWebView(
                    peer=await self.client.resolve_peer(self.username),
                    app=InputBotAppShortName(bot_id=await self.client.resolve_peer(self.username),
                                             short_name=self.short_name),
                    platform='android',
                    write_allowed=True,
                    start_param=f'{self.referral_code}'
                ))
            else:
                web_view = await self.client.invoke(RequestAppWebView(
                    peer=await self.client.resolve_peer(self.username),
                    app=InputBotAppShortName(bot_id=await self.client.resolve_peer(self.username),
                                             short_name=self.short_name),
                    platform='android',
                    write_allowed=True
                ))
            await self.client.disconnect()
            return web_view.url
        except:
            return None
