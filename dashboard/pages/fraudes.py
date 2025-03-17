import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
def load_data():
    df = pd.read_csv("../data/processed/df_final_walmart.csv")
    return df

df = load_data()

# Configuração do layout
st.set_page_config(page_title="Análise de Fraudes", layout="wide")

# Título
st.title("📊 Análise de Fraudes nas Entregas")

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

# Filtrar apenas pedidos fraudulentos
df_fraudes = df_filtered[df_filtered["fraud_flag"] == 1]

# KPIs
total_fraudes = df_fraudes.shape[0]
percentual_fraude = total_fraudes / df_filtered.shape[0] if df_filtered.shape[0] > 0 else 0
impacto_financeiro = df_fraudes["order_amount"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total de Fraudes", total_fraudes)
col2.metric("Percentual de Fraudes", f"{percentual_fraude:.2%}")
col3.metric("Impacto Financeiro", f"$ {impacto_financeiro:,.2f}")

# Gráfico de Fraudes por Categoria
st.markdown("### Fraudes por Categoria de Produto")
fig_fraudes_categoria = px.bar(
    df_fraudes.groupby("category").size().reset_index(name="total"),
    x="category", y="total", title="Total de Fraudes por Categoria",
    labels={"category": "Categoria", "total": "Número de Fraudes"},
    color="total"
)
st.plotly_chart(fig_fraudes_categoria, use_container_width=True)

# Gráfico de Fraudes por Região
st.markdown("### Distribuição de Fraudes por Região")
fig_fraudes_regiao = px.bar(
    df_fraudes.groupby("region").size().reset_index(name="total"),
    x="region", y="total", title="Total de Fraudes por Região",
    labels={"region": "Região", "total": "Número de Fraudes"},
    color="total"
)
st.plotly_chart(fig_fraudes_regiao, use_container_width=True)

# Tabela de Detalhes
st.markdown("### Detalhamento dos Pedidos Fraudulentos")
df_fraudes_detalhado = df_fraudes[["order_id", "customer_name", "driver_name", "order_amount", "region"]]
st.dataframe(df_fraudes_detalhado)