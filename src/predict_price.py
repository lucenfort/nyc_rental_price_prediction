#!/usr/bin/env python
"""
predict_price.py
----------------
Este módulo carrega o modelo treinado e o scaler, realiza a preparação dos dados de entrada
seguindo o mesmo pipeline de engenharia de atributos, aplica a normalização e realiza a previsão do preço.
A previsão é revertida da transformação logarítmica para sugerir o preço em dólares.

Também inclui uma conversão de moeda para BRL (Real) e EUR (Euro) utilizando a API AwesomeAPI.
"""

import os
import joblib
import numpy as np
import pandas as pd
import logging
import requests

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def carregar_modelo(caminho: str):
    """
    Carrega o modelo treinado a partir do arquivo especificado.
    """
    try:
        model = joblib.load(caminho)
        logger.info(f"Modelo carregado com sucesso de: {caminho}")
        return model
    except Exception as e:
        logger.error(f"Erro ao carregar o modelo: {e}", exc_info=True)
        raise

def carregar_scaler(caminho: str):
    """
    Carrega o scaler salvo a partir do arquivo especificado.
    """
    try:
        scaler = joblib.load(caminho)
        logger.info(f"Scaler carregado com sucesso de: {caminho}")
        return scaler
    except Exception as e:
        logger.error(f"Erro ao carregar o scaler: {e}", exc_info=True)
        raise

def preparar_entrada(dados: dict, expected_columns: list, scaler) -> pd.DataFrame:
    """
    Prepara os dados de entrada para a previsão, aplicando o mesmo pipeline de transformação utilizado no treinamento.
    """
    # Verificar se as chaves essenciais estão presentes
    chaves_necessarias = ['bairro_group', 'room_type']
    for chave in chaves_necessarias:
        if chave not in dados:
            logger.warning(f"A chave '{chave}' não foi fornecida. Verifique os dados de entrada.")
    
    # Cria DataFrame a partir dos dados fornecidos
    df = pd.DataFrame([dados])
    # Remover colunas irrelevantes e vazadoras
    df = df.drop(columns=['nome', 'host_name', 'ultima_review', 'bairro', 'price', 'id', 'host_id'], errors='ignore')

    # Adicionar novas features com valores padrão se não existirem
    if 'densidade_imoveis' not in df.columns:
        df['densidade_imoveis'] = 1
    if 'proximidade_centro' not in df.columns:
        df['proximidade_centro'] = 0

    # Aplicar codificação one-hot para as colunas categóricas
    df = pd.get_dummies(df, columns=['bairro_group', 'room_type'], drop_first=True)

    # Reindexar para garantir que os dados tenham as mesmas colunas do conjunto de treinamento
    df = df.reindex(columns=expected_columns, fill_value=0)

    # Identificar as colunas numéricas que foram normalizadas durante o treinamento
    if hasattr(scaler, 'feature_names_in_'):
        numeric_cols = list(scaler.feature_names_in_)
        cols_to_scale = [col for col in numeric_cols if col in df.columns]
        if cols_to_scale:
            df[cols_to_scale] = scaler.transform(df[cols_to_scale])
            logger.info("Dados numéricos normalizados com sucesso.")
    else:
        logger.warning("O scaler não possui o atributo 'feature_names_in_'. Pulando a normalização.")
    
    return df

def prever_preco(modelo, X):
    """
    Realiza a previsão do preço utilizando o modelo e reverte a transformação logarítmica.
    """
    preco_log = modelo.predict(X)[0]
    return np.expm1(preco_log)

def converter_moedas(valor_usd):
    """
    Converte o valor previsto em USD para BRL e EUR utilizando a API AwesomeAPI.
    """
    try:
        # URL da API para obter as cotações de USD para BRL e EUR
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,USD-EUR"
        response = requests.get(url)
        data = response.json()

        # Obter as taxas de câmbio
        usd_brl = float(data['USDBRL']['bid'])
        usd_eur = float(data['USDEUR']['bid'])

        # Converter o valor previsto
        valor_brl = valor_usd * usd_brl
        valor_eur = valor_usd * usd_eur

        # Exibir os resultados com emojis
        print(f"\n🔹 == Conversão de Moedas == 🔹")
        print(f"💵 Valor previsto em USD:\t{valor_usd:.2f} $")
        print(f"🇧🇷💰 Valor convertido em BRL:\t{valor_brl:.2f} R$")
        print(f"💶 Valor convertido em EUR:\t{valor_eur:.2f} €\n")

    except Exception as e:
        print(f"❌ Erro ao converter moedas: {e}")

def main():
    logger.info("=== Executando predict_price.py ===")
    
    # Caminhos para o modelo e scaler treinados
    caminho_modelo = os.path.join("models", "random_forest.pkl")
    caminho_scaler = os.path.join("models", "scaler.pkl")
    modelo = carregar_modelo(caminho_modelo)
    scaler = carregar_scaler(caminho_scaler)
    
    # Carregar as colunas esperadas do conjunto de treinamento (exceto 'price_log')
    caminho_features = os.path.join("data", "final", "nyc_rental_data_features.csv")
    df_features = pd.read_csv(caminho_features)
    expected_columns = list(df_features.drop(columns=["price_log"]).columns)
    
    # Dados do apartamento a ser precificado
    apartamento = {
        'id': 2595,
        'nome': 'Skylit Midtown Castle',
        'host_id': 2845,
        'host_name': 'Jennifer',
        'bairro_group': 'Manhattan',
        'bairro': 'Midtown',
        'latitude': 40.75362,
        'longitude': -73.98377,
        'room_type': 'Entire home/apt',
        'minimo_noites': 1,
        'numero_de_reviews': 45,
        'ultima_review': '2019-05-21',
        'reviews_por_mes': 0.38,
        'calculado_host_listings_count': 2,
        'disponibilidade_365': 355
    }
    
    # Preparar os dados de entrada com normalização e pipeline de transformação
    X = preparar_entrada(apartamento, expected_columns, scaler)
    
    # Realizar a previsão e converter de log(price) para price
    preco_sugerido = prever_preco(modelo, X)
    
    logger.info(f"🏡 Preço sugerido para '{apartamento['nome']}': **${preco_sugerido:.2f}**")
    
    # Converter o valor previsto para BRL e EUR
    converter_moedas(preco_sugerido)

    logger.info("✅ Módulo predict_price executado com sucesso.")

if __name__ == "__main__":
    main()
