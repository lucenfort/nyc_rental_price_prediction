#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import logging
import math

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def carregar_dados(caminho: str) -> pd.DataFrame:
    """
    Carrega os dados a partir de um arquivo CSV.
    """
    df = pd.read_csv(caminho)
    logger.info(f"Dados carregados com sucesso de: {caminho}")
    return df

def calcular_proximidade_centro(df: pd.DataFrame) -> pd.Series:
    """
    Calcula a proximidade do ponto dado com o centro de Nova York (coordenadas: 40.7128, -74.0060) utilizando a fórmula de Haversine.
    Se as colunas 'latitude' e 'longitude' não existirem, retorna uma série de zeros.
    """
    if 'latitude' in df.columns and 'longitude' in df.columns:
        # Coordenadas do centro de Nova York
        lat_centro = 40.7128
        lon_centro = -74.0060
        
        # Converter graus para radianos
        lat1 = np.radians(df['latitude'])
        lon1 = np.radians(df['longitude'])
        lat2 = math.radians(lat_centro)
        lon2 = math.radians(lon_centro)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        # Raio da Terra em quilômetros
        raio = 6371
        distancia = c * raio
        logger.info("Feature 'proximidade_centro' calculada utilizando a fórmula de Haversine.")
        return distancia
    else:
        logger.warning("Colunas 'latitude' e 'longitude' não encontradas. 'proximidade_centro' definido como 0.")
        return pd.Series(0, index=df.index)

def criar_novas_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria novas features no dataset.
    - densidade_imoveis: Número de imóveis por bairro.
    - proximidade_centro: Distância do imóvel ao centro de Nova York.
    """
    df = df.copy()
    if 'bairro' in df.columns:
        df["densidade_imoveis"] = df.groupby("bairro")["bairro"].transform("count")
    else:
        df["densidade_imoveis"] = 1
        logger.warning("Coluna 'bairro' não encontrada. 'densidade_imoveis' definido como 1 para todos os registros.")
    
    df["proximidade_centro"] = calcular_proximidade_centro(df)
    logger.info("Novas features criadas com sucesso.")
    return df

def codificar_variaveis_categoricas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Codifica variáveis categóricas com baixa cardinalidade utilizando one-hot encoding.
    Exclui as colunas: 'nome', 'host_name', 'ultima_review', 'bairro'.
    """
    colunas_para_codificar = []
    for coluna in df.select_dtypes(include=["object"]).columns:
        if coluna not in ['nome', 'host_name', 'ultima_review', 'bairro']:
            if df[coluna].nunique() < 50:
                colunas_para_codificar.append(coluna)
    if colunas_para_codificar:
        df = pd.get_dummies(df, columns=colunas_para_codificar, drop_first=True)
        logger.info(f"Variáveis categóricas codificadas: {colunas_para_codificar}")
    else:
        logger.info("Nenhuma variável categórica para codificar foi encontrada.")
    return df

def transformar_variavel_alvo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma a variável alvo 'price' utilizando log1p e cria a coluna 'price_log'.
    """
    df = df.copy()
    df["price_log"] = np.log1p(df["price"])
    logger.info("Variável alvo transformada para 'price_log'.")
    return df

def excluir_colunas_irrelevantes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Exclui colunas irrelevantes que podem causar vazamento de informação.
    """
    colunas_para_excluir = ['nome', 'host_name', 'ultima_review', 'bairro', 'price', 'id', 'host_id']
    df = df.drop(columns=colunas_para_excluir, errors='ignore')
    logger.info(f"Colunas irrelevantes removidas: {colunas_para_excluir}")
    return df

def normalizar_variaveis_numericas(df: pd.DataFrame) -> (pd.DataFrame, StandardScaler):
    """
    Normaliza variáveis numéricas (exceto 'price_log') utilizando StandardScaler.
    """
    colunas_numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    if 'price_log' in colunas_numericas:
        colunas_numericas.remove('price_log')
    scaler = StandardScaler()
    df[colunas_numericas] = scaler.fit_transform(df[colunas_numericas])
    logger.info("Variáveis numéricas normalizadas com sucesso.")
    return df, scaler

def salvar_dados(df: pd.DataFrame, caminho: str) -> None:
    """
    Salva o DataFrame em um arquivo CSV no caminho especificado.
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    df.to_csv(caminho, index=False)
    logger.info(f"Dados com novas features salvos com sucesso em: {caminho}")

def gerar_relatorio(df: pd.DataFrame, caminho_report: str) -> None:
    """
    Gera um relatório TXT contendo o resumo da engenharia de atributos.
    """
    with open(caminho_report, 'w', encoding='utf-8') as f:
        f.write("RELATÓRIO DE ENGENHARIA DE ATRIBUTOS\n")
        f.write("------------------------------------\n")
        f.write(f"Dimensões do dataset após feature engineering: {df.shape}\n")
        f.write("Estatísticas descritivas:\n")
        f.write(df.describe().to_string())
    logger.info(f"Relatório de engenharia de atributos gerado em: {caminho_report}")

def main():
    logger.info("=== Executando feature_engineering.py ===")
    caminho_entrada = os.path.join("data", "processed", "nyc_rental_data_processed.csv")
    caminho_saida = os.path.join("data", "final", "nyc_rental_data_features.csv")
    df = carregar_dados(caminho_entrada)
    df = criar_novas_features(df)
    df = codificar_variaveis_categoricas(df)
    df = transformar_variavel_alvo(df)   # Calcular price_log antes de remover price
    df = excluir_colunas_irrelevantes(df)  # Remover colunas vazadoras agora que price_log foi calculado
    df, scaler = normalizar_variaveis_numericas(df)
    salvar_dados(df, caminho_saida)
    
    report_dir = os.path.join("reports", "feature_engineering")
    os.makedirs(report_dir, exist_ok=True)
    gerar_relatorio(df, os.path.join(report_dir, "feature_engineering_report.txt"))
    
    # Salvar o scaler para uso em previsões
    os.makedirs("models", exist_ok=True)
    joblib.dump(scaler, os.path.join("models", "scaler.pkl"))
    logger.info("Scaler salvo com sucesso em: models/scaler.pkl")
    
    logger.info("Engenharia de atributos concluída com sucesso.\nMódulo feature_engineering executado com sucesso.")

if __name__ == "__main__":
    main()
