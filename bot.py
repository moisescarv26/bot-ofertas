from telegram import Bot
import asyncio
import feedparser

TOKEN = "8780348557:AAFmjkBMxTYv8YnyUCkAyHQ8IbosVEPKPJo"
CHAT_ID = "-1003922054940"

bot = Bot(token=TOKEN)

RSS_URL = "https://www.promobit.com.br/feed/"

async def main():

    feed = feedparser.parse(RSS_URL)

    mensagem = "🔥 TESTE RSS\n\n"

    for item in feed.entries[:5]:
        mensagem += f"{item.title}\n{item.link}\n\n"

    await bot.send_message(
        chat_id=CHAT_ID,
        text=mensagem
    )

asyncio.run(main())
