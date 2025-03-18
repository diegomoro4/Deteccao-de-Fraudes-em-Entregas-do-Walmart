import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
def load_data():
    df = pd.read_csv("../data/processed/df_final_walmart.csv")
    return df

df = load_data()

# Configuração do layout
st.set_page_config(page_title="Análise Detalhada de Itens Faltantes", layout="wide")

# Título
st.title("Análise Detalhada de Itens Faltantes 📊")

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
st.markdown("## Tendências Temporais")

# Gráfico 1: Pedidos com Itens Faltantes por Hora do Dia
# Converter delivery_hour para datetime e extrair apenas a hora inteira
df_filtered["delivery_hour"] = pd.to_datetime(df_filtered["delivery_hour"], format="%H:%M:%S", errors="coerce").dt.hour

# Verificar se há dados válidos após a conversão
if df_filtered["delivery_hour"].isnull().all():
    st.error("Não há dados válidos na coluna 'delivery_hour'.")
else:
    # Agrupar os dados por hora inteira
    df_hora = df_filtered.groupby("delivery_hour").agg(
        total_pedidos=("order_id", "count"),
        pedidos_com_faltantes=("order_id", lambda x: (df.loc[x.index, "items_missing"] > 0).sum())
    ).reset_index()

    # Verificar se há dados após o agrupamento
    if df_hora.empty:
        st.warning("Não há dados disponíveis para criar o gráfico.")
    else:
        # Criar gráfico combinado: barras para total de pedidos e linha para pedidos com itens faltantes
        fig_hora = px.bar(
            df_hora,
            x="delivery_hour",
            y="total_pedidos",
            title="Frequência de Pedidos por Hora do Dia com Itens Faltantes",
            labels={"delivery_hour": "Hora do Dia", "total_pedidos": "Número de Pedidos"},
            color_discrete_sequence=["#636EFA"],  # Cor das barras
        )

        # Adicionar linha ao gráfico para representar pedidos com itens faltantes
        fig_hora.add_scatter(
            x=df_hora["delivery_hour"],
            y=df_hora["pedidos_com_faltantes"],
            mode="lines+markers",
            name="Pedidos com Itens Faltantes",
            line=dict(color="#EF553B", width=2),  # Cor e espessura da linha
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig_hora, use_container_width=True)



# Gráfico 2: Pedidos com Itens Faltantes por Dia da Semana

# Definir a ordem dos dias da semana
dias_da_semana = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Agrupar os dados por dia da semana
df_dia = df_filtered.groupby("day_of_week").agg(
    total_pedidos=("order_id", "count"),
    pedidos_com_faltantes=("order_id", lambda x: (df.loc[x.index, "items_missing"] > 0).sum())
).reset_index()

# Ordenar os dados pela ordem dos dias da semana
df_dia["day_of_week"] = pd.Categorical(df_dia["day_of_week"], categories=dias_da_semana, ordered=True)
df_dia = df_dia.sort_values("day_of_week")

# Criar gráfico combinado: barras para total de pedidos e linha para pedidos com itens faltantes
fig_dia = px.bar(
    df_dia,
    x="day_of_week",
    y="total_pedidos",
    title="Frequência de Pedidos por Dia da Semana com Itens Faltantes",
    labels={"day_of_week": "Dia da Semana", "total_pedidos": "Número de Pedidos"},
    color_discrete_sequence=["#636EFA"],  # Cor das barras
)

# Adicionar linha ao gráfico para representar pedidos com itens faltantes
fig_dia.add_scatter(
    x=df_dia["day_of_week"],
    y=df_dia["pedidos_com_faltantes"],
    mode="lines+markers",
    name="Pedidos com Itens Faltantes",
    line=dict(color="#EF553B", width=2),  # Cor e espessura da linha
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_dia, use_container_width=True)


# Gráfico 3: Pedidos com Itens Faltantes por Mês

# Definir a ordem dos meses
meses_do_ano = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Agrupar os dados por mês
df_mes = df_filtered.groupby("month_name").agg(
    total_pedidos=("order_id", "count"),
    pedidos_com_faltantes=("order_id", lambda x: (df.loc[x.index, "items_missing"] > 0).sum())
).reset_index()

# Ordenar os dados pela ordem dos meses do ano
df_mes["month_name"] = pd.Categorical(df_mes["month_name"], categories=meses_do_ano, ordered=True)
df_mes = df_mes.sort_values("month_name")

# Criar gráfico combinado: barras para total de pedidos e linha para pedidos com itens faltantes
fig_mes = px.bar(
    df_mes,
    x="month_name",
    y="total_pedidos",
    title="Frequência de Pedidos por Mês com Itens Faltantes",
    labels={"month_name": "Mês", "total_pedidos": "Número de Pedidos"},
    color_discrete_sequence=["#636EFA"],  # Cor das barras
)

