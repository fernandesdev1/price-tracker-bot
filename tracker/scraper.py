import requests
from bs4 import BeautifulSoup
import re
from typing import Optional, Tuple
from tracker.models import Product
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PriceScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        }

    def fetch_page(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, headers=self.headers, timeout=15, verify=False)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Ops, deu erro ao acessar {url}: {e}")
            return None

    def _clean_price(self, price_str: str) -> Optional[float]:
        if not price_str:
            return None
        price_str = price_str.replace('R$', '').replace('$', '').strip()
        
        try:
            if ',' in price_str and '.' in price_str:
                if price_str.find('.') < price_str.find(','): 
                    price_str = price_str.replace('.', '').replace(',', '.')
            elif ',' in price_str:
                price_str = price_str.replace(',', '.')
            
            price_str = re.sub(r'[^\d.]', '', price_str)
            price = float(price_str)
            return price if price > 0 else None
        except ValueError:
            return None

    def scrape(self, url: str) -> Tuple[Optional[str], Optional[float]]:
        html = self.fetch_page(url)
        if not html:
            return None, None

        soup = BeautifulSoup(html, 'html.parser')
        
        name = self._extract_name(soup)
        price = self._extract_price(soup)

        if not name:
            name = "Produto sem nome"

        return name, price

    def _extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        meta_title = soup.find('meta', property='og:title')
        if meta_title:
            return meta_title['content'].strip()
            
        return soup.title.string.strip() if soup.title else "Produto Desconhecido"

    def _extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        price_meta = soup.find('meta', property='product:price:amount')
        if price_meta:
            return self._clean_price(price_meta['content'])
            
        price_selectors = [
            '.price', '#price', '.current-price', '.price-tag-fraction',
            '[data-price]', '.a-price-whole', '.ui-pdp-price__part'
        ]
        
        for selector in price_selectors:
            el = soup.select_one(selector)
            if el:
                return self._clean_price(el.get_text())

        return None
