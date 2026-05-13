from telegram import Bot
import asyncio
import json
import random

TOKEN = "8780348557:AAFmjkBMxTYv8YnyUCkAyHQ8IbosVEPKPJo"
CHAT_ID = "-1003922054940"

bot = Bot(token=TOKEN)

async def enviar_oferta():

    with open("produtos.json", "r", encoding="utf-8") as file:
        produtos = json.load(file)

    produto = random.choice(produtos)

    desconto = round(
        ((produto["preco_normal"] - produto["preco_promocao"]) /
        produto["preco_normal"]) * 100
    )

    mensagem = f"""
🔥 OFERTA ENCONTRADA

📦 {produto['titulo']}

💰 De R$ {produto['preco_normal']}
🔥 Por R$ {produto['preco_promocao']}

🎯 Desconto de {desconto}%

✅ Oferta em destaque
✅ Confira antes que acabe

🛒 Comprar agora:
{produto['link']}
"""

    await bot.send_photo(
        chat_id=CHAT_ID,
        photo=produto["imagem"],
        caption=mensagem
    )

asyncio.run(enviar_oferta())
