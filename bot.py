from telegram import Bot
import asyncio
import json
import random

TOKEN = "SEU_TOKEN"
CHAT_ID = "-1003922054940"

async def main():

    bot = Bot(token=TOKEN)

    with open("produtos.json", "r", encoding="utf-8") as file:
        produtos = json.load(file)

    produto = random.choice(produtos)

    desconto = round(
        ((produto["preco_normal"] - produto["preco_promocao"]) /
        produto["preco_normal"]) * 100
    )

    descricao = [
        "🔥 Oferta por tempo limitado",
        "⚡ Excelente custo-benefício",
        "🚀 Produto muito procurado",
        "💥 Vale a pena conferir",
        "🎯 Ótima oportunidade"
    ]

    mensagem = f"""
{random.choice(descricao)}

📦 {produto['titulo']}

💰 De R$ {produto['preco_normal']}
🔥 Por R$ {produto['preco_promocao']}

🎯 {desconto}% OFF

🛒 Comprar:
{produto['link']}
"""

    await bot.send_message(
        chat_id=CHAT_ID,
        text=mensagem
    )

asyncio.run(main())
