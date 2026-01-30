# price-tracker-bot

Bot em Python para monitorar preços de produtos e registrar mudanças ao longo do tempo.

O projeto foi feito para automatizar o acompanhamento de preços em páginas de e-commerce, evitando a necessidade de checar manualmente. Ele permite adicionar URLs: Amazon, Shopee, etc. Armazenar histórico e identificar quedas de preço.

---

## Funcionalidades

* Monitoramento de preços a partir de URLs
* Extração de nome e preço via scraping (BeautifulSoup)
* Armazenamento de histórico em SQLite
* Detecção de mudança de preço
* Execução periódica (intervalo configurável)
* Interface CLI simples para gerenciar produtos

---

## Stack

* Python 3
* requests
* BeautifulSoup4
* SQLite
* schedule

---

## Como usar

### Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### Adicionar produto

```bash
python cli.py add <url>
```

---

### Listar produtos monitorados

```bash
python cli.py list
```

---

### Rodar monitoramento

```bash
python main.py --interval 30
```

Rodar apenas uma verificação:

```bash
python main.py --now
```

---

## Estrutura

```text
tracker/
├── scraper.py
├── storage.py
├── monitor.py
├── notifier.py
├── models.py
main.py
cli.py
```

---

## Decisões técnicas

* Uso de SQLite para simplificar persistência local
* Separação entre scraping, armazenamento e monitoramento
* CLI isolada para facilitar testes e uso manual

---

## Limitações

* Scraping genérico pode falhar em sites com proteção (ex: Amazon)
* Seletores precisam ser ajustados dependendo do site
* Não utiliza proxies ou headless browser por padrão

Feito por fernandes dev hehe