import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import timedelta

st.set_page_config(
    page_title="SalesPulse | Inteligencia Comercial",
    page_icon="📊",
    layout="wide",
)

st.title("📊 SalesPulse")
st.subheader("Panel de inteligencia comercial")
st.caption("Demo empresarial · Datos ficticios")

# Datos de ejemplo

df = pd.read_csv("data/ventas.csv")
df["fecha_hora"] = pd.to_datetime(df["fecha_hora"])
df["fecha"] = df["fecha_hora"].dt.date
df["hora"] = df["fecha_hora"].dt.hour
df["facturacion"] = df["unidades"] * df["precio"]

# Filtros de la barra lateral
st.sidebar.header("Filtros")

# Filtro por categoría
categorias = ["Todas"] + sorted(df["categoria"].unique().tolist())
categoria_seleccionada = st.sidebar.selectbox(
    "Categoría de producto",
    categorias
)

# Filtro por fechas
fecha_min = df["fecha_hora"].min().date()
fecha_max = df["fecha_hora"].max().date()

rango_fechas = st.sidebar.date_input(
    "Período de ventas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max,
)

# Aplicamos los filtros
df_filtrado = df.copy()

if categoria_seleccionada != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["categoria"] == categoria_seleccionada
    ]

# Inicializamos la comparación
variacion_porcentual = None

if len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas

    df_filtrado = df_filtrado[
        (df_filtrado["fecha"] >= fecha_inicio)
        & (df_filtrado["fecha"] <= fecha_fin)
    ]

# Indicadores principales
facturacion_total = df_filtrado["facturacion"].sum()
unidades_totales = df_filtrado["unidades"].sum()
productos_distintos = df_filtrado["producto"].nunique()

# Comparación con el período anterior
if len(rango_fechas) == 2:
    dias_periodo = (fecha_fin - fecha_inicio).days + 1

    fecha_inicio_anterior = fecha_inicio - timedelta(days=dias_periodo)
    fecha_fin_anterior = fecha_inicio - timedelta(days=1)

    df_anterior = df[
        (df["fecha"] >= fecha_inicio_anterior)
        & (df["fecha"] <= fecha_fin_anterior)
    ]

    if categoria_seleccionada != "Todas":
        df_anterior = df_anterior[
            df_anterior["categoria"] == categoria_seleccionada
        ]

    facturacion_anterior = df_anterior["facturacion"].sum()

    if facturacion_anterior > 0:
        variacion_porcentual = (
            (facturacion_total - facturacion_anterior)
            / facturacion_anterior
        ) * 100

col1, col2, col3, col4 = st.columns(4)

if variacion_porcentual is not None:
    col1.metric(
        "Facturación",
        f"${facturacion_total:,.2f}",
        delta=f"{variacion_porcentual:+.2f}%",
        delta_description="vs. período anterior",
    )
else:
    col1.metric(
        "Facturación",
        f"${facturacion_total:,.2f}",
        delta="Sin datos anteriores",
        delta_color="off",
    )
col2.metric("Unidades vendidas", f"{unidades_totales:,}")
col3.metric("Productos diferentes", productos_distintos)

ticket_promedio = (
    facturacion_total / len(df_filtrado)
    if len(df_filtrado) > 0
    else 0
)

col4.metric("Ticket promedio", f"${ticket_promedio:,.2f}")

st.divider()

# Agrupación por producto
resumen = (
    df_filtrado.groupby("producto", as_index=False)["facturacion"]
    .sum()
    .sort_values("facturacion", ascending=False)
)

st.subheader("Facturación por hora y día")

ventas_por_hora = (
    df_filtrado.groupby(["fecha", "hora"], as_index=False)["facturacion"]
    .sum()
    .sort_values(["fecha", "hora"])
)

fig_hora = px.line(
    ventas_por_hora,
    x="hora",
    y="facturacion",
    color="fecha",
    markers=True,
    labels={
        "fecha": "Día del pedido",
        "hora": "Hora del día",
        "facturacion": "Facturación ($)",
    },
)

st.plotly_chart(fig_hora, use_container_width=True)

st.divider()

st.subheader("Evolución de la facturación")

ventas_por_fecha = (
    df_filtrado.groupby("fecha", as_index=False)["facturacion"]
    .sum()
    .sort_values("fecha")
)

fig_fecha = px.line(
    ventas_por_fecha,
    x="fecha",
    y="facturacion",
    markers=True,
    labels={
        "fecha": "Fecha",
        "facturacion": "Facturación ($)",
    },
)

st.plotly_chart(fig_fecha, use_container_width=True)

st.divider()

col_grafico, col_tabla = st.columns([3, 2])

with col_grafico:
    st.subheader("Facturación por producto")
    fig = px.bar(
        resumen,
        x="producto",
        y="facturacion",
        color="facturacion",
        labels={
            "producto": "Producto",
            "facturacion": "Facturación ($)",
        },
        text_auto=".2s",
    )
    st.plotly_chart(fig, use_container_width=True)

with col_tabla:
    st.subheader("Detalle de ventas")
    st.dataframe(
        df_filtrado,
        hide_index=True,
        use_container_width=True,
    )

st.caption("SalesPulse · Proyecto de portafolio con datos ficticios")


