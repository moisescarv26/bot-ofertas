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
        "🔥 Muito usado nos treinos",
        "⚡ Ótimo custo-benefício",
        "🏋️ Produto muito procurado"
    ],

    "Tecnologia": [
        "🚀 Produto em alta",
        "🔥 Excelente oportunidade",
        "⚡ Tecnologia com ótimo preço",
        "🎯 Vale a pena conferir"
    ]
}

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

    try:

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

{' '.join(random.sample(hashtags, 3))}
"""

        # tenta enviar imagem
        try:

            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=produto["imagem"],
                caption=mensagem
            )

            print("Imagem enviada com sucesso")

        except Exception as erro_imagem:

            print("Erro imagem:", erro_imagem)

            # fallback sem imagem
            await bot.send_message(
                chat_id=CHAT_ID,
                text=mensagem
            )

            print("Mensagem enviada sem imagem")

    except Exception as erro:

        print("ERRO GERAL:", erro)

asyncio.run(main())