# Adicionar linha ao gráfico para representar pedidos com itens faltantes
fig_mes.add_scatter(
    x=df_mes["month_name"],
    y=df_mes["pedidos_com_faltantes"],
    mode="lines+markers",
    name="Pedidos com Itens Faltantes",
    line=dict(color="#EF553B", width=2),  # Cor e espessura da linha
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_mes, use_container_width=True)

# Seção 2: Perfil de Motoristas e Clientes
st.markdown("## Perfil de Motoristas e Clientes")

# Gráfico 4: Idade do Motorista vs Pedidos com Itens Faltantes

# Agrupar os dados por idade do motorista
df_motorista_idade = df_filtered.groupby("age").agg(
    pedidos_com_faltantes=("order_id", lambda x: (df.loc[x.index, "items_missing"] > 0).sum())
).reset_index()

# Criar gráfico de barras mostrando a relação entre idade do motorista e pedidos com itens faltantes
fig_motorista_idade = px.bar(
    df_motorista_idade,
    x="age",
    y="pedidos_com_faltantes",
    title="Pedidos com Itens Faltantes por Idade dos Motoristas",
    labels={"age": "Idade do Motorista", "pedidos_com_faltantes": "Pedidos com Faltantes"},
    color_discrete_sequence=["#636EFA"]
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_motorista_idade, use_container_width=True)


# Gráfico 5: Idade do Cliente vs Pedidos com Itens Faltantes

# Agrupar os dados por idade do cliente
df_cliente_idade = df_filtered.groupby("customer_age").agg(
    pedidos_com_faltantes=("order_id", lambda x: (df.loc[x.index, "items_missing"] > 0).sum())
).reset_index()

# Criar gráfico de barras mostrando a relação entre idade do cliente e pedidos com itens faltantes
fig_cliente_idade = px.bar(
    df_cliente_idade,
    x="customer_age",
    y="pedidos_com_faltantes",
    title="Pedidos com Itens Faltantes por Idade dos Clientes",
    labels={"customer_age": "Idade do Cliente", "pedidos_com_faltantes": "Pedidos com Faltantes"},
    color_discrete_sequence=["#EF553B"]
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_cliente_idade, use_container_width=True)


# Seção 3: Análise de Categorias e Produtos
st.markdown("## Análise de Categorias e Produtos")

# Função para normalizar as categorias
def normalize_category(category):
    if isinstance(category, str) and category.startswith("["):
        # Extrair a primeira categoria dentro da lista
        category = category.strip("[]").split(",")[0].strip("'").strip()
    if category in ["Supermarket", "Electronics"]:
        return category
    return None  # Ignorar outras categorias

# Aplicar a função na coluna 'category'
df["category_cleaned"] = df["category"].apply(normalize_category)

# Filtrar os dados com base na região selecionada e categorias válidas
df_filtered_categoria = df[df["category_cleaned"].notnull()]
df_filtered_categoria = df_filtered_categoria if selected_region == "Todas" else df_filtered_categoria[df_filtered_categoria["region"] == selected_region]

# Agrupar os dados por categoria limpa e calcular o total de itens faltantes
df_categoria = df_filtered_categoria.groupby("category_cleaned").agg(
    itens_faltantes=("items_missing", "sum")
).reset_index()

# Criar gráfico de barras para as categorias mais associadas a itens faltantes
fig_categoria = px.bar(
    df_categoria,
    x="category_cleaned",
    y="itens_faltantes",
    title=f"Categorias mais Associadas a Itens Faltantes ({selected_region})",
    labels={"category_cleaned": "Categoria", "itens_faltantes": "Itens Faltantes"},
    color="category_cleaned"
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_categoria, use_container_width=True)

# Seção 4: Tamanho do Pedido vs Itens Faltantes
st.markdown("## Tamanho do Pedido vs Itens Faltantes")

# Filtrar os dados com base na região selecionada
df_filtered_tamanho = df if selected_region == "Todas" else df[df["region"] == selected_region]

# Calcular o tamanho do pedido (total de itens)
df_filtered_tamanho["tamanho_pedido"] = df_filtered_tamanho["items_delivered"] + df_filtered_tamanho["items_missing"]

# Agrupar os dados pelo tamanho do pedido e calcular o total de itens faltantes
df_tamanho_pedido = df_filtered_tamanho.groupby("tamanho_pedido").agg(
    itens_faltantes=("items_missing", "sum")
).reset_index()

# Criar gráfico mostrando a relação entre tamanho do pedido e itens faltantes
fig_tamanho_pedido = px.bar(
    df_tamanho_pedido,
    x="tamanho_pedido",
    y="itens_faltantes",
    title=f"Relação entre Tamanho do Pedido e Itens Faltantes ({selected_region})",
    labels={"tamanho_pedido": "Tamanho do Pedido (Número Total de Itens)", "itens_faltantes": "Itens Faltantes"},
    color_discrete_sequence=["#636EFA"]
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_tamanho_pedido, use_container_width=True)
