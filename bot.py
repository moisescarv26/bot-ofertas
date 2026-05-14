from telegram import Bot
import asyncio
import json
import random

TOKEN = "8780348557:AAFmjkBMxTYv8YnyUCkAyHQ8IbosVEPKPJo"
CHAT_ID = "-1003922054940"

bot = Bot(token=TOKEN)

descricoes = [
    "🔥 Oferta encontrada automaticamente",
    "⚡ Excelente oportunidade",
    "💥 Produto em destaque",
    "🚀 Vale a pena conferir"
]

urgencia = [
    "⏳ Oferta pode acabar rápido",
    "🚨 Promoção relâmpago",
    "🔥 Aproveite antes que aumente",
    "⚡ Últimas unidades"
]

hashtags = [
    "#Amazon",
    "#Promoção",
    "#Ofertas",
    "#Desconto"
]

async def main():

    with open("produtos.json", "r", encoding="utf-8") as file:
        produtos = json.load(file)

    produto = random.choice(produtos)

    desconto = round(
        ((produto["preco_antigo"] - produto["preco_atual"]) /
        produto["preco_antigo"]) * 100
    )

    mensagem = f"""
{random.choice(descricoes)}

📦 {produto["nome"]}

💰 De R$ {produto["preco_antigo"]}
🔥 Por R$ {produto["preco_atual"]}

🎯 {desconto}% OFF

{random.choice(urgencia)}

🛒 Comprar agora:
{produto["link"]}

{' '.join(random.sample(hashtags, 3))}
"""

    try:

        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=produto["imagem"],
            caption=mensagem
        )

        print("Imagem enviada com sucesso")

    except Exception as erro:

        print("Erro imagem:", erro)

        await bot.send_message(
            chat_id=CHAT_ID,
            text=mensagem
        )

        print("Mensagem enviada sem imagem")

asyncio.run(main())
