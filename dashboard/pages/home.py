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

# Criar uma função para ajustar cores com base na região selecionada
def ajustar_cores(df, coluna_regiao, regiao_selecionada):
    if regiao_selecionada != "Todas":
        df["opacity"] = df[coluna_regiao].apply(lambda x: 1 if x == regiao_selecionada else 0.5)
    else:
        df["opacity"] = 1
    return df

# Gráfico 1: Total de Pedidos e Total de Pedidos com Itens Faltantes por Região
df_grouped_pedidos = df.groupby("region").agg(
    total_pedidos=("order_id", "count"),
    pedidos_com_faltantes=("order_id", lambda x: (df.loc[x.index, "items_missing"] > 0).sum())
).reset_index()

# Ajustar cores para destacar a região selecionada
df_grouped_pedidos = ajustar_cores(df_grouped_pedidos, "region", selected_region)

fig_pedidos = px.bar(
    df_grouped_pedidos.melt(id_vars=["region", "opacity"], value_vars=["total_pedidos", "pedidos_com_faltantes"]),
    x="region",
    y="value",
    color="variable",
    barmode="group",
    title="Total de Pedidos e Total de Pedidos com Itens Faltantes por Região",
    labels={"region": "Região", "value": "Número de Pedidos", "variable": "Métrica"},
    opacity=df_grouped_pedidos["opacity"],
    text="value"  # Adicionar valores nas barras
)

# Adicionar valores formatados nas barras
fig_pedidos.update_traces(texttemplate="%{text}", textposition="outside")

st.plotly_chart(fig_pedidos, use_container_width=True)

# Gráfico 2: Número de Itens Entregues e Itens Faltantes por Região
df_grouped_itens = df.groupby("region").agg(
    itens_entregues=("items_delivered", "sum"),
    itens_faltantes=("items_missing", "sum")
).reset_index()

# Ajustar cores para destacar a região selecionada
df_grouped_itens = ajustar_cores(df_grouped_itens, "region", selected_region)

fig_itens = px.bar(
    df_grouped_itens.melt(id_vars=["region", "opacity"], value_vars=["itens_entregues", "itens_faltantes"]),
    x="region",
    y="value",
    color="variable",
    barmode="group",
    title="Número de Itens Entregues e Itens Faltantes por Região",
    labels={"region": "Região", "value": "Número de Itens", "variable": "Métrica"},
    opacity=df_grouped_itens["opacity"],
    text="value"  # Adicionar valores nas barras
)    # Adicionar valores formatados nas barras

fig_itens.update_traces(texttemplate="%{text}", textposition="outside")

st.plotly_chart(fig_itens, use_container_width=True)

# Gráfico 3: Impacto Financeiro Comparado com Receita
df_financeiro = df.groupby("region").agg(
    receita_total=("order_amount", "sum"),
    impacto_financeiro=("order_amount", lambda x: (df.loc[x.index, "items_missing"] > 0).sum())
).reset_index()

# Ajustar cores para destacar a região selecionada
df_financeiro = ajustar_cores(df_financeiro, "region", selected_region)

fig_financeiro = px.bar(
    df_financeiro.melt(id_vars=["region", "opacity"], value_vars=["receita_total", "impacto_financeiro"]),
    x="region",
    y="value",
    color="variable",
    barmode="group",
    title="Impacto Financeiro Comparado com Receita por Região",
    labels={"region": "Região", "value": "$ Valor ($)", "variable": "Métrica"},
    opacity=df_financeiro["opacity"],
    text="value"
)

# Adicionar valores nas barras
fig_financeiro.update_traces(texttemplate="$ %{text:.2f}", textposition="outside")

st.plotly_chart(fig_financeiro, use_container_width=True)

# Detalhes da Região Selecionada
if selected_region != "Todas":
    st.markdown(f"### Detalhes da Região Selecionada: {selected_region}")
    
    df_faltantes = df_filtered[df_filtered["items_missing"] > 0]
    
    # Tabela de motoristas com itens faltantes
    st.markdown("#### Motoristas com Itens Faltantes")
    tabela_motoristas = df_faltantes.groupby("driver_name").agg(
        n_pedidos=("order_id", "count"),
        pedidos_com_faltantes=("order_id", "nunique"),
        itens_entregues=("items_delivered", "sum"),
        itens_faltantes=("items_missing", "sum"),
        impacto_financeiro=("order_amount", "sum")
    ).reset_index().sort_values(by="impacto_financeiro", ascending=False)

    tabela_motoristas["taxa_media_faltantes"] = (
        tabela_motoristas["itens_faltantes"] / (tabela_motoristas["itens_entregues"] + tabela_motoristas["itens_faltantes"])
    ).apply(lambda x: f"{x*100:.2f}%")
    
    tabela_motoristas["impacto_financeiro"] = tabela_motoristas["impacto_financeiro"].apply(lambda x: f"$ {x:,.2f}")

    st.dataframe(tabela_motoristas.set_index("driver_name"))

    # Tabela de clientes com itens faltantes
    st.markdown("#### Clientes com Itens Faltantes")
    tabela_clientes = df_faltantes.groupby("customer_name").agg(
        n_pedidos=("order_id", "count"),
        pedidos_com_faltantes=("order_id", "nunique"),
        itens_entregues=("items_delivered", "sum"),
        itens_faltantes=("items_missing", "sum"),
        impacto_financeiro=("order_amount", "sum")
    ).reset_index().sort_values(by="impacto_financeiro", ascending=False)

    tabela_clientes["taxa_media_faltantes"] = (
        tabela_clientes["itens_faltantes"] / (tabela_clientes["itens_entregues"] + tabela_clientes["itens_faltantes"])
    ).apply(lambda x: f"{x*100:.2f}%")
    
    tabela_clientes["impacto_financeiro"] = tabela_clientes["impacto_financeiro"].apply(lambda x: f"$ {x:,.2f}")

    st.dataframe(tabela_clientes.set_index("customer_name"))