from telegram import Bot
import asyncio

TOKEN = "8780348557:AAFmjkBMxTYv8YnyUCkAyHQ8IbosVEPKPJo"
CHAT_ID = "-1003922054940"

async def main():

    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text="🚀 BOT AUTOMÁTICO FUNCIONANDO PELO GITHUB"
    )

asyncio.run(main())
