import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
def load_data():
    return pd.read_csv("../data/processed/df_final_walmart.csv")

df = load_data()

# Configuração do layout
st.set_page_config(page_title="Dashboard Walmart", layout="wide")

st.title("Bem-vindo ao Dashboard Walmart!")
st.write("Selecione uma página no menu lateral.")