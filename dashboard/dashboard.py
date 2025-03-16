import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar os dados
def load_data():
    df = pd.read_csv("data/processed/df_final_walmart.csv")
    return df

df = load_data()

# Configuração do layout do Streamlit
st.set_page_config(page_title="Dashboard Walmart", layout="wide")

# Barra lateral para filtros
st.sidebar.title("Filtros")

# Ordenar as regiões em ordem alfabética
regioes_ordenadas = sorted(df["region"].unique())

# Criar botões de seleção para regiões (exibição vertical)
selected_region = st.sidebar.radio(
    "Selecione a Região:", 
    options=["Todas"] + regioes_ordenadas
)

# Filtrar os dados com base na região selecionada
df_filtered = df if selected_region == "Todas" else df[df["region"] == selected_region]

# KPIs Gerais (para todas as regiões ou região selecionada)
total_pedidos = df_filtered["order_id"].nunique()
total_pedidos_faltantes = df_filtered[df_filtered["items_missing"] > 0]["order_id"].nunique()
taxa_media_faltantes = df_filtered["missing_rate"].mean()

# Motorista com mais entregas na região selecionada
motorista_top = (
    df_filtered.groupby("driver_name")
    .agg(total_pedidos=("order_id", "count"), itens_faltantes=("items_missing", "sum"))
    .reset_index()
    .sort_values(by="total_pedidos", ascending=False)
    .iloc[0]
)

# Cliente que mais recebeu pedidos na região selecionada
cliente_top = (
    df_filtered.groupby("customer_name")
    .agg(total_pedidos=("order_id", "count"), itens_faltantes=("items_missing", "sum"))
    .reset_index()
    .sort_values(by="total_pedidos", ascending=False)
    .iloc[0]
)

# Impacto financeiro (exemplo: soma dos valores dos pedidos com itens faltantes)
impacto_financeiro = df_filtered[df_filtered["items_missing"] > 0]["order_amount"].sum()

# Layout do Dashboard
st.title("Visão Geral - Dashboard Walmart")

# KPIs Principais
st.markdown("#### Indicadores-Chave de Desempenho (KPIs)")

# Primeira linha com três colunas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Pedidos", total_pedidos)
col2.metric("Pedidos c/ Faltantes", total_pedidos_faltantes)
col3.metric("(%) Itens Faltantes", f"{taxa_media_faltantes:.2%}")

# Segunda linha com duas colunas
col4, col5 = st.columns(2)
col4.metric(
    f"Motorista Top: {motorista_top['driver_name']}",
    f"Pedidos: {motorista_top['total_pedidos']}",
    f"Itens Faltantes: {motorista_top['itens_faltantes']}",
)
col5.metric(
    f"Cliente Top: {cliente_top['customer_name']}",
    f"Pedidos: {cliente_top['total_pedidos']}",
    f"Itens Faltantes: {cliente_top['itens_faltantes']}",
)

# Gráficos por Região
st.markdown("### Análise por Região")
col1, col2 = st.columns(2)

# Gráfico 1: Total de Pedidos por Região
fig_total_pedidos = px.bar(
    df.groupby("region").agg(total_pedidos=("order_id", "count")).reset_index(),
    x="region",
    y="total_pedidos",
    title="Total de Pedidos por Região",
    labels={"region": "Região", "total_pedidos": "Total de Pedidos"},
    color="total_pedidos",
)
col1.plotly_chart(fig_total_pedidos, use_container_width=True)

# Gráfico 2: Taxa Média de Produtos Faltantes por Região
fig_taxa_faltantes = px.bar(
    df.groupby("region").agg(taxa_media=("missing_rate", "mean")).reset_index(),
    x="region",
    y="taxa_media",
    title="Taxa Média de Produtos Faltantes por Região",
    labels={"region": "Região", "taxa_media": "Taxa Média"},
    color="taxa_media",
)
col2.plotly_chart(fig_taxa_faltantes, use_container_width=True)

# Detalhes da Região Selecionada
if selected_region != "Todas":
    st.markdown(f"### Detalhes da Região Selecionada: {selected_region}")
    
    # Filtrar pedidos com itens faltantes
    df_faltantes = df_filtered[df_filtered["items_missing"] > 0]
    
    # Tabela detalhada para a região selecionada, ordenada pelo maior impacto financeiro
    tabela_detalhada = df_faltantes.groupby(["driver_name"]).agg(
        total_entregas=("order_id", "count"),
        itens_faltantes=("items_missing", "sum"),
        taxa_media_faltantes=("missing_rate", "mean"),
        impacto_financeiro=("order_amount", "sum")  # Soma apenas dos pedidos com itens faltantes
    ).reset_index().sort_values(by="impacto_financeiro", ascending=False)
    
    st.dataframe(tabela_detalhada.head(10))



