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
df["fecha"] = df["fecha_hora"].dt.normalize()
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

    fecha_inicio = pd.Timestamp(fecha_inicio)
    fecha_fin = pd.Timestamp(fecha_fin)

    df_filtrado = df_filtrado[
        (df_filtrado["fecha"] >= fecha_inicio)
        & (df_filtrado["fecha"] < fecha_fin + pd.Timedelta(days=1))
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
        (df["fecha"] >= pd.Timestamp(fecha_inicio_anterior))
        & (df["fecha"] < pd.Timestamp(fecha_inicio))
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
        delta="Sin comparación disponible",
        delta_color="off",
    )

col2.metric("Unidades vendidas", f"{unidades_totales:,}")
col3.metric("Productos diferentes", productos_distintos)

ticket_promedio = (
    facturacion_total / len(df_filtrado)
    if len(df_filtrado) > 0
    else 0
)

col4.metric("Facturación media por registro", f"${ticket_promedio:,.2f}")

st.divider()

# Agrupación por producto
resumen = (
    df_filtrado.groupby("producto", as_index=False)["facturacion"]
    .sum()
    .sort_values("facturacion", ascending=False)
)

st.subheader("Facturación por hora y día")

ventas_por_hora = (
    df_filtrado.groupby("hora", as_index=False)["facturacion"]
    .sum()
    .sort_values("hora")
)

fig_hora = px.bar(
    ventas_por_hora,
    x="hora",
    y="facturacion",
    labels={
        "hora": "Hora del día",
        "facturacion": "Facturación ($)",
    },
)

fig_hora.update_layout(
    template="plotly_dark",
    paper_bgcolor="#14283F",
    plot_bgcolor="#1E3A50",
    font=dict(color="#F2F6FA"),
    colorway=[
        "#55D6BE",
        "#69A7EB",
        "#F2C572",
        "#E58AA8",
        "#B5A0F2",
        "#72D6E8",
        "#F29C75",
    ],
    xaxis=dict(
        title="Hora del día",
        gridcolor="#365267",
        dtick=2,
    ),
    yaxis=dict(
        title="Facturación ($)",
        gridcolor="#365267",
        zerolinecolor="#365267",
    ),
    margin=dict(l=20, r=20, t=30, b=20),
    legend_title_text="Día de venta",
)

fig_hora.update_traces(
    marker_color="#55D6BE",
    marker_line_color="#55D6BE",
    marker_line_width=1,
)

st.plotly_chart(fig_hora, use_container_width=True)

st.divider()

st.subheader("Evolución de la facturación")

ventas_por_fecha = (
    df_filtrado
    .assign(
        semana=pd.to_datetime(df_filtrado["fecha"]).dt.to_period("W").dt.start_time
    )
    .groupby("semana", as_index=False)["facturacion"]
    .sum()
    .sort_values("semana")
)

fig_fecha = px.line(
    ventas_por_fecha,
    x="semana",
    y="facturacion",
    markers=True,
    labels={
        "semana": "Semana",
        "facturacion": "Facturación ($)",
    },
)

fig_fecha.update_traces(
    line=dict(color="#55D6BE", width=3),
    marker=dict(size=8, color="#55D6BE"),
)

fig_fecha.update_layout(
    paper_bgcolor="#14283F",
    plot_bgcolor="#1E3A50",
    font=dict(color="#F2F6FA"),
    xaxis=dict(
        title="Fecha",
        showgrid=False,
    ),
    yaxis=dict(
        title="Facturación ($)",
        gridcolor="#365267",
        zerolinecolor="#365267",
    ),
    margin=dict(l=20, r=20, t=30, b=20),
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

    fig.update_traces(
        marker_color="#55D6BE",
        marker_line_color="#55D6BE",
        marker_line_width=1,
        textfont=dict(color="#F2F6FA"),
    )

    fig.update_layout(
        paper_bgcolor="#14283F",
        plot_bgcolor="#1E3A50",
        font=dict(color="#F2F6FA"),
        xaxis=dict(
            title="Producto",
            showgrid=False,
        ),
        yaxis=dict(
            title="Facturación ($)",
            gridcolor="#365267",
            zerolinecolor="#365267",
        ),
        margin=dict(l=20, r=20, t=30, b=20),
    )

    st.plotly_chart(fig, use_container_width=True)

with col_tabla:
    st.subheader("Detalle de ventas")

    st.dataframe(
        df_filtrado,
        hide_index=True,
        use_container_width=True,
        height=400,
        column_order=[
            "fecha_hora",
            "producto",
            "categoria",
            "unidades",
            "precio",
            "facturacion",
        ],
        column_config={
            "fecha_hora": st.column_config.DatetimeColumn(
                "Fecha y hora",
                format="DD/MM/YYYY HH:mm",
            ),
            "producto": st.column_config.TextColumn("Producto"),
            "categoria": st.column_config.TextColumn("Categoría"),
            "unidades": st.column_config.NumberColumn(
                "Unidades",
                format="%d",
            ),
            "precio": st.column_config.NumberColumn(
                "Precio",
                format="$ %.2f",
            ),
            "facturacion": st.column_config.NumberColumn(
                "Facturación",
                format="$ %.2f",
            ),
        },
    )

st.divider()
st.caption("SalesPulse · Proyecto de portafolio con datos ficticios")
