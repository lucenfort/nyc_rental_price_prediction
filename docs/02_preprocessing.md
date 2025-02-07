[← Voltar para o README](../README.md)

# 🏗️ Relatório de Pré-Processamento e Feature Engineering

## 📝 1. Introdução

Este relatório documenta as etapas de **pré-processamento e engenharia de atributos** aplicadas ao dataset de precificação de aluguéis em Nova York.

📌 **Objetivo:**

- Tratar valores ausentes e outliers para garantir a qualidade dos dados.
- Criar novas features relevantes que possam melhorar a capacidade preditiva do modelo.
- Normalizar as variáveis para garantir melhor desempenho durante o treinamento.

📊 **Dimensão inicial do dataset:** 48.894 registros e 17 colunas.

---

## 🔍 2. Tratamento de Dados

### 🚨 2.1 Valores Ausentes

- **`nome` e `host_name`**: 16 e 21 valores ausentes, respectivamente. Preenchidos com a moda.
- **`ultima_review` e `reviews_por_mes`**: 10.052 valores ausentes. Preenchidos com 0, indicando que nunca receberam avaliações.

📌 **Impacto**: Esse tratamento evita a exclusão de dados valiosos e preserva a distribuição estatística original.

### 🔄 2.2 Remoção de Outliers

Utilizamos o método do **Intervalo Interquartil (IQR)** para remover outliers extremos da coluna `price`. Os limites estabelecidos foram:

- **Limite inferior**: Q1 - 1.5 * IQR
- **Limite superior**: Q3 + 1.5 * IQR

> Onde: 
> - Q1 (Primeiro Quartil - 25%): Valor abaixo do qual estão 25% dos dados.
> - Q3 (Terceiro Quartil - 75%): Valor abaixo do qual estão 75% dos dados.
> - IQR (Intervalo Interquartil): Diferença entre o terceiro e o primeiro quartil:

📌 **Impacto**: A remoção de outliers melhorou a distribuição do `price`, reduzindo o impacto de valores aberrantes e tornando o modelo mais robusto.

---

## 🔧 3. Engenharia de Atributos

### 📍 3.1 Criação de Novas Features

#### **Densidade de Imóveis por Bairro**

Criamos a feature `densidade_imoveis`, que contabiliza quantos imóveis existem em cada bairro.

✔ **Impacto esperado**: Regiões com maior densidade tendem a influenciar o preço devido à concorrência.

#### **Proximidade ao Centro**

Calculamos a distância de cada imóvel ao centro de Nova York (**latitude: 40.7128, longitude: -74.0060**) usando a **fórmula de Haversine**.

✔ **Impacto esperado**: Imóveis mais próximos ao centro geralmente possuem preços mais elevados.

### 🎭 3.2 Codificação de Variáveis Categóricas

Variáveis categóricas de baixa cardinalidade (`bairro_group` e `room_type`) foram convertidas em variáveis dummies, garantindo compatibilidade com o modelo.

✔ **Impacto esperado**: Permite ao modelo aprender relações entre categorias e preço.

### 🔄 3.3 Transformação da Variável Alvo

Para reduzir a influência de valores extremos, aplicamos a **transformação logarítmica** (`log1p`) sobre `price`, criando a nova coluna `price_log`.

✔ **Impacto esperado**: Estabiliza a variabilidade dos dados e melhora o ajuste do modelo.

### 📏 3.4 Normalização das Variáveis Numéricas

Todas as features numéricas (exceto `price_log`) foram normalizadas utilizando **StandardScaler**.

✔ **Impacto esperado**: Evita que variáveis com escalas diferentes impactem desproporcionalmente o modelo.

📊 **Dimensão final do dataset:** 45.922 registros e 16 colunas.

---

## ✅ 4. Conclusão

📌 **Principais melhorias:**

- **Redução de ruído nos dados** (remoção de outliers e tratamento de valores ausentes).
- **Adicionadas features com potencial preditivo** (`densidade_imoveis` e `proximidade_centro`).
- **Melhoria na distribuição dos dados** via transformação logarítmica e normalização.

---
