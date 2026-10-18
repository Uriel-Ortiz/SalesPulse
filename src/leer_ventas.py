import pandas as pd

df = pd.read_csv("data/ventas.csv")

print("=== DATOS DE SALESPULSE ===")
print(df)

print("\n=== RESUMEN ===")
print(f"Registros de venta: {len(df)}")
print(f"Unidades vendidas: {df['unidades'].sum()}")
print(f"Facturación total: ${(df['unidades'] * df['precio']).sum():,.2f}")
print(f"Productos diferentes: {df['producto'].nunique()}")

