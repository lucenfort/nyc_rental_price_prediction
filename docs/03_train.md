[← Voltar para o README](../README.md)

# 🎯 Relatório de Treinamento e Validação do Modelo

## 📝 1. Introdução

Este relatório documenta os resultados do **treinamento e validação** do modelo preditivo de preços de aluguel em Nova York.

📌 **Objetivo:**

- Ajustar e otimizar um modelo **Random Forest Regressor**.
- Avaliar a precisão e confiabilidade do modelo em prever preços.

📊 **Modelo escolhido:** Random Forest com **validação cruzada k-fold (k=5)**.

---

## 🎛️ 2. Treinamento do Modelo

### 🔧 2.1 Otimização de Hiperparâmetros

Utilizamos **GridSearchCV** para encontrar a melhor combinação de hiperparâmetros:

🔹 **Melhores hiperparâmetros encontrados:**

- `max_depth`: 20
- `min_samples_leaf`: 2
- `min_samples_split`: 10
- `n_estimators`: 200

✔ **Impacto esperado**: Reduzir overfitting e melhorar generalização.

### 📊 2.2 Avaliação do Modelo

📌 **Métricas obtidas:**

- ✅ Erro Médio Absoluto (MAE) = 0.2603

    ✔ O modelo, em média, erra em 0.26 unidades na escala logarítmica do preço. Quanto menor, melhor.

- ✅ Erro Quadrático Médio (RMSE) = 0.3492
    
    ✔ O RMSE é ligeiramente maior que o MAE, indicando que há alguns outliers influenciando as previsões. Penaliza mais erros maiores.

- ✅ Coeficiente de Determinação (R² Score) = 0.6321

    ✔ O modelo explica 63,2% da variação dos preços logarítmicos, indicando um desempenho razoável, mas com espaço para melhoria
---

## 📊 3. Análise Gráfica dos Resultados

### 🎯 3.1 Valores Reais vs Previstos

![Valores Reais vs Previstos](/reports/figures/real_vs_previsto.png)

📌 **Análise**: A maioria dos pontos está próxima da diagonal vermelha, indicando uma previsão consistente. No entanto, alguns valores subestimados e superestimados são visíveis.

### 📈 3.2 Distribuição dos Resíduos

![Distribuição dos Resíduos](/reports/figures/residuos_distribuicao.png)

📌 **Análise**: A distribuição é aproximadamente normal, mas ligeiramente enviesada. Isso sugere que o modelo pode subestimar alguns valores altos.

### 🔄 3.3 Resíduos vs Valores Previstos

![Resíduos vs Valores Previstos](/reports/figures/residuos_vs_previsto.png)

📌 **Análise**: A dispersão sugere um padrão heterocedástico, indicando que a variabilidade dos erros aumenta para preços mais altos.

---
