from telegram import Bot
import asyncio
import json
import random

TOKEN = "8780348557:AAFmjkBMxTYv8YnyUCkAyHQ8IbosVEPKPJo"
CHAT_ID = "-1003922054940"

bot = Bot(token=TOKEN)

descricoes = {
    "Suplementos": [
        "💪 Excelente para performance",
        "🔥 Muito procurado nos treinos",
        "⚡ Ótimo custo-benefício",
        "🏋️ Excelente opção fitness"
    ],

    "Tecnologia": [
        "🚀 Produto muito procurado",
        "🔥 Excelente oportunidade",
        "⚡ Tecnologia com ótimo preço",
        "🎯 Vale a pena conferir"
    ]
}

urgencia = [
    "⏳ Oferta pode acabar rápido",
    "🚨 Promoção relâmpago",
    "⚡ Aproveite antes que aumente",
    "🔥 Últimas unidades"
]

async def main():

    with open("produtos.json", "r", encoding="utf-8") as file:
        produtos = json.load(file)

    produto = random.choice(produtos)

    desconto = round(
        ((produto["preco_normal"] - produto["preco_promocao"]) /
        produto["preco_normal"]) * 100
    )

    mensagem = f"""
{random.choice(descricoes[produto["categoria"]])}

📦 {produto["titulo"]}

💰 De R$ {produto["preco_normal"]}
🔥 Por R$ {produto["preco_promocao"]}

🎯 {desconto}% OFF

{random.choice(urgencia)}

🛒 Comprar agora:
{produto["link"]}
"""

    await bot.send_message(
        chat_id=CHAT_ID,
        text=mensagem
    )

asyncio.run(main())
