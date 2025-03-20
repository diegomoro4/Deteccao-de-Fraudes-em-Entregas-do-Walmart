import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Configuração do layout
st.set_page_config(page_title="Modelo Preditivo", layout="wide")

# Banner ou imagem
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Walmart_logo.svg/2560px-Walmart_logo.svg.png", width=150)

# Título
st.title("Modelo Preditivo")

# Introdução ao Modelo Preditivo
st.markdown("""
<div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
    <p style="font-size: 16px;">         
        Esta página permite que você interaja com o modelo preditivo desenvolvido para identificar possíveis fraudes em entregas realizadas pelo Walmart.  
        Insira os dados abaixo para obter uma previsão do modelo.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Carregar o modelo preditivo salvo em um arquivo .pkl
def carregar_modelo():
    try:
        with open("../modelo/gradient_boosting_model.pkl", "rb") as file:
            modelo = pickle.load(file)
        return modelo
    except Exception as e:
        st.error(f"Erro ao carregar o modelo: {e}")
        return None

modelo = carregar_modelo()

if modelo is not None:
    # Entrada do usuário
    st.markdown("### Insira os Dados para Previsão")
    idade_motorista = st.slider("Idade do Motorista", 18, 70, 35)
    idade_cliente = st.slider("Idade do Cliente", 18, 100, 40)
    itens_entregues = st.number_input("Itens Entregues", min_value=0, value=10)
    itens_faltantes = st.number_input("Itens Faltantes", min_value=0, value=2)
    valor_pedido = st.number_input("Valor Total do Pedido ($)", min_value=0.0, value=100.0)

    # Botão para realizar a previsão
    if st.button("Realizar Previsão"):
        try:
            # Criar array com os dados de entrada
            dados_entrada = np.array([[idade_motorista, idade_cliente, itens_entregues, itens_faltantes, valor_pedido]])
            
            # Exibir os dados de entrada para depuração
            st.write("Dados de Entrada:", dados_entrada)

            # Fazer previsão usando o modelo carregado
            previsao = modelo.predict(dados_entrada)
            probabilidade = modelo.predict_proba(dados_entrada)

            # Exibir os resultados da previsão
            st.markdown("### Resultado da Previsão")
            if previsao[0] == 1:
                st.error(f"⚠️ Fraude Detectada! Probabilidade: {probabilidade[0][1]:.2%}")
            else:
                st.success(f"✅ Sem Fraude Detectada! Probabilidade: {probabilidade[0][0]:.2%}")
        except Exception as e:
            st.error(f"Erro ao realizar a previsão: {e}")
else:
    st.error("O modelo não foi carregado corretamente. Verifique o arquivo .pkl.")