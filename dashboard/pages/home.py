import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
def load_data():
    df = pd.read_csv("../data/processed/df_final_walmart.csv")
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

# KPIs Gerais
total_pedidos = df_filtered["order_id"].nunique()
total_produtos_entregues = df_filtered["items_delivered"].sum()
total_pedidos_faltantes = df_filtered[df_filtered["items_missing"] > 0]["order_id"].nunique()
total_itens_faltantes = df_filtered["items_missing"].sum()
impacto_financeiro = df_filtered[df_filtered["items_missing"] > 0]["order_amount"].sum()

# Corrigir taxa média de faltantes
total_itens = total_produtos_entregues + total_itens_faltantes
taxa_media_faltantes = (total_itens_faltantes / total_itens) if total_itens > 0 else 0

# Motorista com mais entregas
motorista_top = (
    df_filtered.groupby("driver_name")
    .agg(total_pedidos=("order_id", "count"), itens_faltantes=("items_missing", "sum"))
    .reset_index()
    .sort_values(by="total_pedidos", ascending=False)
    .iloc[0]
)

# Cliente com mais pedidos
cliente_top = (
    df_filtered.groupby("customer_name")
    .agg(total_pedidos=("order_id", "count"), itens_faltantes=("items_missing", "sum"))
    .reset_index()
    .sort_values(by="total_pedidos", ascending=False)
    .iloc[0]
)

# Layout do Dashboard
st.title("Visão Geral - Dashboard Walmart")

# KPIs Principais
st.markdown("#### Indicadores-Chave de Desempenho (KPIs)")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de Pedidos", total_pedidos)
col2.metric("Pedidos com Faltantes", total_pedidos_faltantes)
col3.metric("Itens Faltantes", total_itens_faltantes)
col4.metric("Taxa Média de Faltantes", f"{taxa_media_faltantes:.2%}")
col5.metric("Produtos Entregues", total_produtos_entregues)

# Segunda linha com três colunas
col6, col7, col8 = st.columns(3)
col6.metric(
    f"Motorista Top: {motorista_top['driver_name']}",
    f"Pedidos: {motorista_top['total_pedidos']}",
    f"Itens Faltantes: {motorista_top['itens_faltantes']}"
)
col7.metric(
    f"Cliente Top: {cliente_top['customer_name']}",
    f"Pedidos: {cliente_top['total_pedidos']}",
    f"Itens Faltantes: {cliente_top['itens_faltantes']}"
)
col8.metric("Impacto Financeiro", f"$ {impacto_financeiro:,.2f}")

# Gráficos por Região
st.markdown("### Análise por Região")
col1, col2 = st.columns(2)

fig_total_pedidos = px.bar(
    df.groupby("region").agg(total_pedidos=("order_id", "count")).reset_index(),
    x="region", y="total_pedidos", title="Total de Pedidos por Região",
    labels={"region": "Região", "total_pedidos": "Total de Pedidos"},
    color="total_pedidos"
)
col1.plotly_chart(fig_total_pedidos, use_container_width=True)

fig_taxa_faltantes = px.bar(
    df[df["items_missing"] > 0]
    .groupby("region")
    .agg(taxa_media=("missing_rate", "mean"))
    .reset_index(),
    x="region",
    y="taxa_media",
    title="Taxa Média de Produtos Faltantes por Região",
    labels={"region": "Região", "taxa_media": "Taxa Média"},
    color="taxa_media"
)

col2.plotly_chart(fig_taxa_faltantes, use_container_width=True)

# Detalhes da Região Selecionada
if selected_region != "Todas":
    st.markdown(f"### Detalhes da Região Selecionada: {selected_region}")
    df_faltantes = df_filtered[df_filtered["items_missing"] > 0]
    
    tabela_detalhada = df_faltantes.groupby("driver_name").agg(
        n_pedidos=("order_id", "count"),
        pedidos_com_faltantes=("order_id", "nunique"),
        itens_entregues=("items_delivered", "sum"),
        itens_faltantes=("items_missing", "sum"),
        impacto_financeiro=("order_amount", "sum")
    ).reset_index().sort_values(by="impacto_financeiro", ascending=False)

    tabela_detalhada["taxa_media_faltantes"] = (
        tabela_detalhada["itens_faltantes"] / (tabela_detalhada["itens_entregues"] + tabela_detalhada["itens_faltantes"])
    ).apply(lambda x: f"{x*100:.2f}%")
    
    tabela_detalhada["impacto_financeiro"] = tabela_detalhada["impacto_financeiro"].apply(lambda x: f"$ {x:,.2f}")

    st.dataframe(tabela_detalhada.set_index("driver_name"))
