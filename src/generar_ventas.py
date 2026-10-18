import csv
import random
from datetime import date, datetime, time, timedelta
from pathlib import Path

# Para obtener los mismos datos en cada ejecución.
random.seed(42)

# Productos, categorías, precios y popularidad.
productos = {
    "Teclado": ("Perifericos", 35.00, 15),
    "Mouse": ("Perifericos", 18.00, 20),
    "Monitor": ("Pantallas", 220.00, 8),
    "Auriculares": ("Audio", 45.00, 12),
    "Webcam": ("Accesorios", 60.00, 7),
    "Microfono": ("Audio", 85.00, 6),
    "Disco SSD": ("Almacenamiento", 95.00, 9),
    "Memoria RAM": ("Componentes", 75.00, 8),
    "Parlantes": ("Audio", 55.00, 7),
    "Mousepad": ("Perifericos", 12.00, 10),
}

# Período de ventas: abril hasta mediados de octubre de 2026.
fecha_inicio = date(2026, 4, 1)
fecha_fin = date(2026, 10, 15)

fechas = [
    fecha_inicio + timedelta(days=i)
    for i in range((fecha_fin - fecha_inicio).days + 1)
]

def generar_venta(fecha):
    """Genera una venta ficticia para una fecha determinada."""

    nombres = list(productos.keys())
    pesos = [productos[nombre][2] for nombre in nombres]
    producto = random.choices(nombres, weights=pesos, k=1)[0]

    categoria, precio, _ = productos[producto]

    hora = random.choices(
        range(9, 21),
        weights=[3, 5, 6, 7, 6, 5, 5, 6, 8, 7, 4, 2],
        k=1,
    )[0]

    fecha_hora = datetime.combine(
        fecha,
        time(hora, random.randint(0, 59)),
    )

    unidades = random.choices(
        range(1, 9),
        weights=[20, 20, 16, 12, 10, 8, 5, 3],
        k=1,
    )[0]

    return {
        "fecha_hora": fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
        "producto": producto,
        "categoria": categoria,
        "unidades": unidades,
        "precio": f"{precio:.2f}",
    }


# Creamos al menos una venta por cada día.
ventas = [generar_venta(fecha) for fecha in fechas]

# Completamos hasta llegar a 500 ventas.
pesos_fechas = [
    1.0 if fecha.weekday() < 5 else 0.55
    for fecha in fechas
]

while len(ventas) < 500:
    fecha = random.choices(
        fechas,
        weights=pesos_fechas,
        k=1,
    )[0]
    ventas.append(generar_venta(fecha))

# Ordenamos las ventas cronológicamente.
ventas.sort(key=lambda venta: venta["fecha_hora"])

# Guardamos el CSV en la carpeta data.
ruta_csv = Path(__file__).resolve().parent.parent / "data" / "ventas.csv"

with ruta_csv.open("w", newline="", encoding="utf-8") as archivo:
    columnas = ["fecha_hora", "producto", "categoria", "unidades", "precio"]
    escritor = csv.DictWriter(archivo, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(ventas)

print(f"Ventas generadas: {len(ventas)}")
print(f"Período: {fecha_inicio} a {fecha_fin}")
print(f"Archivo guardado en: {ruta_csv}")
