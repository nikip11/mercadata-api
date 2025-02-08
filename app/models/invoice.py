from database import database
from .schema import Ticket

invoice_collection = database.get_collection("invoices_collections")

def invoice_json(invoice: dict) -> dict:
    invoice["_id"] = str(invoice["_id"])
    return invoice

async def add_invoice(invoice_data: Ticket) -> dict:
    check_invoice = await get_one(invoice_data['invoiceId'])
    if check_invoice:
        return check_invoice
    invoice = await invoice_collection.insert_one(invoice_data)
    new_invoice = await invoice_collection.find_one({"_id": invoice.inserted_id})
    return invoice_json(new_invoice)

async def get_invoices():
    invoices = await invoice_collection.find().to_list(200)
    return [invoice_json(ticket) for ticket in invoices]

async def get_one(invoiceId: str):
    invoice = await invoice_collection.find_one({"invoiceId": invoiceId})
    if invoice:
        return invoice_json(invoice)
    return False