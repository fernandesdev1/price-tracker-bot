from tracker.storage import SQLiteStorage
from tracker.scraper import PriceScraper
from tracker.notifier import Notifier
from datetime import datetime

class PriceMonitor:
    def __init__(self, storage: SQLiteStorage, scraper: PriceScraper):
        self.storage = storage
        self.scraper = scraper
        self.notifier = Notifier()

    def check_prices(self):
        products = self.storage.get_all_products()
        agora = datetime.now().strftime('%d/%m/%Y %H:%M')
        print(f"[{agora}] Iniciando checagem de {len(products)} produtos...")
        
        for p in products:
            try:
                print(f"Verificando {p.name}...")
                _, preco_novo = self.scraper.scrape(p.url)
                
                if preco_novo is not None:
                    preco_antigo = p.current_price
                    
                    if preco_antigo is None or preco_novo != preco_antigo:
                        self.storage.add_price_history(p.id, preco_novo)
                        
                        if preco_antigo is not None and preco_novo < preco_antigo:
                            self.notifier.notify_terminal(p.name, preco_antigo, preco_novo)
                            self.notifier.notify_system(p.name, preco_novo)
                        else:
                            print(f"Preço atualizado: {preco_antigo} -> {preco_novo}")
                    else:
                        print(f"Sem alteração para {p.name}")
                else:
                    print(f"Não consegui pegar o preço de {p.name}")
            except Exception as e:
                print(f"Erro ao processar {p.name}: {e}")

        print("Monitoramento finalizado.")
