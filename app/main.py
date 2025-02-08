
from fastapi import FastAPI, UploadFile
from models.invoice import get_invoices, add_invoice
from utils.pdf import extract_table_from_pdf
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "¡Hola, Docker con FastAPI y Hot Reload!"}

@app.post("/get-ticket/")
async def extract_table(file: UploadFile):
    """
    Endpoint para extraer la tabla de un archivo PDF subido.

    :param file: Archivo PDF subido.
    :return: JSON con los productos, el total, la fecha y el total
    """
    try:
        file_location = f"/tmp/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        invoice = extract_table_from_pdf(file_location)
        i = await add_invoice(invoice)
        return JSONResponse(content={"status": "success", "data": i})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/invoices")
async def get_invoices_all():
    try:
        invoices = await get_invoices()
        # return invoices
        return JSONResponse(content={"status": "success", "data": invoices})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
