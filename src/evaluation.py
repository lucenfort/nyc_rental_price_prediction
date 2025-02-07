#!/usr/bin/env python
"""
evaluation.py
-------------
Este módulo realiza a avaliação do modelo treinado.
As etapas incluem:
    - Carregamento dos dados finais (com features) e divisão em treino/teste;
    - Carregamento do modelo salvo;
    - Previsão no conjunto de teste;
    - Cálculo das métricas de desempenho: MAE, RMSE e R²;
    - Geração de gráficos (distribuição dos resíduos, scatter plot de valores reais vs. previstos e resíduos vs. previstos);
    - Geração e salvamento de um relatório de avaliação.
"""

import os
import warnings
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import logging
from scipy.stats import normaltest

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_model(model_path: str):
    """
    Carrega o modelo treinado a partir do caminho especificado.
    """
    try:
        model = joblib.load(model_path)
        logger.info(f"Modelo carregado com sucesso de: {model_path}")
        return model
    except Exception as e:
        logger.error(f"Erro ao carregar o modelo: {e}", exc_info=True)
        raise

def load_data(filepath: str) -> pd.DataFrame:
    """
    Carrega os dados a partir de um arquivo CSV.
    """
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Dados carregados com sucesso de: {filepath}")
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar os dados: {e}", exc_info=True)
        raise

def load_best_params(path: str) -> dict:
    """
    Carrega os melhores hiperparâmetros a partir de um arquivo JSON.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            best_params = json.load(f)
        logger.info(f"Melhores parâmetros carregados de: {path}")
        return best_params
    except Exception as e:
        logger.error(f"Erro ao carregar os melhores parâmetros: {e}", exc_info=True)
        return {"n_estimators": "Desconhecido",
                "max_depth": "Desconhecido",
                "min_samples_split": "Desconhecido",
                "min_samples_leaf": "Desconhecido"}

def generate_plots(y_true, y_pred, report_figures_dir: str):
    """
    Gera gráficos de avaliação dos resíduos e salva os mesmos no diretório especificado.
    """
    os.makedirs(report_figures_dir, exist_ok=True)
    residuals = y_true - y_pred
    
    # Teste de normalidade dos resíduos
    stat, p_value = normaltest(residuals)
    if p_value < 0.05:
        logger.info("Os resíduos não seguem uma distribuição normal (p-valor < 0.05).")
    else:
        logger.info("Os resíduos parecem seguir uma distribuição normal (p-valor >= 0.05).")
    
    plt.figure(figsize=(10,6))
    sns.histplot(residuals, bins=30, kde=True, color='purple')
    plt.title("Distribuição dos Resíduos", fontsize=14)
    plt.xlabel("Resíduos", fontsize=12)
    plt.ylabel("Frequência", fontsize=12)
    plt.tight_layout()
    path_residuos_hist = os.path.join(report_figures_dir, "residuos_distribuicao.png")
    plt.savefig(path_residuos_hist)
    plt.close()
    
    plt.figure(figsize=(10,6))
    sns.scatterplot(x=y_true, y=y_pred, color='green', alpha=0.6)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--')
    plt.title("Valores Reais vs Previstos", fontsize=14)
    plt.xlabel("Valores Reais", fontsize=12)
    plt.ylabel("Valores Previstos", fontsize=12)
    plt.tight_layout()
    path_scatter = os.path.join(report_figures_dir, "real_vs_previsto.png")
    plt.savefig(path_scatter)
    plt.close()
    
    plt.figure(figsize=(10,6))
    sns.scatterplot(x=y_pred, y=residuals, color='orange', alpha=0.6)
    plt.axhline(0, linestyle='--', color='red')
    plt.title("Resíduos vs Valores Previstos", fontsize=14)
    plt.xlabel("Valores Previstos", fontsize=12)
    plt.ylabel("Resíduos", fontsize=12)
    plt.tight_layout()
    path_residuos_scatter = os.path.join(report_figures_dir, "residuos_vs_previsto.png")
    plt.savefig(path_residuos_scatter)
    plt.close()
    
    logger.info("Gráficos de avaliação gerados com sucesso.")
    return {
        "residuos_hist": path_residuos_hist,
        "real_vs_previsto": path_scatter,
        "residuos_vs_previsto": path_residuos_scatter
    }

def generate_report(report_path: str, metrics: dict, best_params: dict, figures_paths: dict):
    """
    Gera e salva um relatório de avaliação do modelo.
    """
    report_text = (
        "RELATÓRIO DE AVALIAÇÃO DO MODELO\n"
        "---------------------------------\n\n"
        "Métricas de Desempenho:\n"
        f"MAE: {metrics['MAE']:.4f}\n"
        f"RMSE: {metrics['RMSE']:.4f}\n"
        f"R²: {metrics['R2']:.4f}\n\n"
        "Melhores Hiperparâmetros:\n"
    )
    for param, value in best_params.items():
        report_text += f" - {param}: {value}\n"
    
    report_text += "\nCaminhos dos Gráficos Gerados:\n"
    for key, path in figures_paths.items():
        report_text += f" - {key}: {path}\n"
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    logger.info(f"Relatório de avaliação salvo em: {report_path}")

def main():
    logger.info("=== Executando evaluation.py ===")
    warnings.filterwarnings("ignore")
    
    caminho_dados = os.path.join("data", "final", "nyc_rental_data_features.csv")
    df = load_data(caminho_dados)
    
    target_column = 'price_log'
    # Remover colunas vazadoras e irrelevantes: price, id e host_id
    features_to_drop = [target_column, 'price', 'id', 'host_id']
    X = df.drop(columns=features_to_drop, errors='ignore')
    y = df[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    caminho_modelo = os.path.join("models", "random_forest.pkl")
    model = load_model(caminho_modelo)
    
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    metrics = {"MAE": mae, "RMSE": rmse, "R2": r2}
    logger.info(f"Métricas de Desempenho: {metrics}")
    
    # As figuras serão salvas na pasta 'reports/figures'
    report_figures_dir = os.path.join("reports", "figures")
    figures_paths = generate_plots(y_test, y_pred, report_figures_dir)
    
    best_params_path = os.path.join("reports", "model_training", "best_params.json")
    best_params = load_best_params(best_params_path)
    
    # O relatório de avaliação será salvo na pasta 'reports'
    report_path = os.path.join("reports", "evaluation.txt")
    generate_report(report_path, metrics, best_params, figures_paths)
    
    logger.info("Avaliação do modelo concluída com sucesso.\nMódulo evaluation executado com sucesso.")

if __name__ == "__main__":
    main()
