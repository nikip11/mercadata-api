from pydantic import BaseModel, Field, condecimal
from typing import List, Optional
from datetime import datetime

'''
"ticket_date": "10/01/2025",
"total": "208,04",
"totalCalc": 208.04000000000002,
"invoiceId": "4567-010-591230"
products
    "cantidad": "1",
    "producto": "ZANAHORIA BOLSA",
    "precioPorKg": "N/A",
    "peso": "N/A",
    "precio": "1,02"
'''
class Product(BaseModel):
    cantidad: int = Field(..., description="Cantidad del producto")
    producto: str = Field(..., description="Nombre del producto")
    precioPorKg: Optional[str] = Field("N/A", description="Precio por kilo del producto")
    peso: Optional[str] = Field("N/A", description="Peso del producto")
    precio: condecimal(gt=0, decimal_places=2) = Field(..., description="Precio total del producto")


class Ticket(BaseModel):
    products: List[Product]
    ticket_date: datetime = Field(..., description="Fecha del ticket en formato ISO 8601")
    total: str = Field(..., description="Total como cadena, directamente del ticket")
    totalCalc: condecimal(gt=0, decimal_places=2) = Field(..., description="Total calculado")
    invoiceId: str = Field(..., description="ID único de la factura")



# class InvoiceSchema(BaseModel):
#     # nombre: constr(strict=True) = Field(...)
#     # apellido: constr(strict=True) = Field(...)
#     # dni: conint(strict=True) = Field(...)
#     # nro_socie: conint(strict=True, gt=0) = Field(...)
#     # email: EmailStr = Field(...)
#     # telefono: constr(strict=True) = Field()
#     # direccion: constr(strict=True) = Field()
#     # codigo_postal: constr(strict=True) = Field()
#     # tipo_socio: bool = Field()
#     invoiceId: constr(strict=true) = Field(...)
#     date: constr(strict=true) = Field(...)
#     total: conint(strict=True, gt=0) = Field(...)
#     # total: constr(strict=true) = Field(...)

#     @classmethod
#     def as_optional(cls):
#         annonations = cls.__fields__
#         fields = {
#             attribute: (Optional[data_type.type_], None)
#             for attribute, data_type in annonations.items()
#         }
#         OptionalModel = create_model(f"Optional{cls.__name__}", **fields)
#         return OptionalModel