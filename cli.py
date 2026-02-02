import argparse
import sys
from tracker.storage import SQLiteStorage
from tracker.scraper import PriceScraper
from tracker.models import Product
from tabulate import tabulate
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Bot Rastreador de Preços")
    subparsers = parser.add_subparsers(dest="comando")

    add_parser = subparsers.add_parser("add", help="Adiciona um produto para monitorar")
    add_parser.add_argument("url", help="URL do produto")

    subparsers.add_parser("lista", help="Lista todos os produtos")

    remove_parser = subparsers.add_parser("remover", help="Remove um produto")
    remove_parser.add_argument("id", type=int, help="ID do produto")

    args = parser.parse_args()
    storage = SQLiteStorage()
    scraper = PriceScraper()

    if args.comando == "add":
        if not args.url.startswith("http"):
            print("Erro: A URL precisa começar com http:// ou https://")
            return

        print(f"Buscando informações em {args.url}...")
        nome, preco = scraper.scrape(args.url)
        
        if nome:
            p = Product(name=nome, url=args.url, current_price=preco, last_updated=datetime.now())
            pid = storage.add_product(p)
            print(f"Produto adicionado: {nome} (ID: {pid}) - Preço: {p.formatted_price}")
        else:
            print("Puxa, não consegui ler as infos do produto. Veja se a URL tá certa.")

    elif args.comando == "lista":
        produtos = storage.get_all_products()
        if not produtos:
            print("Nenhum produto sendo monitorado ainda.")
            return

        dados = []
        for p in produtos:
            dados.append([p.id, p.name, p.formatted_price, p.last_updated])
        
        print("\nLista de Monitoramento:")
        print(tabulate(dados, headers=["ID", "Nome", "Preço Atual", "Última Verificação"], tablefmt="grid"))

    elif args.comando == "remover":
        storage.delete_product(args.id)
        print(f"Produto {args.id} removido com sucesso!")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
