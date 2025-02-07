#!/usr/bin/env python
import os
import warnings
import joblib
import pandas as pd
import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(filepath: str) -> pd.DataFrame:
    """
    Carrega os dados a partir de um arquivo CSV.
    """
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Dados carregados com sucesso de: {filepath}")
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar o arquivo '{filepath}': {e}", exc_info=True)
        raise

def train_model(X_train, y_train):
    """
    Treina o modelo RandomForestRegressor utilizando GridSearchCV para otimização dos hiperparâmetros.
    Retorna o melhor modelo encontrado, os melhores parâmetros e o erro médio da validação cruzada.
    """
    rf = RandomForestRegressor(random_state=42)
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5,
                               scoring='neg_mean_squared_error', n_jobs=-1, verbose=1, error_score='raise')
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    mean_cv_score = -cv_scores.mean()
    logger.info(f"Melhores hiperparâmetros encontrados: {best_params}")
    logger.info(f"Erro quadrático médio na validação cruzada: {mean_cv_score:.4f}")
    return best_model, best_params

def save_model(model, path: str):
    """
    Salva o modelo treinado em um arquivo.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    logger.info(f"Modelo salvo com sucesso em: {path}")

def salvar_best_params(best_params: dict, path: str):
    """
    Salva os melhores hiperparâmetros em um arquivo JSON.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(best_params, f, indent=4)
    logger.info(f"Melhores hiperparâmetros salvos em: {path}")

def gerar_relatorio_treinamento(best_params: dict, caminho_report: str, test_metrics: dict = None) -> None:
    """
    Gera um relatório TXT contendo o resumo do treinamento do modelo, incluindo os melhores hiperparâmetros e, opcionalmente, as métricas do conjunto de teste.
    """
    with open(caminho_report, 'w', encoding='utf-8') as f:
        f.write("RELATÓRIO DE TREINAMENTO DO MODELO\n")
        f.write("-----------------------------------\n")
        f.write("Melhores hiperparâmetros encontrados:\n")
        for param, value in best_params.items():
            f.write(f" - {param}: {value}\n")
        if test_metrics:
            f.write("\nAvaliação no conjunto de teste:\n")
            for metric, value in test_metrics.items():
                f.write(f" - {metric}: {value:.4f}\n")
    logger.info(f"Relatório de treinamento gerado em: {caminho_report}")

def main():
    logger.info("=== Executando model_training.py ===")
    caminho_dados = os.path.join("data", "final", "nyc_rental_data_features.csv")
    df = load_data(caminho_dados)
    
    target_column = 'price_log'
    # Remover colunas vazadoras e irrelevantes: price, id e host_id
    features_to_drop = [target_column, 'price', 'id', 'host_id']
    X = df.drop(columns=features_to_drop, errors='ignore')
    y = df[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    best_model, best_params = train_model(X_train, y_train)
    
    # Avaliação no conjunto de teste
    y_pred_test = best_model.predict(X_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    r2_test = r2_score(y_test, y_pred_test)
    test_metrics = {"RMSE": rmse_test, "R2": r2_test}
    logger.info(f"Avaliação no conjunto de teste - RMSE: {rmse_test:.4f}, R2: {r2_test:.4f}")
    
    # Salvar apenas os modelos treinados na pasta models
    caminho_modelo = os.path.join("models", "random_forest.pkl")
    save_model(best_model, caminho_modelo)
    
    # Salvar os melhores hiperparâmetros na pasta de relatórios
    best_params_path = os.path.join("reports", "model_training", "best_params.json")
    salvar_best_params(best_params, best_params_path)
    
    report_dir = os.path.join("reports", "model_training")
    os.makedirs(report_dir, exist_ok=True)
    gerar_relatorio_treinamento(best_params, os.path.join(report_dir, "model_training_report.txt"), test_metrics)
    
    logger.info("Treinamento do modelo concluído com sucesso.\nMódulo model_training executado com sucesso.")

if __name__ == "__main__":
    main()
