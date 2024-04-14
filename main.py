import asyncio
import bot
import db

if __name__ == "__main__":
    db.start_db()
    asyncio.run(bot.start_bot())
