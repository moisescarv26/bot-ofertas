"""
Bot de Ofertas Amazon - Telegram
Autor: Moises Carvalho de França
Tag Afiliada: moisescarv07-20
"""

import os
import json
import random
import logging
import hashlib
from datetime import datetime
from pathlib import Path

import requests

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DE LOGGING
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
AFFILIATE_TAG = "moisescarv07-20"
TELEGRAM_TOKEN = os.environ.get("8780348557:AAFmjkBMxTYv8YnyUCkAyHQ8IbosVEPKPJo", "")
TELEGRAM_CHANNEL = os.environ.get("-1003922054940", "")
SENT_HISTORY_FILE = Path("data/sent_history.json")
PRODUCTS_FILE = Path("data/produtos.json")

MAX_HISTORY = 100          # Máximo de produtos no histórico de enviados
DELAY_ENTRE_MSGS = 2       # Segundos entre requisições à API do Telegram


# ─────────────────────────────────────────────
# UTILITÁRIOS
# ─────────────────────────────────────────────

def load_json(path: Path) -> dict | list:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return [] if "history" in str(path) else {}


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def product_hash(product: dict) -> str:
    key = f"{product.get('nome', '')}{product.get('preco_atual', '')}"
    return hashlib.md5(key.encode()).hexdigest()


def build_affiliate_link(url: str) -> str:
    """Adiciona ou substitui a tag de afiliado na URL da Amazon."""
    if not url:
        return url
    # Remove tag anterior se houver
    if "tag=" in url:
        import re
        url = re.sub(r"tag=[^&]+", f"tag={AFFILIATE_TAG}", url)
    else:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}tag={AFFILIATE_TAG}"
    return url


def calcular_desconto(preco_original: float, preco_atual: float) -> int:
    if preco_original <= 0 or preco_atual >= preco_original:
        return 0
    return round(((preco_original - preco_atual) / preco_original) * 100)


# ─────────────────────────────────────────────
# GERADOR DE COPY
# ─────────────────────────────────────────────

ABERTURAS = [
    "🔥 *OFERTA IMPERDÍVEL*",
    "⚡ *PROMOÇÃO RELÂMPAGO*",
    "🚨 *ALERTA DE DESCONTO*",
    "💣 *BOMBA DE OFERTA*",
    "🎯 *ACHADO DO DIA*",
    "🏆 *TOP OFERTA HOJE*",
    "🔴 *QUEIMA DE ESTOQUE*",
    "💥 *DESCONTO ABSURDO*",
]

URGENCIAS = [
    "⏳ *Promoção por tempo LIMITADO!*",
    "🚨 Estoque acabando — não perca!",
    "⚡ Válido enquanto durar o estoque",
    "🔥 Oferta pode sair a qualquer momento",
    "⏰ Últimas unidades com esse preço!",
    "❗ Preço pode subir a qualquer hora",
    "🛑 Aproveite antes que esgote!",
    "💨 Voando dos estoques — corra!",
]

CTAS = [
    "🛒 *Comprar agora com desconto:*",
    "👆 *Garantir o meu desconto:*",
    "🔗 *Ver oferta completa:*",
    "✅ *Pegar promoção agora:*",
    "🎁 *Aproveitar oferta:*",
    "💳 *Comprar com desconto:*",
]

BENEFICIOS_POR_CATEGORIA = {
    "suplementos": [
        "⚡ Entrega rápida para todo o Brasil",
        "✅ Marca confiável com ótimas avaliações",
        "💪 Ideal para quem treina sério",
        "🥇 Produto mais vendido na categoria",
        "🔬 Fórmula comprovada cientificamente",
    ],
    "corrida": [
        "🏃 Equipamento essencial para corredores",
        "🌟 Alta performance comprovada",
        "🦵 Tecnologia que protege suas articulações",
        "📦 Frete grátis disponível",
        "⭐ Mais de 4,5 estrelas nas avaliações",
    ],
    "tecnologia": [
        "📱 Tecnologia de última geração",
        "🔋 Bateria de longa duração",
        "✅ Garantia do fabricante inclusa",
        "🚀 Desempenho superior à concorrência",
        "🌐 Compatível com Android e iOS",
    ],
    "gadgets": [
        "🎁 Presente perfeito para qualquer ocasião",
        "🔧 Fácil de usar e configurar",
        "🌟 Design moderno e sofisticado",
        "📦 Entrega expressa disponível",
        "💯 Produto com excelentes avaliações",
    ],
    "fitness": [
        "💪 Eleva seus treinos ao próximo nível",
        "🏋️ Recomendado por personal trainers",
        "🔥 Acelera seus resultados",
        "✅ Durável e resistente ao uso intenso",
        "⭐ Favorito entre atletas profissionais",
    ],
}

HASHTAGS_POR_CATEGORIA = {
    "suplementos":  "#Suplementos #Nutrição #Whey #Creatina #Amazon #Oferta #Fitness #Musculação",
    "corrida":      "#Corrida #Running #Maratona #Atletismo #Amazon #Oferta #Esporte",
    "tecnologia":   "#Tecnologia #Tech #Gadget #Amazon #Oferta #Eletrônicos #Inovação",
    "gadgets":      "#Gadgets #Tech #Amazon #Oferta #Presente #Novidade #Inovação",
    "fitness":      "#Fitness #Academia #Treino #Saúde #Amazon #Oferta #Bem-estar",
}


