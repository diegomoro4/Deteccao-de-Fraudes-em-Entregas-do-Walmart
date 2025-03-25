# Detecção de Fraudes em Entregas do Walmart

## 🌐 Dashboard Online
Acesse o dashboard interativo hospedado no Streamlit Cloud:
[Dashboard Walmart](https://<link-do-dashboard-streamlit-cloud>)

## Objetivo do Projeto

Este projeto foi desenvolvido como parte de um estudo de **Data Science** para o Walmart, com o objetivo de **detectar fraudes em entregas realizadas via e-commerce**. A análise abrangeu desde a exploração dos dados até a implementação de um modelo preditivo e a criação de um dashboard interativo.

Fraudes em entregas podem ocorrer por parte dos motoristas ou clientes, gerando perdas financeiras significativas. Este projeto busca identificar padrões fraudulentos e propor ações preventivas para minimizar esses problemas.

---

## Índice

1. [Objetivo do Projeto](#-objetivo-do-projeto)
2. [Principais Componentes](#-principais-componentes)
3. [Tecnologias Utilizadas](#-tecnologias-utilizadas)
4. [Como Executar o Projeto](#️-como-executar-o-projeto)
5. [Resultados Obtidos](#-resultados-obtidos)
6. [Documentação Complementar](#-documentação-complementar)
7. [Contribuição](#-contribuição)
8. [Contato](#-contato)

---

## 🚀 Principais Componentes

### **1. Análise Exploratória (EDA)**
- Exploramos os datasets individuais (`orders`, `drivers_data`, `customer_data`, `missing_data` e `products`) para entender padrões e identificar problemas logísticos.
- Insights obtidos:
  - Motoristas e clientes problemáticos.
  - Produtos mais reportados como faltantes.
  - Regiões e períodos críticos.

### **2. Integração dos Datasets**
- Consolidamos os dados em um único dataset (`df_final`) para permitir análises cruzadas entre motoristas, clientes, produtos e regiões.
- Identificamos padrões consistentes que indicam fraudes ou problemas operacionais.

### **3. Modelo Preditivo**
- Desenvolvemos um modelo preditivo baseado em Gradient Boosting para detectar fraudes.
- Métricas principais:
  - Precisão: **84%**
  - Recall: **10%**
  - ROC-AUC: **0.93**
- O modelo foi ajustado para minimizar falsos positivos e oferecer impacto financeiro positivo.

### **4. Dashboard Interativo**
- Criamos um dashboard interativo usando Streamlit para monitorar entregas e identificar problemas em tempo real.
- Funcionalidades:
  - Visualização de KPIs por região.
  - Análise detalhada de motoristas, clientes e produtos.
  - Previsões baseadas no modelo preditivo.

---

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal para análise de dados e desenvolvimento do modelo.
- **Streamlit**: Framework para criação do dashboard interativo.
- **Pandas & NumPy**: Manipulação e análise dos dados.
- **Scikit-learn**: Desenvolvimento e avaliação do modelo preditivo.
- **Plotly**: Criação de visualizações interativas.
- **Jupyter Notebook**: Documentação das etapas analíticas.

---

## ⚙️ Como Executar o Projeto

### **1. Pré-requisitos**
Certifique-se de ter instalado:
- Python (versão >= 3.8)
- Pip ou Conda para gerenciar pacotes

### **2. Instalação**
Clone este repositório:
- git clone <https://github.com/diegomoro4/Deteccao-de-Fraudes-em-Entregas-do-Walmart>


### **3. Instale as dependências**
- pip install -r requirements.txt


### **3. Executar o Dashboard**
Para rodar o dashboard interativo:
`streamlit run dashboard.py``


---


## 📈 Resultados Obtidos

### Impacto Financeiro:
- Redução estimada de **10% nas fraudes**, representando economia significativa nos prejuízos financeiros causados por itens faltantes.

### Eficiência Operacional:
- Identificação de motoristas e clientes problemáticos, permitindo ações corretivas direcionadas.
- Melhorias sugeridas nos processos logísticos para regiões críticas como Apopka.

---

## 📄 Documentação Complementar

Os seguintes documentos estão disponíveis na pasta `documentos/`:
1. **Recomendações Preventivas:** Medidas práticas para reduzir fraudes e melhorar a eficiência logística.
2. **Propostas de Aprimoramento:** Estratégias avançadas para melhorar a qualidade dos dados, implementar tecnologias modernas e realizar experimentos controlados.

---

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias ou sugestões! Para isso:
1. Faça um fork deste repositório.
2. Crie uma branch com sua contribuição (`git checkout -b minha-contribuicao`).
3. Envie um pull request.

---

## 📧 Contato

Para dúvidas ou informações adicionais, entre em contato:
- Nome: Diego Moro
- Email: diego.moro4@hotmail.com


