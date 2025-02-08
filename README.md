# 🏡 Previsão de Preços de Aluguel - Nova York  

---  

## 📌 Sobre o Projeto  

Este projeto tem como objetivo prever os preços de aluguéis em Nova York com base em um conjunto de dados de imóveis de Nova York.  
Utilizando **Machine Learning**, realizamos uma análise exploratória, pré-processamento dos dados, engenharia de atributos, treinamento do modelo e avaliação de desempenho.  

As principais etapas do projeto incluem:  

✅ **Análise Exploratória dos Dados (EDA)** 📊  
✅ **Pré-processamento e Engenharia de Atributos** 🛠️  
✅ **Treinamento e Avaliação do Modelo** 🤖  
✅ **Previsão** 💰  

---  

## 📁 Estrutura do Repositório  

```bash
nyc_rental_price_prediction/
│── data/                     # Conjunto de dados (bruto, processado e final)
│── models/                   # Modelos treinados (.pkl)
│── notebooks/                # Jupyter Notebooks com análises e treinamento
│── reports/                  # Relatórios gerados durante as análises
│── scr/                      # Scripts de pré-processamento e modelagem
│── README.md                 # Documentação do projeto
└── requirements.txt          # Pacotes e versões utilizadas
```

---  

## 🚀 Como Executar o Projeto  

### **1️⃣ Clonar o Repositório**  

```bash
git clone https://github.com/lucenfort/nyc_rental_price_prediction.git
cd nyc_rental_price_prediction
```  

### **2️⃣ Criar e Ativar o Ambiente Virtual**  

```bash
python -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate     # Para Windows

```  

### **3️⃣ Instalar as Dependências**  

```bash
pip install -r requirements.txt
```  

### **4️⃣ Executar os Notebooks**  

Os notebooks do projeto podem ser encontrados na pasta `/notebooks/` e devem ser executados na seguinte ordem:  

1️⃣ **[EDA - Análise Exploratória](./notebooks/01_eda_notebook.ipynb)** 📊  
2️⃣ **[Pré-Processamento e Feature Engineering](./notebooks/02_processing_notebook.ipynb)** 🛠️  
3️⃣ **[Treinamento e Validação](./notebooks/03_training_notebook.ipynb)** 🤖  
4️⃣ **[Predição](./notebooks/04_prediction_notebook.ipynb)** 📈  

Para abrir os notebooks, utilize:  

```bash
jupyter notebook
```  

---  

## 🔍 Modelo Utilizado  

O modelo treinado foi um **Random Forest Regressor**, escolhido por suas vantagens:  

✅ **Captura relações não lineares nos dados**  
✅ **Robusto a outliers**  
✅ **Lida bem com múltiplas variáveis**  
✅ **Baixo risco de overfitting** (quando bem parametrizado)  

Métrica de Avaliação:  

| **Métrica** | **Valor** |
|------------|----------|
| ✅ **MAE**  | 0.2603 |
| ✅ **RMSE** | 0.3492 |
| ✅ **R² Score** | 0.6321 |  

---  

## 📌 Previsão do Preço e Conversão de Moeda  

A previsão do preço do aluguel pode ser realizada com base nas características do imóvel.  
Além disso, a conversão para **BRL (Reais) e EUR (Euros)** é feita utilizando a API **AwesomeAPI**.  

Exemplo de um imóvel previsto:  

```python
apartamento = {
    'bairro_group': 'Manhattan',
    'latitude': 40.75362,
    'longitude': -73.98377,
    'room_type': 'Entire home/apt',
    'minimo_noites': 1,
    'numero_de_reviews': 45,
    'reviews_por_mes': 0.38,
    'calculado_host_listings_count': 2,
    'disponibilidade_365': 355
}
```  

✅ **Preço sugerido:** **$207.08 USD**  
💰 **Conversões:**  

- 🇧🇷 **R$ 1196,94 BRL**  
- 💶 **€ 200,58 EUR**  

---  

## 📂 Entrega do Projeto  

📦 **Arquivos entregues neste repositório:**  

- 📜 **[EDA - Análise Exploratória](./docs/01_eda.md)**  
- 🛠️ **[Pré-Processamento e Feature Engineering](./docs/02_preprocessing.md)**  
- 🤖 **[Treinamento do Modelo](./docs/03_train.md)**  
- 📈 **[Resultados e Avaliação](./docs/04_results.md)**  
- 🔍 **Modelo Treinado** **[(`random_forest.pkl`)](https://drive.google.com/file/d/16oJUcoyqpTtQ1H3VfhtOa7Y7RoMz4tC2/view?usp=sharing)**

- 📊 **Relatórios e Gráficos**  
<!--
📹 **Vídeo Explicativo** será disponibilizado via Google Drive com acesso liberado para visualização.  
-->

---  
