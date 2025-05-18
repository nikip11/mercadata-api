from database import database
from .schema import Ticket
from fastapi.encoders import jsonable_encoder
from datetime import datetime

invoice_collection = database.get_collection("invoices_collections")

def invoice_json(invoice: dict) -> dict:
    invoice["_id"] = str(invoice["_id"])
    if "ticket_date" in invoice and isinstance(invoice["ticket_date"], datetime):
        invoice["ticket_date"] = invoice["ticket_date"].isoformat()  # Convertir datetime a string
    return invoice

async def add_invoice(ticket: Ticket) -> dict:

    ticket = Ticket(**ticket) if isinstance(ticket, dict) else ticket
    check_invoice = await get_one(ticket.invoiceId)
    if check_invoice:
        return invoice_json(check_invoice)
    invoice = await invoice_collection.insert_one(ticket.dict())
    new_invoice = await invoice_collection.find_one({"_id": invoice.inserted_id})
    return invoice_json(new_invoice)

async def get_tickets_byDate(min, max):
    start = datetime.strptime(min, "%Y/%m/%d")
    end = datetime.strptime(max, "%Y/%m/%d")
    query = {"ticket_date": {"$gte": start, "$lte": end}}
    invoices = await invoice_collection.find(query).sort("ticket_date", 1).to_list(200)
    return [invoice_json(ticket) for ticket in invoices]

async def get_tickets():
    invoices = await invoice_collection.find().sort("ticket_date", 1).to_list(200)
    return [invoice_json(ticket) for ticket in invoices]

async def get_one(invoiceId: str):
    invoice = await invoice_collection.find_one({"invoiceId": invoiceId})
    if invoice:
        return invoice_json(invoice)
    return False

async def get_last_price_of_product(product_name):
    pipeline = [
        {"$unwind": "$products"},  # 🎯 Descompone el array de productos
        {"$match": {"products.producto": {"$regex": product_name, "$options": "i"}}},  # 🔎 Búsqueda insensible a mayúsculas/minúsculas
        {"$sort": {"ticket_date": -1}},  # 🗃 Ordena por fecha descendente
        {
            "$group": {
                "_id": "$products.producto",
                "last_price": {"$first": "$products.unitPrice"},
                "last_date": {"$first": "$ticket_date"}
            }
        },
        {"$project": {
            "_id": 0,
            "product": "$_id",
            "last_price": 1,
            "last_date": 1
        }}
    ]
    result = await invoice_collection.aggregate(pipeline).to_list(length=None)
    return result

async def get_totals_by_year(year: int):
    # Crear las fechas de inicio y fin para el año especificado
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31, 23, 59, 59)
    
    pipeline = [
        # Filtrar por el año especificado
        {
            "$match": {
                "ticket_date": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$group": {
                "_id": {"$dateToString": {"format": "%Y-%m", "date": "$ticket_date"}},
                "total": {"$sum": "$totalCalc"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "month": "$_id",
                "total": 1
            }
        },
        {
            "$sort": {"month": 1}
        }
    ]
    result = await invoice_collection.aggregate(pipeline).to_list(length=None)
    return result

async def get_top_products(limit: int = 10):
    """
    Obtiene los productos más comprados, la cantidad de veces que se han comprado y su último precio
    
    :param limit: Límite de productos a devolver (por defecto 10)
    :return: Lista con los productos más comprados, su frecuencia y último precio
    """
    # Pipeline para obtener los productos más comprados y su frecuencia
    count_pipeline = [
        {"$unwind": "$products"},  # Descompone el array de productos
        {
            "$group": {
                "_id": "$products.producto",
                "count": {"$sum": 1},  # Cuenta las apariciones de cada producto
            }
        },
        {"$sort": {"count": -1}},  # Ordena por frecuencia descendente
        {"$limit": limit}  # Limita a los top N productos
    ]
    
    # Ejecutar el pipeline para obtener los productos más comprados
    top_products = await invoice_collection.aggregate(count_pipeline).to_list(length=None)
    
    # Para cada producto en el top, obtener su último precio
    result = []
    for product in top_products:
        product_name = product["_id"]
        
        # Pipeline para obtener el último precio del producto
        price_pipeline = [
            {"$unwind": "$products"},
            {"$match": {"products.producto": product_name}},
            {"$sort": {"ticket_date": -1}},  # Ordena por fecha descendente
            {"$limit": 1},  # Toma solo el más reciente
            {
                "$project": {
                    "_id": 0,
                    "product": "$products.producto",
                    "last_price": "$products.unitPrice",
                    "last_date": "$ticket_date"
                }
            }
        ]
        
        # Ejecutar el pipeline para el precio del producto actual
        price_info = await invoice_collection.aggregate(price_pipeline).to_list(length=None)
        
        if price_info:
            result.append({
                "product": product_name,
                "count": product["count"],
                "last_price": price_info[0]["last_price"],
                "last_date": price_info[0]["last_date"]
            })
        else:
            # Si no se encontró información de precio (caso raro pero posible)
            result.append({
                "product": product_name,
                "count": product["count"],
                "last_price": None,
                "last_date": None
            })
    
    return result

async def get_latest_invoices(limit: int = 6):
    """
    Obtiene las facturas más recientes
    
    :param limit: Número de facturas a devolver (por defecto 6)
    :return: Lista con las facturas más recientes
    """
    invoices = await invoice_collection.find().sort("ticket_date", -1).limit(limit).to_list(length=None)
    return [invoice_json(invoice) for invoice in invoices]
