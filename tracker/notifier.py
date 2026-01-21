from plyer import notification

class Notifier:
    @staticmethod
    def notify_terminal(product_name: str, old_price: float, new_price: float):
        diff = old_price - new_price
        percent = (diff / old_price) * 100
        print("\n" + "💰"*25)
        print("🚨 ALERTA: O PREÇO CAIU! 🚨")
        print(f"Produto: {product_name}")
        print(f"Preço Antigo: R$ {old_price:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        print(f"Preço Novo:   R$ {new_price:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        print(f"Economia:     R$ {diff:,.2f} ({percent:.1f}%)".replace(",", "X").replace(".", ",").replace("X", "."))
        print("💰"*25 + "\n")

    @staticmethod
    def notify_system(product_name: str, new_price: float):
        try:
            notification.notify(
                title='Preço baixou!',
                message=f'{product_name} agora está R$ {new_price:,.2f}!',
                app_name='PriceTracker',
                timeout=10
            )
        except Exception as e:
            print(f"Falha na notificação: {e}")
