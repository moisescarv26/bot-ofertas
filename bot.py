from telegram import Bot
import asyncio
import feedparser
import random
import requests
from bs4 import BeautifulSoup

TOKEN = "8780348557:AAFmjkBMxTYv8YnyUCkAyHQ8IbosVEPKPJo"
CHAT_ID = "-1003922054940"

TAG_AFILIADA = "moisescarv07-20"

bot = Bot(token=TOKEN)

RSS_URL = "https://www.promobit.com.br/feed/"

descricoes = [
    "🔥 Oferta encontrada automaticamente",
    "⚡ Excelente oportunidade",
    "💥 Preço muito abaixo do normal",
    "🚀 Produto em destaque",
    "🎯 Vale a pena conferir"
]

urgencia = [
    "⏳ Oferta pode acabar rápido",
    "🚨 Promoção relâmpago",
    "🔥 Aproveite antes que aumente",
    "⚡ Últimas unidades"
]

async def enviar_oferta():

    feed = feedparser.parse(RSS_URL)

    ofertas_amazon = []

    for item in feed.entries:

        link = item.link.lower()

        if "amazon" in link:
            ofertas_amazon.append(item)

    if not ofertas_amazon:
        return

    oferta = random.choice(ofertas_amazon)

    titulo = oferta.title
    link_original = oferta.link

    # adiciona tag afiliada
    if "?" in link_original:
        link_afiliado = f"{link_original}&tag={TAG_AFILIADA}"
    else:
        link_afiliado = f"{link_original}?tag={TAG_AFILIADA}"

    mensagem = f"""
{random.choice(descricoes)}

📦 {titulo}

{random.choice(urgencia)}

🛒 Comprar agora:
{link_afiliado}
"""

    await bot.send_message(
        chat_id=CHAT_ID,
        text=mensagem
    )

asyncio.run(enviar_oferta())
