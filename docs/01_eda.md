[← Voltar para o README](../README.md)

# 📊 Relatório de Análise Exploratória de Dados (EDA)

## 📝 1. Introdução

Este relatório apresenta uma análise exploratória detalhada do dataset `teste_indicium_precificacao.csv`, contendo informações sobre listagens de imóveis para aluguel em Nova York.

📌 **Objetivo da Análise:**

- Identificar padrões e tendências nos preços.
- Avaliar a influência da disponibilidade e número mínimo de noites no valor dos imóveis.
- Fornecer insights estratégicos para investidores e locadores.

📊 **Tamanho do Dataset:** 48.894 registros e 17 colunas.

---

## 📂 2. Estrutura dos Dados

### 📋 2.1 Informações Gerais

🔹 O dataset contém as seguintes categorias:

- 🏠 **Identificadores:** `id`, `host_id`, `nome`, `host_name`.

- 🌎 **Localização:** `bairro_group`, `bairro`, `latitude`, `longitude`.

- 📌 **Características:** `room_type`, `price`, `minimo_noites`, `disponibilidade_365`.

- ⭐ **Feedbacks:** `numero_de_reviews`, `ultima_review`, `reviews_por_mes`.

### 🚨 2.2 Valores Ausentes

🔎 Alguns campos possuem valores ausentes:

- `nome`: 16 ausentes.

- `host_name`: 21 ausentes.

- `ultima_review` e `reviews_por_mes`: 10.052 ausentes.

Isso indica que algumas propriedades nunca receberam avaliações ou não tiveram reviews recentes.

---

## 📈 3. Correlação Entre Variáveis Numéricas

A matriz de correlação identifica relações entre as variáveis do dataset.

🖼 **Matriz de Correlação** 📊  
![Matriz de Correlação](/reports/eda/figures/eda_matriz_correlacao.png)

### 🔎 **Principais Insights:**

✔ `reviews_por_mes` e `numero_de_reviews` possuem **correlação moderada (0.55)**, indicando que listagens populares recebem avaliações constantes.

✔ `price` não apresenta correlações significativas com outras variáveis, sugerindo que fatores externos (como localização e marketing) podem ser mais influentes.

---

## 💰 4. Distribuição de Preços

### 📊 4.1 Distribuição do `price`

![Distribuição de Price](/reports/eda/figures/eda_distribuicao_price.png)

📌 A maioria dos preços está **abaixo de 500 dólares**, mas existem outliers chegando a **10.000 dólares**.

### 🔄 4.2 Distribuição do `price_log`

![Distribuição de Price Log](/reports/eda/figures/eda_distribuicao_price_log.png)

📌 A transformação logarítmica melhora a distribuição dos preços, reduzindo o impacto de valores extremos.

---

## 📆 5. Mínimo de Noites e Disponibilidade

### 🌙 5.1 Distribuição do `minimo_noites`

![Distribuição de Mínimo de Noites](/reports/eda/figures/eda_distribuicao_minimo_noites.png)

📌 A maioria das propriedades tem um **mínimo de 1 a 5 noites**, mas há casos extremos exigindo **até 1250 noites**.

### 📦 5.2 Boxplots

📌 Há **muitos outliers** no preço e mínimo de noites, o que pode impactar a análise dos dados.

- O boxplot de price mostra um grande número de valores extremos bem acima da parte superior do whisker.

🖼 **Boxplot de `price`** 📊  
![Boxplot de Price](/reports/eda/figures/eda_boxplot_price.png)

- O boxplot de minimo_noites revela valores anômalos com alguns imóveis exigindo centenas de noites de estadia mínima.

🖼 **Boxplot de `minimo_noites`** 📊  
![Boxplot de Mínimo Noites](/reports/eda/figures/eda_boxplot_minimo_noites.png)

- O boxplot de price_log suaviza essa dispersão, mas ainda exibe outliers, mesmo na escala logarítmica.

🖼 **Boxplot de `price_log`** 📊  
![Boxplot de Price Log](/reports/eda/figures/eda_boxplot_price_log.png)

📌 Conclusão: A quantidade de pontos fora do whisker nos boxplots indica uma alta quantidade de outliers, o que sugere que certos imóveis têm valores extremamente altos, podendo distorcer a média e a análise geral.

---

## 🌍 6. Distribuição Geográfica dos Imóveis

📍 **Mapa da Distribuição**  
![Distribuição Geográfica](/reports/eda/figures/eda_distribuicao_geografica.png)

📌 **Principais Regiões:**

✔ **Manhattan** possui a maior concentração de imóveis e valores mais altos.

✔ **Brooklyn** também tem uma alta oferta de acomodações.

✔ **Staten Island** apresenta menos opções disponíveis.

---

## 🏡 7. Distribuição por Tipo de Quarto

📊 **Gráfico de Tipos de Quartos**  
![Distribuição de Tipos de Quarto](/reports/eda/figures/eda_barras_room_type.png)

🏠 **Tipos de Acomodações:**

- 🏢 **Entire home/apt**: 25.409 listagens (**51.9%** do total).
- 🛏 **Private room**: 21.370 listagens (**43.7%** do total).
- 🚪 **Shared room**: 2.115 listagens (**4.3%** do total).

📌 A maioria das listagens são **apartamentos inteiros**, sugerindo que investidores dominam o mercado.

---

## 🔍 8. Respostas às Perguntas

### 📍 8.1 Qual a melhor localização para investir?

📌 **Manhattan e Brooklyn** têm os **maiores preços e demanda**, tornando-os os locais mais atrativos para investimento imobiliário.

### 📆 8.2 O número mínimo de noites impacta o preço?

📌 A correlação entre `minimo_noites` e `price` é **baixa (-0.06)**, indicando que o número mínimo de noites **não afeta diretamente o preço**.

### 🔝 8.3 Existe um padrão nos nomes das acomodações mais caras?

📌 Imóveis mais caros frequentemente incluem palavras como **“Luxury”, “Penthouse” e “View”**, sugerindo uma estratégia de **marketing premium**.

---

## ✅ 9. Conclusão

📌 **Principais Descobertas:**

✔ **Melhores locais para investir:** Manhattan e Brooklyn.

✔ **Impacto do número mínimo de noites:** Pequeno ou irrelevante.

✔ **Acomodações mais caras seguem padrões de marketing premium.**

📌 **Recomendações:**

✔ Investidores devem focar em regiões centrais como Manhattan para maximizar o retorno.

✔ Estratégias de precificação devem considerar não apenas métricas quantitativas, mas também aspectos qualitativos como marketing e localização.

---
