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

# Banner ou imagem
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Walmart_logo.svg/2560px-Walmart_logo.svg.png", width=150)

# Título
st.title("Análise Detalhada de Itens Faltantes")

# Introdução ao Dashboard
st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 16px;">         
        Esta página apresenta uma análise detalhada sobre os itens faltantes nas entregas realizadas pelo Walmart.  
        Aqui você encontrará informações sobre categorias de produtos, tendências temporais e tamanho dos pedidos.  
        Use o filtro na barra lateral para explorar os dados por região específica ou visualizar o cenário geral.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

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

# Seção 1: KPIs Resumidos
st.markdown("### Indicadores-Chave de Desempenho (KPIs)")

# Linha 1: Pedidos fraudulentos e itens faltantes (%)
col1, col2, col3 = st.columns(3)

# Número de pedidos fraudulentos
fraudes_totais = df_filtered_categoria[df_filtered_categoria["fraud_flag"] == 1]["order_id"].nunique()
col1.metric("Pedidos Fraudulentos", fraudes_totais)

# Número de itens faltantes por categoria (com percentual)
itens_faltantes_categoria = df_filtered_categoria.groupby("category_cleaned").agg(
    total_itens_faltantes=("items_missing", "sum"),
    total_itens=("items_delivered", "sum")
).reset_index()
itens_faltantes_categoria["percentual_faltantes"] = (
    itens_faltantes_categoria["total_itens_faltantes"] /
    (itens_faltantes_categoria["total_itens_faltantes"] + itens_faltantes_categoria["total_itens"])
) * 100

supermarket_percentual = itens_faltantes_categoria.loc[itens_faltantes_categoria["category_cleaned"] == "Supermarket", "percentual_faltantes"]
electronics_percentual = itens_faltantes_categoria.loc[itens_faltantes_categoria["category_cleaned"] == "Electronics", "percentual_faltantes"]

col2.metric(
    "Itens Faltantes (%) (Supermarket)", 
    f"{supermarket_percentual.values[0]:.2f}%" if not supermarket_percentual.empty else "0%"
)
col3.metric(
    "Itens Faltantes (%) (Electronics)", 
    f"{electronics_percentual.values[0]:.2f}%" if not electronics_percentual.empty else "0%"
)

# Linha 2: Produtos mais reportados
# Função para limpar os nomes dos produtos (remover colchetes e aspas)
def clean_product_name(product_name):
    if isinstance(product_name, str):
        return product_name.strip("[]").replace("'", "").replace('"', "").strip()
    return product_name

# Agrupar os dados por categoria e produto, calcular o número de vezes que cada produto foi reportado como faltante
produto_por_categoria = df_filtered_categoria.groupby(["category_cleaned", "product_name"]).agg(
    vezes_reportado=("items_missing", "sum")  # Soma do número de itens faltantes
).reset_index()

# Limpar os nomes dos produtos
produto_por_categoria["product_name"] = produto_por_categoria["product_name"].apply(clean_product_name)

# Identificar o produto mais reportado por categoria
produto_supermarket = produto_por_categoria[produto_por_categoria["category_cleaned"] == "Supermarket"].sort_values(
    by="vezes_reportado", ascending=False).iloc[0]
produto_electronics = produto_por_categoria[produto_por_categoria["category_cleaned"] == "Electronics"].sort_values(
    by="vezes_reportado", ascending=False).iloc[0]

# Exibir os KPIs para produtos mais reportados
col4, col5 = st.columns(2)

col4.metric(
    f"Produto Mais Reportado (Supermarket)",
    f"{produto_supermarket['product_name']}",
    f"Vezes Reportado: {produto_supermarket['vezes_reportado']}"
)

col5.metric(
    f"Produto Mais Reportado (Electronics)",
    f"{produto_electronics['product_name']}",
    f"Vezes Reportado: {produto_electronics['vezes_reportado']}"
)

st.markdown("---")

# Seção 2: Análise de Categorias e Produtos
st.markdown("## Análise de Categorias e Produtos")

# Aplicar a função na coluna 'category'
df["category_cleaned"] = df["category"].apply(normalize_category)

# Filtrar os dados com base na região selecionada e categorias válidas
df_filtered_categoria = df[df["category_cleaned"].notnull()]
df_filtered_categoria = df_filtered_categoria if selected_region == "Todas" else df_filtered_categoria[df_filtered_categoria["region"] == selected_region]

# Agrupar os dados por categoria limpa e calcular o total de itens faltantes e impacto financeiro
df_categoria = df_filtered_categoria.groupby("category_cleaned").agg(
    itens_faltantes=("items_missing", "sum"),
    impacto_financeiro=("order_amount", "sum")  # Soma do valor financeiro por categoria
).reset_index()

# Criar gráfico de barras para as categorias mais associadas a itens faltantes
fig_categoria = px.bar(
    df_categoria,
    x="category_cleaned",
    y="itens_faltantes",
    title=f"Categorias mais Associadas a Itens Faltantes ({selected_region})",
    labels={"category_cleaned": "Categoria", "itens_faltantes": "Itens Faltantes"},
    color="category_cleaned",
    text="impacto_financeiro"  # Adicionar valores financeiros diretamente nas barras
)

