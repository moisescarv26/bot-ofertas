from telegram import Bot
import asyncio
import random

TOKEN = "8780348557:AAFmjkBMxTYv8YnyUCkAyHQ8IbosVEPKPJo"
CHAT_ID = "-1003922054940"

produtos = [

    {
        "titulo": "🔥 Smartwatch Esportivo",
        "preco": "R$ 129,90",
        "link": "https://amzn.to/seulink1",
        "imagem": "https://picsum.photos/500?1"
    },

    {
        "titulo": "🎧 Headset Gamer RGB",
        "preco": "R$ 149,90",
        "link": "https://amzn.to/seulink2",
        "imagem": "https://picsum.photos/500?2"
    },

    {
        "titulo": "⌚ Relógio Inteligente",
        "preco": "R$ 89,90",
        "link": "https://amzn.to/seulink3",
        "imagem": "https://picsum.photos/500?3"
    }

]

async def enviar_oferta():

    bot = Bot(token=TOKEN)

    produto = random.choice(produtos)

    mensagem = f"""
{produto['titulo']}

💰 {produto['preco']}

✅ Oferta por tempo limitado
✅ Confira antes que acabe

🛒 Comprar:
{produto['link']}
"""

    await bot.send_photo(
        chat_id=CHAT_ID,
        photo=produto['imagem'],
        caption=mensagem
    )

asyncio.run(enviar_oferta())