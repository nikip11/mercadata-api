
from fastapi import FastAPI, UploadFile, HTTPException
from models.invoice import get_tickets, add_invoice, get_tickets_byDate, get_last_price_of_product
from utils.pdf import extract_table_from_pdf
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
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
