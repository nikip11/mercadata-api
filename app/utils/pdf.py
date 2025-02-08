from PyPDF2 import PdfReader
import re

def extract_table_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Patrón para capturar el ID de la factura
    pattern = r"FACTURA SIMPLIFICADA:\s*(\d{4}-\d{3}-\d{6})"

    match = re.search(pattern, text)
    factura_id = match.group(1) if match else "ID no encontrado"

    date_match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    ticket_date = date_match.group(1) if date_match else ""

    # Buscar el total del ticket
    total_match = re.search(r"TOTAL \(\€\)\s*([\d,]+)", text)
    total_ticket = total_match.group(1) if total_match else "0"

    lines = get_lines(text)

    products = []
    total = 0
    
    for line in lines:
        pattern = r"^(\d+)\s*([A-ZÁÉÍÓÚÑa-záéíóúñ0-9\s\./%&\+\-]+)(?:\s*([\d,]+)\s*kg)?(?:\s*([\d,]+) €/kg)?(?:\s+([\d,]+))?(?:\s+([\d,]+))?$"
        match = re.search(pattern, line.strip())
        
        if match:
            cantidad = match.group(1)
            producto = match.group(2).strip()
            peso = match.group(3) if match.group(3) else "N/A"
            precio_unitario = match.group(5) if match.group(5) else "N/A"
            precio_por_kg = match.group(4) if match.group(4) else "N/A"
            precio_total = match.group(6) if match.group(6) else precio_unitario

            products.append({"cantidad": cantidad, "producto": producto, "precioPorKg": precio_por_kg, "peso": peso, "precio": precio_total})
            if precio_total:
                total = total + float(precio_total.replace(",", "."))
        else:
            print("=> match fail", line)
    return {'products': products, 'ticket_date': ticket_date, 'total': total_ticket, 'totalCalc': total, 'invoiceId': factura_id}

def get_lines(text):
    text = re.split(r"Descripción P\. Unit Importe", text, maxsplit=1)[-1]
    text = re.split(r"TOTAL \(\€\)", text, maxsplit=1)[0]
    # Paso 1: Dividir en líneas
    lines = text.split('\n')

    # Paso 2: Limpiar líneas vacías o irrelevantes
    lines = [line.strip() for line in lines if line.strip()]

    # Paso 3: Combinar líneas partidas
    combined_lines = []
    skip_next = False

    for i in range(len(lines) - 1):
        if skip_next:
            skip_next = False
            continue
        
        current_line = lines[i]
        next_line = lines[i + 1]
        
        # Detectar si la línea actual necesita la siguiente (por kg o precio)
        if re.match(r".*\d+,\d+\s*kg\s*\d+,\d+ €/kg", next_line):
            combined_lines.append(current_line + " " + next_line)
            skip_next = True
        else:
            combined_lines.append(current_line)

    if not skip_next:
        combined_lines.append(lines[-1])  # Añadir la última línea si no fue procesada

    return combined_lines