def gerar_copy(produto: dict) -> str:
    nome = produto["nome"]
    preco_original = float(produto.get("preco_original", 0))
    preco_atual = float(produto["preco_atual"])
    categoria = produto.get("categoria", "fitness").lower()
    desconto = calcular_desconto(preco_original, preco_atual)
    link = build_affiliate_link(produto["link"])

    abertura = random.choice(ABERTURAS)
    urgencia = random.choice(URGENCIAS)
    cta = random.choice(CTAS)

    beneficios_lista = BENEFICIOS_POR_CATEGORIA.get(
        categoria, BENEFICIOS_POR_CATEGORIA["fitness"]
    )
    beneficio = random.choice(beneficios_lista)
    hashtags = HASHTAGS_POR_CATEGORIA.get(categoria, "#Amazon #Oferta #Promoção")

    linhas = [abertura, "", f"📦 *{nome}*", ""]

    if preco_original > 0 and desconto > 0:
        linhas += [
            f"~~💸 De R$ {preco_original:.2f}~~",
            f"🔥 Por apenas *R$ {preco_atual:.2f}*",
            f"🎯 *{desconto}% OFF* — economia real!",
        ]
    else:
        linhas += [f"💰 *R$ {preco_atual:.2f}*"]

    linhas += [
        "",
        beneficio,
        urgencia,
        "",
        cta,
        f"👉 {link}",
        "",
        hashtags,
    ]

    return "\n".join(linhas)


# ─────────────────────────────────────────────
# TELEGRAM
# ─────────────────────────────────────────────

def send_photo_caption(token: str, channel: str, image_url: str, caption: str) -> bool:
    """Envia foto + legenda formatada no Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": channel,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    try:
        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        if data.get("ok"):
            logger.info(f"✅ Mensagem enviada com sucesso! message_id={data['result']['message_id']}")
            return True
        else:
            logger.error(f"❌ Telegram API error: {data}")
            # Tenta enviar só texto se a imagem falhar
            return send_text_only(token, channel, caption)
    except Exception as e:
        logger.error(f"❌ Exceção ao enviar foto: {e}")
        return send_text_only(token, channel, caption)


def send_text_only(token: str, channel: str, text: str) -> bool:
    """Fallback: envia apenas texto caso a imagem falhe."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": channel,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    try:
        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        if data.get("ok"):
            logger.info("✅ Texto enviado com fallback (sem imagem).")
            return True
        logger.error(f"❌ Falha no fallback de texto: {data}")
        return False
    except Exception as e:
        logger.error(f"❌ Exceção no fallback: {e}")
        return False


# ─────────────────────────────────────────────
# GESTÃO DE HISTÓRICO (anti-repetição)
# ─────────────────────────────────────────────

def load_history() -> list:
    data = load_json(SENT_HISTORY_FILE)
    return data if isinstance(data, list) else []


def save_history(history: list) -> None:
    # Mantém apenas os últimos MAX_HISTORY itens
    save_json(SENT_HISTORY_FILE, history[-MAX_HISTORY:])


def pick_unsent_product(products: list, history: list) -> dict | None:
    """Escolhe produto que ainda não foi enviado recentemente."""
    sent_hashes = set(history)
    candidatos = [p for p in products if product_hash(p) not in sent_hashes]

    if not candidatos:
        logger.warning("⚠️ Todos os produtos já foram enviados. Resetando histórico.")
        return random.choice(products)

    # Prioriza produtos com maior desconto
    candidatos_com_desconto = [
        p for p in candidatos
        if calcular_desconto(
            float(p.get("preco_original", 0)),
            float(p["preco_atual"])
        ) >= 10
    ]

    pool = candidatos_com_desconto if candidatos_com_desconto else candidatos
    return random.choice(pool)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    logger.info("═" * 50)
    logger.info(f"🚀 Bot iniciado — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # Validação de credenciais
    if not TELEGRAM_TOKEN:
        logger.critical("❌ TELEGRAM_BOT_TOKEN não configurado!")
        raise SystemExit(1)
    if not TELEGRAM_CHANNEL:
        logger.critical("❌ TELEGRAM_CHANNEL_ID não configurado!")
        raise SystemExit(1)

    # Carrega produtos
    products = load_json(PRODUCTS_FILE)
    if not isinstance(products, list) or not products:
        logger.critical("❌ Nenhum produto encontrado em data/produtos.json")
        raise SystemExit(1)

    logger.info(f"📦 {len(products)} produtos carregados.")

    # Histórico anti-repetição
    history = load_history()
    logger.info(f"📜 Histórico: {len(history)} produtos já enviados.")

    # Seleciona produto
    produto = pick_unsent_product(products, history)
    logger.info(f"🎯 Produto selecionado: {produto['nome']}")

    # Gera copy
    copy_text = gerar_copy(produto)
    logger.info(f"📝 Copy gerada ({len(copy_text)} chars).")

    # Envia para o Telegram
    imagem = produto.get("imagem", "")
    sucesso = (
        send_photo_caption(TELEGRAM_TOKEN, TELEGRAM_CHANNEL, imagem, copy_text)
        if imagem
        else send_text_only(TELEGRAM_TOKEN, TELEGRAM_CHANNEL, copy_text)
    )

    if sucesso:
        # Registra no histórico
        history.append(product_hash(produto))
        save_history(history)
        logger.info("✅ Oferta publicada e histórico atualizado.")
    else:
        logger.error("❌ Falha ao publicar a oferta.")
        raise SystemExit(1)

    logger.info("═" * 50)


if __name__ == "__main__":
    main()
