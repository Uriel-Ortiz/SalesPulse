import pandas as pd

# Datos ficticios de ventas de una tienda online
# Este script calcula indicadores comerciales y facturacion por producto.
ventas = [
    {"producto": "Teclado", "categoria": "Perifericos", "unidades": 12, "precio": 35.00},
    {"producto": "Mouse", "categoria": "Perifericos", "unidades": 20, "precio": 18.00},
    {"producto": "Monitor", "categoria": "Pantallas", "unidades": 5, "precio": 220.00},
    {"producto": "Auriculares", "categoria": "Audio", "unidades": 8, "precio": 45.00},
    {"producto": "Webcam", "categoria": "Accesorios", "unidades": 7, "precio": 60.00},
    {"producto": "Teclado", "categoria": "Perifericos", "unidades": 6, "precio": 35.00},
    {"producto": "Monitor", "categoria": "Pantallas", "unidades": 3, "precio": 220.00},
]

# Convertimos los datos en una tabla de Pandas
df = pd.DataFrame(ventas)

# Calculamos la facturacion por producto vendido
df["facturacion"] = df["unidades"] * df["precio"]

# Calculamos indicadores comerciales
facturacion_total = df["facturacion"].sum()
unidades_totales = df["unidades"].sum()

# Agrupamos las ventas por producto
resumen_productos = (
    df.groupby("producto")["facturacion"]
    .sum()
    .sort_values(ascending=False)
)

# Mostramos los resultados
print("\n=== SALESPULSE: INFORME DE VENTAS ===")
print(f"Facturacion total: ${facturacion_total:,.2f}")
print(f"Unidades vendidas: {unidades_totales}")

print("\nFacturacion por producto:")
print(resumen_productos.to_string())

