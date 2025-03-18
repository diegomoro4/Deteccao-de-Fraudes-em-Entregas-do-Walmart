import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
def load_data():
    df = pd.read_csv("../data/processed/df_final_walmart.csv")
    return df

df = load_data()

# Configuração do layout
st.set_page_config(page_title="Análise Detalhada", layout="wide")

# Título
st.title("Análise Detalhada 📊")

# Barra lateral para filtros
st.sidebar.title("Filtros")

# Filtro por região
regioes_ordenadas = sorted(df["region"].unique())
selected_region = st.sidebar.radio(
    "Selecione a Região:", 
    options=["Todas"] + regioes_ordenadas
)

# Aplicar filtro
df_filtered = df if selected_region == "Todas" else df[df["region"] == selected_region]

# Seção 1: Tendências Temporais
st.markdown("### Tendências Temporais")

# Gráfico 1: Número de Pedidos por Mês
fig_pedidos_mes = px.line(
    df_filtered.groupby("month_name").size().reset_index(name="total"),
    x="month_name",
    y="total",
    title="Número de Pedidos por Mês",
    labels={"month_name": "Mês", "total": "Número de Pedidos"}
)
st.plotly_chart(fig_pedidos_mes, use_container_width=True)

# Gráfico 2: Número de Pedidos por Dia da Semana
fig_pedidos_dia = px.bar(
    df_filtered.groupby("day_of_week").size().reset_index(name="total"),
    x="day_of_week",
    y="total",
    title="Número de Pedidos por Dia da Semana",
    labels={"day_of_week": "Dia da Semana", "total": "Número de Pedidos"},
    color="total"
)
st.plotly_chart(fig_pedidos_dia, use_container_width=True)

# Seção 2: Ranking de Motoristas e Clientes
st.markdown("### Rankings")

# Ranking dos Motoristas
motorista_ranking = df_filtered.groupby("driver_name").agg(
    total_pedidos=("order_id", "count"),
    itens_faltantes=("items_missing", "sum"),
).reset_index().sort_values(by="total_pedidos", ascending=False)

st.markdown("#### Motoristas com Mais Entregas")
st.dataframe(motorista_ranking.head(10))

# Ranking dos Clientes
cliente_ranking = df_filtered.groupby("customer_name").agg(
    total_pedidos=("order_id", "count"),
    itens_faltantes=("items_missing", "sum"),
).reset_index().sort_values(by="total_pedidos", ascending=False)

st.markdown("#### Clientes com Mais Pedidos")
st.dataframe(cliente_ranking.head(10))

# Seção 3: Análise de Fraudes
st.markdown("### Análise de Fraudes")

df_fraudes = df_filtered[df_filtered["fraud_flag"] == 1]

# Gráfico 3: Total de Fraudes por Categoria
fig_fraudes_categoria = px.bar(
    df_fraudes.groupby("category").size().reset_index(name="total"),
    x="category",
    y="total",
    title="Total de Fraudes por Categoria",
    labels={"category": "Categoria", "total": "Número de Fraudes"},
    color="total"
)
st.plotly_chart(fig_fraudes_categoria, use_container_width=True)

# Tabela detalhada dos pedidos fraudulentos
st.markdown("#### Detalhes dos Pedidos Fraudulentos")
df_fraudes_detalhado = df_fraudes[["order_id", "customer_name", "driver_name", "order_amount", "region"]]
st.dataframe(df_fraudes_detalhado)
