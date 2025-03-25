import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# Carregar os dados com caminho absoluto
def load_data():
    # Caminho absoluto baseado na raiz do projeto
    base_dir = Path(__file__).resolve().parent.parent.parent  # Sobe três níveis para "Projeto/"
    file_path = base_dir / "data" / "processed" / "df_final_walmart.csv"
    return pd.read_csv(file_path)

# Carregar os dados
df = load_data()

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
        # Caminho absoluto baseado na raiz do projeto
        base_dir = Path(__file__).resolve().parent.parent.parent  # Sobe três níveis para "Projeto/"
        modelo_path = base_dir / "modelo" / "gradient_boosting_model.pkl"
        
        if not modelo_path.exists():
            raise FileNotFoundError(f"O arquivo do modelo não foi encontrado em: {modelo_path}")
        
        return joblib.load(modelo_path)
    except Exception as e:
        st.error(f"Erro ao carregar o modelo: {e}")
        return None

# Carregar o modelo
modelo = carregar_modelo()

if modelo is not None:
    st.success("Modelo carregado com sucesso!")
else:
    st.error("O modelo não foi carregado corretamente.")

# Definir as colunas usadas no treinamento (extraídas do Jupyter Notebook)
X_train_columns = [
    # Variáveis Numéricas
    "order_amount", "items_delivered", "Trips",
    "driver_complaint_rate", "customer_complaint_rate", "is_night_delivery",

    # region (codificadas)
    "region_Altamonte Springs", "region_Apopka", "region_Clermont",
    "region_Kissimmee", "region_Orlando", "region_Sanford",
    "region_Winter Park",

    # delivery_period (codificadas)
    "delivery_period_Manhã", "delivery_period_Noite", "delivery_period_Tarde",

    # day_of_week (codificadas)
    "day_of_week_Friday", "day_of_week_Monday", "day_of_week_Saturday",
    "day_of_week_Sunday", "day_of_week_Thursday", "day_of_week_Tuesday",
    "day_of_week_Wednesday",

    # driver_age_group (codificadas)
    "driver_age_group_18-25", "driver_age_group_26-35",
    "driver_age_group_36-45", "driver_age_group_46-55",
    "driver_age_group_56-65",

    # customer_age_group (codificadas)
    "customer_age_group_18-25", "customer_age_group_26-35",
    "customer_age_group_36-45", "customer_age_group_46-55",
    "customer_age_group_56-65", "customer_age_group_66-75",
    "customer_age_group_76-85", "customer_age_group_85+",

    # order_value_category (codificadas)
    "order_value_category_low", "order_value_category_medium",
    "order_value_category_high"
]

if modelo is not None:
    st.markdown("### Insira os Dados para Previsão")
        
    # Widgets interativos para entrada manual de dados
    order_amount = st.number_input("Valor Total do Pedido ($)", min_value=0.0, value=150.0)
    region = st.selectbox("Região", ['Altamonte Springs', 'Apopka', 'Clermont', 
                                     'Kissimmee', 'Orlando', 'Sanford', 
                                     'Winter Park'])
    items_delivered = st.number_input("Itens Entregues", min_value=0, value=5)
    delivery_period = st.selectbox("Período da Entrega", ['Manhã', 'Noite', 
                                                         'Tarde'])
    day_of_week = st.selectbox("Dia da Semana", ["Friday", "Monday", "Saturday", 
                                                 "Sunday", "Thursday", 
                                                 "Tuesday", "Wednesday"])
    driver_age_group = st.selectbox("Faixa Etária do Motorista", ['18-25', '26-35', 
                                                                  '36-45', '46-55',
                                                                  '56-65'])
    customer_age_group = st.selectbox("Faixa Etária do Cliente", ['18-25', '26-35',
                                                                  '36-45', '46-55',
                                                                  '56-65', '66-75',
                                                                  '76-85', '85+'])
    Trips = st.number_input("Número de Viagens (Motorista)", min_value=0, value=10)
    is_night_delivery = st.selectbox("Entrega Noturna?", [0, 1])
    order_value_category = st.selectbox("Categoria do Valor do Pedido", ['low', 'medium', 'high'])

    if st.button("Realizar Previsão"):
        try:
            # Criar DataFrame com os dados fornecidos pelo usuário
            new_data = pd.DataFrame({
                'order_amount': [order_amount],
                'region': [region],
                'items_delivered': [items_delivered],
                'delivery_period': [delivery_period],
                'day_of_week': [day_of_week],
                'driver_age_group': [driver_age_group],
                'Trips': [Trips],
                'customer_age_group': [customer_age_group],
                'is_night_delivery': [is_night_delivery],
                'order_value_category': [order_value_category]
            })

            # Definir todas as categorias esperadas com base no treinamento
            region_categories = ['Altamonte Springs', 'Apopka', 'Clermont', 'Kissimmee',
                     'Orlando', 'Sanford', 'Winter Park']
            delivery_period_categories = ['Manhã', 'Noite', 'Tarde']
            day_of_week_categories = ["Friday", "Monday", "Saturday", 
                                    "Sunday", "Thursday", 
                                    "Tuesday", "Wednesday"]
            driver_age_categories = ['18-25', '26-35', '36-45', 
                                    '46-55', '56-65']
            customer_age_categories = ['18-25', '26-35', '36-45',
                                    '46-55', '56-65', 
                                    '66-75', '76-85',
                                    '85+']
            order_value_categories = ['low', 'medium', 'high']

            # Garantir que todas as categorias sejam representadas corretamente
            new_data['region'] = pd.Categorical(new_data['region'], categories=region_categories)
            new_data['delivery_period'] = pd.Categorical(new_data['delivery_period'], categories=delivery_period_categories)
            new_data['day_of_week'] = pd.Categorical(new_data['day_of_week'], categories=day_of_week_categories)
            new_data['driver_age_group'] = pd.Categorical(new_data['driver_age_group'], categories=driver_age_categories)
            new_data['customer_age_group'] = pd.Categorical(new_data['customer_age_group'], categories=customer_age_categories)
            new_data['order_value_category'] = pd.Categorical(new_data['order_value_category'], categories=order_value_categories)

            # Pré-processar os dados
            new_data = pd.get_dummies(new_data, columns=['region', 'delivery_period', 
                                                         'day_of_week',
                                                         'driver_age_group',
                                                         'customer_age_group',
                                                         'order_value_category'])

            # Adicionar colunas ausentes e garantir a ordem correta
            for col in X_train_columns:
                if col not in new_data.columns:
                    new_data[col] = 0
            new_data = new_data[X_train_columns]

            # Fazer previsão usando o modelo carregado
            probabilities = modelo.predict_proba(new_data)[:, 1]
            predictions = (probabilities >= 0.45).astype(int)

            # Exibir os resultados da previsão
            st.markdown("### Resultado da Previsão")
            if predictions[0] == 1:
                st.error(f"⚠️ Fraude Detectada!\n Nivel de Confiança: {probabilities[0]:.2%}")
            else:
                st.success(f"✅ Sem Fraude Detectada! Nivel de Confiança: {(1 - probabilities[0]):.2%}")

            # Explicação sobre o nível de confiança
            st.markdown("""
            <div style="background-color:#f9f9f9; padding: 15px; border-radius: 10px;">
                <p style="font-size: 14px;">         
                    O nível de confiança indica a probabilidade calculada pelo modelo para cada classe. 
                </p>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erro ao realizar a previsão: {e}")
else:
    st.error("O modelo não foi carregado corretamente.")
