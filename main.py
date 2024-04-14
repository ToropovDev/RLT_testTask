import asyncio
import db
import bot

request = eval("""{
   "dt_from": "2022-09-01T00:00:00",
   "dt_upto": "2022-12-31T23:59:00",
   "group_type": "month"
}
""")

if __name__ == "__main__":
    asyncio.run(bot.start_bot())
