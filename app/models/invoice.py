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