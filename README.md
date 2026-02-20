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

## Exemplos Reais de Uso

### No terminal (CLI)
```text
PS C:\Users\llpz7\Desktop\tracker-price> python cli.py add https://www.amazon.com.br/dp/B0F7J2KKFW
Buscando informações em https://www.amazon.com.br/dp/B0F7J2KKFW...
Produto adicionado: Massageador Facial LED (ID: 1) - Preço: R$ 305,00
```

### No Monitoramento
```text
PS C:\Users\llpz7\Desktop\tracker-price> python main.py --agora
Rastreador de Preços iniciado! Vou verificar a cada 60 minutos.
[18/04/2026 16:41] Iniciando checagem de 1 produtos...
Verificando Massageador Facial LED...
Sem alteração para Massageador Facial LED
Monitoramento finalizado.
```

---

## Estrutura do Projeto

*   `tracker/scraper.py`: Inteligência de extração via BeautifulSoup.
*   `tracker/storage.py`: Gerenciamento do banco de dados SQLite (com modo WAL).
*   `tracker/monitor.py`: Lógica central de monitoramento e alertas.
*   `tracker/notifier.py`: Sistema de avisos no terminal e notificações sistêmicas.
*   `tracker/models.py`: Classes de dados (Produto e Histórico).
*   `main.py`: Serviço de agendamento automático.
*   `cli.py`: Interface de linha de comando.

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

Feito por fernandes dev hehe (em constante evolução)