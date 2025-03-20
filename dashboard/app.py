import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
def load_data():
    return pd.read_csv("../data/processed/df_final_walmart.csv")

df = load_data()

# Configuração do layout
st.set_page_config(page_title="Dashboard Walmart", layout="wide")

# Banner ou imagem
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Walmart_logo.svg/2560px-Walmart_logo.svg.png", width=150)

# Título principal
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Bem-vindo ao Dashboard Walmart!</h1>", unsafe_allow_html=True)

# Introdução ao projeto
st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 18px;">
        Este dashboard foi desenvolvido como parte de um projeto de <b>Data Science</b> para o Walmart, com o objetivo de analisar e detectar <b>fraudes em entregas realizadas via e-commerce</b>.
    </p>
</div>
""", unsafe_allow_html=True)

# Objetivo do projeto
st.markdown("## Objetivo do Projeto")
st.markdown("""
O Walmart é a maior rede de varejo dos Estados Unidos, gerando cerca de <b>US$ 1,6 bilhão em receita por dia</b>. Apesar de seu sucesso, desafios como <b>fraudes e roubos</b> têm gerado perdas significativas, especialmente nas compras online.

Neste projeto, buscamos identificar padrões e anomalias nos dados de entrega para entender melhor:
- **Fraude do Motorista:** Motoristas podem estar reportando entregas completas quando itens foram desviados ou não entregues.
- **Fraude do Consumidor:** Consumidores podem estar declarando falsamente que não receberam itens para obter reembolsos.
- **Problemas no Sistema:** Falhas no processo ou sistema podem estar contribuindo para os problemas relatados.

O foco inicial deste dashboard é na região Central da Flórida, servindo como modelo para futuras implementações em outras regiões dos Estados Unidos.
""", unsafe_allow_html=True)

# Orientação ao usuário
st.markdown("## Como Navegar no Dashboard")
st.markdown("""
Utilize as páginas disponíveis no menu lateral para explorar as análises detalhadas sobre:
- **KPIs por Região:** Uma visão geral dos indicadores-chave relacionados às entregas.
- **Produtos e Pedidos:** Análise detalhada dos itens faltantes e impacto financeiro por categoria.
- **Motoristas e Clientes:** Relação entre motoristas/clientes e problemas nas entregas.

Nosso objetivo é fornecer insights claros e acionáveis para reduzir perdas financeiras e melhorar a experiência dos consumidores.
""", unsafe_allow_html=True)
