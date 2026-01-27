import schedule
import time
import argparse
from tracker.storage import SQLiteStorage
from tracker.scraper import PriceScraper
from tracker.monitor import PriceMonitor

def realizar_checagem():
    storage = SQLiteStorage()
    scraper = PriceScraper()
    monitor = PriceMonitor(storage, scraper)
    monitor.check_prices()

def main():
    parser = argparse.ArgumentParser(description="Serviço de Monitoramento de Preços")
    parser.add_argument("--intervalo", type=int, default=60, help="Intervalo em minutos (padrão: 60)")
    parser.add_argument("--agora", action="store_true", help="Rodar uma vez agora")
    
    args = parser.parse_args()

    if args.agora:
        realizar_checagem()
        return

    print(f"Rastreador de Preços iniciado! Vou verificar a cada {args.intervalo} minutos.")
    
    realizar_checagem()

    schedule.every(args.intervalo).minutes.do(realizar_checagem)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSaindo do Rastreador...")

if __name__ == "__main__":
    main()
