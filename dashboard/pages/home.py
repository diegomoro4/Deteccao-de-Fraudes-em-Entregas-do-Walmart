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

# Banner ou imagem
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Walmart_logo.svg/2560px-Walmart_logo.svg.png", width=150)

# Layout do Dashboard
st.title("Visão Geral - Dashboard Walmart")

# Introdução ao Dashboard
st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 18px;">         
        Aqui você encontrará uma análise completa sobre os pedidos realizados, itens entregues e faltantes, além de informações financeiras e operacionais.  
        Use o filtro na barra lateral para explorar os dados por região específica ou visualizar o cenário geral.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

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

st.markdown("---")

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

# Texto explicativo para o gráfico 1
st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 16px;">         
        Este gráfico compara o número total de pedidos realizados com aqueles que apresentaram itens faltantes em cada região.  
        Use o filtro na barra lateral para destacar uma região específica.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

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

st.markdown("---")

# Texto explicativo para o gráfico 2
st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 16px;">         
        Este gráfico mostra a quantidade total de itens entregues com sucesso em comparação aos itens faltantes em cada região.  
        Ele ajuda a identificar áreas que podem ter maior impacto operacional.
    </p>
</div>
""", unsafe_allow_html=True)

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

st.markdown("---")

# Texto explicativo para o gráfico 3
st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 16px;">         
        Este gráfico apresenta uma comparação entre a receita total gerada e o impacto financeiro causado pelos itens faltantes em cada região.  
        Ele destaca as regiões que tiveram maior perda financeira devido a problemas nas entregas.
    </p>
</div>
""", unsafe_allow_html=True)

# Tabela Detalhada por Região
st.markdown("## Ranking das Região com Mais Itens Faltantes")

# Texto explicativo para o gráfico 4
st.markdown(""" * Esta tabela apresenta um ranking das regiões com base no impacto financeiro causado por itens faltantes. """)

# Agrupar os dados por região e calcular as métricas
df_tabela_regiao = df.groupby("region").agg(
    total_pedidos=("order_id", "nunique"),  # Total de pedidos
    produtos_entregues=("items_delivered", "sum"),  # Produtos entregues
    itens_faltantes=("items_missing", "sum"),  # Itens faltantes
    impacto_financeiro=("order_amount", lambda x: (df.loc[x.index, "items_missing"] > 0).sum())  # Impacto financeiro
).reset_index()

# Calcular a taxa média de faltantes
df_tabela_regiao["taxa_media_faltantes"] = (
    df_tabela_regiao["itens_faltantes"] /
    (df_tabela_regiao["produtos_entregues"] + df_tabela_regiao["itens_faltantes"])
) * 100

# Ordenar a tabela pelo impacto financeiro em ordem decrescente
df_tabela_regiao = df_tabela_regiao.sort_values(by="impacto_financeiro", ascending=False)

# Renomear as colunas para exibição mais amigável
df_tabela_regiao.rename(columns={
    "region": "Região",
    "total_pedidos": "Total de Pedidos",
    "produtos_entregues": "Produtos Entregues",
    "taxa_media_faltantes": "Taxa Média de Faltantes (%)",
    "impacto_financeiro": "Valores Perdidos ($)"
}, inplace=True)

# Formatar os valores financeiros como moeda e taxas como porcentagem
df_tabela_regiao["Valores Perdidos ($)"] = df_tabela_regiao["Valores Perdidos ($)"].apply(lambda x: f"$ {x:,.2f}")
df_tabela_regiao["Taxa Média de Faltantes (%)"] = df_tabela_regiao["Taxa Média de Faltantes (%)"].apply(lambda x: f"{x:.2f}%")

# Exibir a tabela no Streamlit
st.dataframe(df_tabela_regiao.set_index("Região"))

st.markdown("---")

# Resumo Final
st.markdown("""
### Resumo Final 
- A região que mais contribuiu para perdas financeiras foi a região **Altamonte Springs**, também associado a 253 itens faltantes.  
- O cliente com mais pedidos foi **Holly Stewart**, com 19 pedidos realizados e 5 itens faltantes.
- O motorista com mais pedidos foi **Jennifer Miller**, com 22 pedidos entregues e 6 itens faltantes.              
- A taxa média de itens faltantes é de **1,63%**, indicando que há espaço para melhorias no processo de entrega.  
""")

st.markdown("---")

st.markdown("""
### Explore Mais
Utilize o menu lateral para acessar análises detalhadas sobre produtos, motoristas e clientes.
""")
