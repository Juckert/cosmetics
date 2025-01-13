import asyncio
import logging
from aiogram import Bot, Dispatcher
from tessfiles.telefiles.config import TOKEN
from tessfiles.telefiles.handlers import router, im

prev_time = im.get_time()


class DoBotInterface:
    def __init__(self):
        self.__bot__ = Bot(TOKEN)
        self.__dispatch__ = Dispatcher()

    async def __run__(self):
        self.__dispatch__.include_router(router)
        await self.__dispatch__.start_polling(self.__bot__)

    def main_process(self):
        logging.basicConfig(level=logging.INFO)
        try:
            asyncio.run(self.__run__())
        except KeyboardInterrupt:
            print('EXIT')

