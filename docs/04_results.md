[← Voltar para o README](../README.md)

# 📊 Análise e Respostas - Desafio de Precificação de Aluguéis  

## **1️⃣ Análise Exploratória dos Dados (EDA)**  

A Análise Exploratória de Dados (EDA) foi realizada para entender melhor o conjunto de dados, identificar padrões e levantar hipóteses de negócio. As principais etapas foram:  

### **📂 Carregamento e Estrutura dos Dados**  

- O dataset contém informações sobre imóveis para aluguel na plataforma, incluindo localização, tipo de acomodação, preço e disponibilidade.  
- Variáveis categóricas como **bairro_group** e **room_type** foram analisadas usando **gráficos de barras**.  
- Variáveis numéricas como **price** e **reviews_por_mes** foram exploradas através de **histogramas e boxplots**.  

### **🔍 Principais Descobertas**  

1. **Distribuição de Preços:** A maioria dos imóveis tem preços abaixo de $500, mas há **outliers acima de $10.000**.  
2. **Correlação entre Variáveis:**  
   - O preço tem **baixa correlação linear** com a maioria das variáveis.  
   - A **localização (latitude e longitude)** tem impacto significativo no preço.  
3. **Densidade de Imóveis:** Áreas como **Manhattan e Brooklyn** possuem **alta densidade de imóveis**, indicando grande concorrência.  
4. **Tipos de Acomodação:**  
   - **Entire home/apt** tem preços médios mais altos que **private room** ou **shared room**.  

### **📌 Hipóteses de Negócio**  

1. **Investir em Manhattan pode ser mais lucrativo**, pois há maior demanda e preços médios mais elevados.  
2. **Imóveis disponíveis por mais dias no ano tendem a gerar maior receita.**  
3. **Imóveis com maior número de avaliações são mais atrativos para novos clientes.**  

---  

## **2️⃣ Perguntas Específicas**  

### **2A - Onde seria mais indicada a compra de um apartamento para aluguel?**  

**Recomendação:** Investir em **Manhattan**, pois apresenta os preços mais altos e grande demanda, especialmente para **"Entire home/apt"**.  

### **2B - O número mínimo de noites e a disponibilidade ao longo do ano interferem no preço?**  

- A variável **minimo_noites** apresenta alguns outliers extremos, mas não influencia diretamente no preço.  
- A **disponibilidade_365** pode impactar a **rentabilidade** do imóvel, mas não mostrou forte correlação com o preço.  
- **Sugestão:** Investidores devem considerar um imóvel com **alta disponibilidade** para maximizar a receita anual.  

### **2C - Existe um padrão no nome do local para lugares de maior valor?**  

- Imóveis com nomes como **"Luxury", "Penthouse", "Suite"** tendem a estar em regiões com preços mais elevados.  
- Nomes mais genéricos ou sem apelo comercial geralmente pertencem a acomodações mais baratas.  

---  

## **3️⃣ Como a previsão do preço é realizada?**  

O modelo de previsão foi construído com base no **Random Forest Regressor**, utilizando as seguintes etapas:  

### **📊 Variáveis Utilizadas e Transformações**  

| **Variável**               | **Transformação Utilizada**  | **Justificativa** |
|---------------------------|----------------------------|------------------|
| **price** (Preço)         | `log(price + 1)`           | Reduz a dispersão dos valores e melhora a modelagem da variável alvo. |
| **bairro_group**          | One-Hot Encoding           | Variável categórica com poucas categorias. |
| **room_type**             | One-Hot Encoding           | Categórica, com impacto direto no preço. |
| **latitude / longitude**  | Normalização + Distância ao centro | Representação espacial do imóvel. |
| **densidade_imoveis**     | Contagem por bairro        | Indica a oferta de imóveis na região. |
| **proximidade_centro**    | Cálculo via fórmula de Haversine | Quanto mais próximo do centro, maior a tendência de preços elevados. |
| **reviews_por_mes**       | Normalização               | Indica a popularidade do imóvel. |
| **disponibilidade_365**   | Normalização               | Determina quantos dias por ano o imóvel está disponível. |

### **🎯 Tipo de Problema**  

O problema é de **Regressão**, pois o objetivo é prever um **valor numérico contínuo** (preço do aluguel).  

### **🔍 Modelo Escolhido: Random Forest Regressor**  

✅ **Vantagens:**  

- Captura **relações não lineares** nos dados.  
- **Robusto a outliers** devido à combinação de múltiplas árvores de decisão.  
- **Lida bem com muitas variáveis** sem exigir pré-processamento excessivo.  

⚠️ **Desvantagens:**  

- Pode ser **computacionalmente custoso**.  
- **Difícil interpretação** dos pesos das variáveis.  

**Métrica de Avaliação:**  

| **Métrica** | **Valor** |
|------------|----------|
| ✅ **MAE**  | 0.2603 |
| ✅ **RMSE** | 0.3492 |
| ✅ **R² Score** | 0.6321 |  

---  

## **4️⃣ Qual seria a sugestão de preço para o apartamento fornecido?**  

Para o seguinte imóvel:  

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

## **5️⃣ Salvamento do Modelo em `.pkl`**  

O modelo foi salvo no formato **.pkl** para possibilitar **reuso e previsões futuras**:  

```python
joblib.dump(modelo, "models/random_forest.pkl")
```  

---  

## **6️⃣ Entrega do Projeto**  

Para atender aos requisitos, o projeto será disponibilizado em um **repositório público** contendo:  

✅ **README com instruções de instalação e execução** 📄  
✅ **Arquivo de requisitos (`requirements.txt`)** 📦  
✅ **Relatórios das análises estatísticas e EDA** 📊  
✅ **Códigos de modelagem no Jupyter Notebook** 🖥️  
✅ **Arquivo `.pkl` do modelo treinado** 🔍  
✅ **Vídeo explicativo** 🎥  

---  

## **📌 Conclusão**  

- O modelo de **Random Forest Regressor** mostrou **boa capacidade preditiva**, explicando **63,21% da variância dos preços**.  
- A análise de preços indicou que **Manhattan** é a melhor região para investimento.  
- A abordagem utilizada pode ser refinada com **novas features e otimização de hiperparâmetros**.  

📌 *Este estudo demonstra como um modelo de Machine Learning pode ser utilizado para precificação inteligente de imóveis!* 🚀🏡  