# Formatando os valores financeiros exibidos nas barras
fig_categoria.update_traces(
    texttemplate="$ %{text:,.2f}",  # Formatar como valores monetários
    textposition="outside"         # Exibir os valores fora das barras
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_categoria, use_container_width=True)

st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 16px;">         
        Este gráfico apresenta as categorias mais associadas a itens faltantes, juntamente com o impacto financeiro causado por esses problemas.  
        Use o filtro na barra lateral para explorar os dados por região específica.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 3: Tendências Temporais
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

st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 16px;">         
        Este gráfico mostra como os pedidos com itens faltantes variam ao longo do dia.  
        Identificar padrões temporais pode ajudar a otimizar processos logísticos.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

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

st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 16px;">         
        Este gráfico apresenta a frequência de pedidos com itens faltantes ao longo da semana.  
        Ele ajuda a identificar dias críticos que podem exigir atenção especial.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

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

st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 16px;">         
        Este gráfico mostra como os pedidos com itens faltantes variam ao longo dos meses.  
        Ele ajuda a identificar períodos sazonais que podem estar associados a problemas nas entregas.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 3: Tamanho do Pedido vs Itens Faltantes
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

st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 16px;">         
        Este gráfico apresenta a relação entre o tamanho dos pedidos e os itens faltantes.  
        Pedidos maiores podem estar associados a maior probabilidade de problemas.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seção 5: Tabelas Detalhadas de Produtos por Categoria
st.markdown("## Tabelas Detalhadas de Produtos por Categoria")

st.markdown("""
* As tabelas abaixo destacam os produtos mais associados a problemas nas categorias Supermarket e Electronics.  
* Os produtos estão ordenados por quantidade de itens faltantes e impacto financeiro.
""")

# Função para limpar os nomes dos produtos (remover colchetes e aspas)
def clean_product_name(product_name):
    if isinstance(product_name, str):
        return product_name.strip("[]").replace("'", "").replace('"', "").strip()
    return product_name

# Aplicar a função na coluna 'product_name' para limpar os nomes dos produtos
df_filtered_categoria["product_name_cleaned"] = df_filtered_categoria["product_name"].apply(clean_product_name)

# Agrupar os dados por nome do produto e categoria, calcular as métricas
df_tabela_produtos = df_filtered_categoria.groupby(["product_name_cleaned", "category_cleaned"]).agg(
    quantidade_pedidos=("order_id", "count"),  # Número de pedidos
    quantidade_faltantes=("items_missing", "sum"),  # Soma dos itens faltantes
    valor_financeiro=("order_amount", "sum")  # Soma do valor financeiro
).reset_index()

# Separar as tabelas por categoria
df_supermarket = df_tabela_produtos[df_tabela_produtos["category_cleaned"] == "Supermarket"].sort_values(
    by=["quantidade_faltantes", "valor_financeiro"], ascending=False
)

df_electronics = df_tabela_produtos[df_tabela_produtos["category_cleaned"] == "Electronics"].sort_values(
    by=["quantidade_faltantes", "valor_financeiro"], ascending=False
)

# Formatar os valores financeiros como moeda
df_supermarket["valor_financeiro"] = df_supermarket["valor_financeiro"].apply(lambda x: f"$ {x:,.2f}")
df_electronics["valor_financeiro"] = df_electronics["valor_financeiro"].apply(lambda x: f"$ {x:,.2f}")

# Exibir a tabela para Supermarket
st.markdown("### Supermarket")
st.dataframe(df_supermarket.set_index("product_name_cleaned").rename(columns={
    "category_cleaned": "Categoria",
    "quantidade_pedidos": "Quantidade de Pedidos",
    "quantidade_faltantes": "Quantidade de Itens Faltantes",
    "valor_financeiro": "Valor Financeiro ($)"
}), height=400)

st.markdown("---")

# Exibir a tabela para Electronics
st.markdown("### Electronics")
st.dataframe(df_electronics.set_index("product_name_cleaned").rename(columns={
    "category_cleaned": "Categoria",
    "quantidade_pedidos": "Quantidade de Pedidos",
    "quantidade_faltantes": "Quantidade de Itens Faltantes",
    "valor_financeiro": "Valor Financeiro ($)"
}), height=400)

st.markdown("---")

# Resumo Final
st.markdown("""
### Resumo Final
- A categoria Supermarket apresenta o maior número de itens faltantes, com destaque para o produto Chicken Breast e Rice Cakes.
- A categoria Electronics também apresenta problemas significativos, especialmente com produtos de menor tamanho como Mouse e Earbuds.
- Análise de Tendências Temporais não parecem ter nenhuma ligação forte com os problemas de itens faltantes.
""")

st.markdown("---")

st.markdown("""
### Explore Mais
Utilize o menu lateral para acessar análises detalhadas sobre produtos, motoristas e clientes.
""")