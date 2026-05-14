from telegram import Bot
import asyncio
import json

TOKEN = "8780348557:AAFmjkBMxTYv8YnyUCkAyHQ8IbosVEPKPJo"
CHAT_ID = "-1003922054940"

async def main():

    bot = Bot(token=TOKEN)

    with open("produtos.json", "r", encoding="utf-8") as file:
        produtos = json.load(file)

    produto = produtos[0]

    mensagem = f"""
🔥 TESTE AUTOMÁTICO

📦 {produto["titulo"]}

💰 De R$ {produto["preco_normal"]}
🔥 Por R$ {produto["preco_promocao"]}

🛒 Comprar:
{produto["link"]}
"""

    # TESTE SEM IMAGEM PRIMEIRO
    await bot.send_message(
        chat_id=CHAT_ID,
        text=mensagem
    )

    print("Mensagem enviada com sucesso")

asyncio.run(main())
