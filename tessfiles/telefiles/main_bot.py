import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from config import TOKEN
from handlers import router

bot = Bot(TOKEN)
dispatch = Dispatcher()



async def main():
        dispatch.include_router(router)
        await dispatch.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')