import os
import json
import random
import asyncio
import requests
from telegram import Bot

# Configurações via Variáveis de Ambiente (GitHub Secrets)
TOKEN = os.getenv("8780348557:AAFmjkBMxTYv8YnyUCkAyHQ8IbosVEPKPJo")
CHAT_ID = os.getenv("-1003922054940")
AMAZON_TAG = "moisescarv07-20"

def carregar_produtos():
    with open('produtos.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_produtos(produtos):
    with open('produtos.json', 'w', encoding='utf-8') as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

def gerar_link_afiliado(url_base):
    connector = "&" if "?" in url_base else "?"
    return f"{url_base}{connector}tag={AMAZON_TAG}"

def calcular_desconto(de, por):
    desconto = ((de - por) / de) * 100
    return int(desconto)

def formatar_copy(produto):
    pct_off = calcular_desconto(produto['preco_de'], produto['preco_por'])
    link = gerar_link_afiliado(produto['url_base'])
    
    copy = (
        f"🔥 *OFERTA RELÂMPAGO*\n\n"
        f"📦 *{produto['nome']}*\n\n"
        f"💰 De ~~R$ {produto['preco_de']:.2f}~~\n"
        f"🔥 *Por R$ {produto['preco_por']:.2f}*\n\n"
        f"🎯 *{pct_off}% OFF*\n\n"
        f"⚡ Excelente custo-benefício\n"
        f"🚨 Aproveite antes que acabe!\n\n"
        f"🛒 *Comprar agora:*\n"
        f"[{link}]({link})\n\n"
        f"#Amazon #{produto['categoria']} #Promoção"
    )
    return copy

async def enviar_oferta():
    produtos = carregar_produtos()
    # Filtra produtos não enviados
    disponiveis = [p for p in produtos if not p.get('enviado')]
    
    if not disponiveis:
        print("Todos os produtos já foram enviados.")
        return

    produto = random.choice(disponiveis)
    bot = Bot(token=TOKEN)
    
    try:
        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=produto['imagem'],
            caption=formatar_copy(produto),
            parse_mode='Markdown'
        )
        
        # Marcar como enviado
        for p in produtos:
            if p['id'] == produto['id']:
                p['enviado'] = True
        salvar_produtos(produtos)
        print(f"Sucesso: {produto['nome']} enviado.")
        
    except Exception as e:
        print(f"Erro ao enviar: {e}")

if __name__ == "__main__":
    asyncio.run(enviar_oferta())
