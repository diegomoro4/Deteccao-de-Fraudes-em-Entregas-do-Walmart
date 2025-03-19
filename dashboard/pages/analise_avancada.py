import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
def load_data():
    df = pd.read_csv("../data/processed/df_final_walmart.csv")
    return df

df = load_data()

# Configuração do layout
st.set_page_config(page_title="Análise Detalhada: Motoristas e Clientes", layout="wide")

# Título
st.title("Análise Detalhada: Motoristas e Clientes 📊")

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

# Seção 1: KPIs Gerais
st.markdown("## KPIs Gerais")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Reclamação Média dos Motoristas", f"{df_filtered['driver_complaint_rate'].mean():.2%}")
col2.metric("Reclamação Média dos Clientes", f"{df_filtered['customer_complaint_rate'].mean():.2%}")
col3.metric("Total de Viagens (Motoristas)", df_filtered["driver_recurrence"].sum())
col4.metric("Total de Pedidos (Clientes)", df_filtered["customer_recurrence"].sum())

# Seção 2: Idade x Taxa Média de Pedidos com Faltantes
st.markdown("## Idade vs Taxa Média de Pedidos com Faltantes")

# Gráfico 1: Idade do Motorista vs Taxa Média de Pedidos com Faltantes e Sem Faltantes
df_motorista_idade = df_filtered.groupby("age").agg(
    total_pedidos=("order_id", "count"),
    pedidos_com_faltantes=("order_id", lambda x: (df.loc[x.index, "items_missing"] > 0).sum())
).reset_index()

# Calcular taxas médias
df_motorista_idade["taxa_com_faltantes"] = df_motorista_idade["pedidos_com_faltantes"] / df_motorista_idade["total_pedidos"]
df_motorista_idade["taxa_sem_faltantes"] = 1 - df_motorista_idade["taxa_com_faltantes"]  # Complemento da taxa

# Criar gráfico de barras agrupadas
fig_motorista_idade = px.bar(
    df_motorista_idade.melt(id_vars="age", value_vars=["taxa_com_faltantes", "taxa_sem_faltantes"]),
    x="age",
    y="value",
    color="variable",
    barmode="group",
    title="Taxa Média de Pedidos por Idade dos Motoristas (Com e Sem Itens Faltantes)",
    labels={"age": "Idade do Motorista", "value": "Taxa Média (%)", "variable": "Métrica"},
    color_discrete_map={
        "taxa_com_faltantes": "#EF553B",  # Cor para taxa média de pedidos com itens faltantes
        "taxa_sem_faltantes": "#636EFA"   # Cor para taxa média de pedidos sem itens faltantes
    }
)
st.plotly_chart(fig_motorista_idade, use_container_width=True)

# Gráfico 2: Idade do Cliente vs Taxa Média de Pedidos com Faltantes e Sem Faltantes
df_cliente_idade = df_filtered.groupby("customer_age").agg(
    total_pedidos=("order_id", "count"),
    pedidos_com_faltantes=("order_id", lambda x: (df.loc[x.index, "items_missing"] > 0).sum())
).reset_index()

# Calcular taxas médias
df_cliente_idade["taxa_com_faltantes"] = df_cliente_idade["pedidos_com_faltantes"] / df_cliente_idade["total_pedidos"]
df_cliente_idade["taxa_sem_faltantes"] = 1 - df_cliente_idade["taxa_com_faltantes"]  # Complemento da taxa

# Criar gráfico de barras agrupadas
fig_cliente_idade = px.bar(
    df_cliente_idade.melt(id_vars="customer_age", value_vars=["taxa_com_faltantes", "taxa_sem_faltantes"]),
    x="customer_age",
    y="value",
    color="variable",
    barmode="group",
    title="Taxa Média de Pedidos por Idade dos Clientes (Com e Sem Itens Faltantes)",
    labels={"customer_age": "Idade do Cliente", "value": "Taxa Média (%)", "variable": "Métrica"},
    color_discrete_map={
        "taxa_com_faltantes": "#EF553B",  # Cor para taxa média de pedidos com itens faltantes
        "taxa_sem_faltantes": "#636EFA"   # Cor para taxa média de pedidos sem itens faltantes
    }
)
st.plotly_chart(fig_cliente_idade, use_container_width=True)

# Seção 4: Top 10 Motoristas e Clientes por Perda Financeira
st.markdown(f"### Detalhes da Região Selecionada: {selected_region}")
st.markdown("## Top 10 Motoristas e Clientes por Perda Financeira")
    
df_faltantes = df_filtered[df_filtered["items_missing"] > 0]

# Tabela de motoristas com itens faltantes
st.markdown("### Motoristas")
tabela_motoristas = df_faltantes.groupby("driver_name").agg(
    n_pedidos=("order_id", "count"),
    pedidos_com_faltantes=("order_id", "nunique"),
    itens_entregues=("items_delivered", "sum"),
    itens_faltantes=("items_missing", "sum"),
    perda_financeira=("order_amount", "sum")
).reset_index().sort_values(by="perda_financeira", ascending=False)

tabela_motoristas["taxa_media_faltantes"] = (
    tabela_motoristas["itens_faltantes"] / (tabela_motoristas["itens_entregues"] + tabela_motoristas["itens_faltantes"])
).apply(lambda x: f"{x*100:.2f}%")

tabela_motoristas["perda_financeira"] = tabela_motoristas["perda_financeira"].apply(lambda x: f"$ {x:,.2f}")

st.dataframe(tabela_motoristas.set_index("driver_name"))

# Tabela de clientes com itens faltantes
st.markdown("### Clientes")
tabela_clientes = df_faltantes.groupby("customer_name").agg(
    n_pedidos=("order_id", "count"),
    pedidos_com_faltantes=("order_id", "nunique"),
    itens_entregues=("items_delivered", "sum"),
    itens_faltantes=("items_missing", "sum"),
    perda_financeira=("order_amount", "sum")
).reset_index().sort_values(by="perda_financeira", ascending=False)

tabela_clientes["taxa_media_faltantes"] = (
    tabela_clientes["itens_faltantes"] / (tabela_clientes["itens_entregues"] + tabela_clientes["itens_faltantes"])
).apply(lambda x: f"{x*100:.2f}%")

tabela_clientes["perda_financeira"] = tabela_clientes["perda_financeira"].apply(lambda x: f"$ {x:,.2f}")

st.dataframe(tabela_clientes.set_index("customer_name"))