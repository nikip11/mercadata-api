from pydantic import BaseModel, Field, condecimal, validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

class Product(BaseModel):
    cantidad: int = Field(..., description="Cantidad del producto")
    producto: str = Field(..., description="Nombre del producto")
    precioPorKg: Optional[float] = None
    peso: Optional[float] = None       
    precio: float = Field(..., description="Precio total del producto")
    unitPrice: float = Field(..., description="Precio unitario")

    @validator("precio", pre=True)
    def parse_precio(cls, v):
        if isinstance(v, str):
            v = v.replace(",", ".")
        return float(v)

    @validator("precioPorKg", "unitPrice", "peso", pre=True)
    def parse_decimal_fields(cls, v):
        if v is None or str(v).strip().upper() == "N/A":
            return None
        if isinstance(v, str):
            v = v.replace(",", ".")
        return float(v)


class Ticket(BaseModel):
    products: List[Product]
    ticket_date: datetime = Field(..., description="Fecha del ticket en formato ISO 8601")
    total: str = Field(..., description="Total como cadena, directamente del ticket")
    totalCalc: float = Field(..., description="Total calculado")
    invoiceId: str = Field(..., description="ID único de la factura")
    comercio: str = Field(default="Mercadona", description="Nombre del comercio")  # 💡 Valor por defecto

    @validator("ticket_date", pre=True)
    def parse_ticket_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%d/%m/%Y")
        return datetime.fromisoformat(v)

    @validator("total", pre=True)
    def parse_total(cls, v):
        if isinstance(v, str):
            v = v.replace(",", ".")
        return v

    @validator("totalCalc", pre=True)
    def round_total_calc(cls, v):
        if isinstance(v, (float, str)):
            v = Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return float(v)
