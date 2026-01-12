from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class PricePoint:
    price: float
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Product:
    url: str
    name: str
    current_price: Optional[float] = None
    id: Optional[int] = None
    last_updated: Optional[datetime] = None
    price_history: List[PricePoint] = field(default_factory=list)

    @property
    def formatted_price(self) -> str:
        if self.current_price is None:
            return "N/A"
        return f"R$ {self.current_price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
