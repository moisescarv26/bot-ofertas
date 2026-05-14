"""
Utilitário para adicionar novos produtos ao produtos.json
Uso: python src/add_produto.py
"""

import json
from pathlib import Path

PRODUCTS_FILE = Path("data/produtos.json")

CATEGORIAS = ["suplementos", "corrida", "tecnologia", "gadgets", "fitness"]


def load_products():
    if PRODUCTS_FILE.exists():
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


def add_product():
    print("\n" + "═" * 50)
    print("  ➕ ADICIONAR NOVO PRODUTO")
    print("═" * 50)

    nome = input("\n📦 Nome do produto: ").strip()
    if not nome:
        print("❌ Nome obrigatório!")
        return

    print(f"\nCategorias disponíveis: {', '.join(CATEGORIAS)}")
    categoria = input("🏷️  Categoria: ").strip().lower()
    if categoria not in CATEGORIAS:
        print(f"⚠️  Categoria inválida. Usando 'fitness'.")
        categoria = "fitness"

    try:
        preco_original = float(input("💸 Preço original (R$): ").replace(",", "."))
        preco_atual = float(input("🔥 Preço atual/promoção (R$): ").replace(",", "."))
    except ValueError:
        print("❌ Preço inválido!")
        return

    link = input("🔗 Link do produto Amazon: ").strip()
    if not link:
        print("❌ Link obrigatório!")
        return

    imagem = input("🖼️  URL da imagem (Enter para pular): ").strip()

    desconto = round(((preco_original - preco_atual) / preco_original) * 100) if preco_original > 0 else 0

    novo = {
        "nome": nome,
        "categoria": categoria,
        "preco_original": preco_original,
        "preco_atual": preco_atual,
        "link": link,
        "imagem": imagem,
        "ativo": True,
    }

    products = load_products()
    products.append(novo)
    save_products(products)

    print(f"\n✅ Produto adicionado com sucesso!")
    print(f"   Nome: {nome}")
    print(f"   Desconto calculado: {desconto}% OFF")
    print(f"   Total de produtos: {len(products)}")


if __name__ == "__main__":
    add_product()
