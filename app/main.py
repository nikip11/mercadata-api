from fastapi import FastAPI, UploadFile, HTTPException
from models.invoice import get_tickets, add_invoice, get_tickets_byDate, get_last_price_of_product, get_totals_by_year, get_top_products, get_latest_invoices
from utils.pdf import extract_table_from_pdf
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
# from utils.gmail import obtener_adjuntos_y_enviar

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/")
async def root():
    return {"message": "¡Hola, Docker con FastAPI y Hot Reload!"}

@app.post("/api/get-ticket/")
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

@app.get("/api/tickets/")
async def get_tickets_all(min = None, max = None):
    try:
        if not min or not max:
            tickets = await get_tickets()
        else:
            tickets = await get_tickets_byDate(min, max)
        return JSONResponse(content={"status": "success", "data": tickets})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# @app.get("/api/mails")
# async def read_mails():
#     try:
#         return JSONResponse(content={"status": "success"}, status_code=200)
#     except Exception as e:
#         return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/product/{product_name}")
async def search_product(product_name: str):
    try:
        print(product_name)
        results = await get_last_price_of_product(product_name)
        print(results)
        if not results:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # 🧪 Formatear fecha a ISO string
        for r in results:
            # if isinstance(r["last_date"], datetime):
            r["last_date"] = r["last_date"].isoformat()

        return JSONResponse(content={"status": "success", "data": results})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar el producto: {str(e)}")

@app.get("/api/tickets/totals/{year}")
async def get_totals(year: int):
    '''
    endpoint recibe un año y devuelve el total mensual de los tickets
    :param year: año a consultar
    :return: JSON con el total mensual de los tickets
    {
        "status": "success",
        "data": {
            "January": 100,
            "February": 200,
            ...
        }
    }
    '''
    print("get_totals", year)
    try:
        data = await get_totals_by_year(year)
        if not data:
            raise HTTPException(status_code=404, detail="No se encontraron datos para el año especificado")
        return JSONResponse(content={"status": "success", "data": data})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/products/top")
async def get_top_consumed_products(limit: int = 10):
    '''
    Endpoint que devuelve los productos más comprados, la cantidad de veces que se han comprado y su último precio
    :param limit: Número de productos a devolver (por defecto 10)
    :return: JSON con los productos más comprados
    {
        "status": "success",
        "data": [
            {
                "product": "Nombre del producto",
                "count": 15,
                "last_price": 2.45,
                "last_date": "2025-05-01T00:00:00"
            },
            ...
        ]
    }
    '''
    try:
        data = await get_top_products(limit)
        if not data:
            raise HTTPException(status_code=404, detail="No se encontraron productos")
        
        # Formatear las fechas a ISO string
        for product in data:
            if product["last_date"] and isinstance(product["last_date"], datetime):
                product["last_date"] = product["last_date"].isoformat()
                
        return JSONResponse(content={"status": "success", "data": data})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/invoices/latest")
async def get_latest_invoices_endpoint(limit: int = 6):
    '''
    Endpoint que devuelve las facturas más recientes
    :param limit: Número de facturas a devolver (por defecto 6)
    :return: JSON con las facturas más recientes
    {
        "status": "success",
        "data": [
            {
                "_id": "...",
                "invoiceId": "...",
                "ticket_date": "2025-05-01T00:00:00",
                "products": [...],
                ...
            },
            ...
        ]
    }
    '''
    try:
        invoices = await get_latest_invoices(limit)
        if not invoices:
            raise HTTPException(status_code=404, detail="No se encontraron facturas")
                
        return JSONResponse(content={"status": "success", "data": invoices})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

