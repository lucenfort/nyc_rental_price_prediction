#!/usr/bin/env python
import os
import pandas as pd
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def carregar_dados(caminho: str) -> pd.DataFrame:
    """
    Carrega os dados a partir de um arquivo CSV.
    """
    try:
        df = pd.read_csv(caminho)
        logger.info(f"Dados carregados com sucesso de: {caminho}")
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar o arquivo '{caminho}': {e}", exc_info=True)
        raise

def tratar_valores_ausentes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata os valores ausentes, preenchendo com a mediana para colunas numéricas e moda para colunas categóricas.
    """
    df = df.copy()
    for coluna in df.columns:
        if df[coluna].dtype in ['float64', 'int64']:
            df[coluna] = df[coluna].fillna(df[coluna].median())
        else:
            df[coluna] = df[coluna].fillna(df[coluna].mode()[0])
    logger.info("Valores ausentes tratados com sucesso.")
    return df

def remover_outliers(df: pd.DataFrame, coluna: str, fator: float = 1.5) -> pd.DataFrame:
    """
    Remove outliers utilizando o método do intervalo interquartil (IQR).

    Parâmetros:
    - df: DataFrame a ser processado.
    - coluna: Coluna sobre a qual a remoção de outliers será aplicada.
    - fator: Multiplicador do IQR para definir os limites (default é 1.5).
    """
    Q1 = df[coluna].quantile(0.25)
    Q3 = df[coluna].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - fator * IQR
    limite_superior = Q3 + fator * IQR
    filtro = (df[coluna] >= limite_inferior) & (df[coluna] <= limite_superior)
    logger.info(f"Outliers removidos na coluna '{coluna}' utilizando fator {fator}.")
    return df.loc[filtro]

def salvar_dados(df: pd.DataFrame, caminho: str) -> None:
    """
    Salva o DataFrame em um arquivo CSV no caminho especificado.
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    df.to_csv(caminho, index=False)
    logger.info(f"Dados processados salvos com sucesso em: {caminho}")

def gerar_relatorio(df: pd.DataFrame, caminho_report: str) -> None:
    """
    Gera um relatório TXT contendo o resumo do pré-processamento.
    """
    with open(caminho_report, 'w', encoding='utf-8') as f:
        f.write("RELATÓRIO DE PRÉ-PROCESSAMENTO\n")
        f.write("-------------------------------\n")
        f.write(f"Dimensões do dataset: {df.shape}\n")
        f.write("Colunas e tipos:\n")
        f.write(df.dtypes.to_string())
    logger.info(f"Relatório de pré-processamento gerado em: {caminho_report}")

def main():
    logger.info("=== Executando data_processing.py ===")
    caminho_entrada = os.path.join("data", "raw", "teste_indicium_precificacao.csv")
    caminho_saida = os.path.join("data", "processed", "nyc_rental_data_processed.csv")
    df = carregar_dados(caminho_entrada)
    df = tratar_valores_ausentes(df)
    df = remover_outliers(df, "price", fator=1.5)
    salvar_dados(df, caminho_saida)
    
    report_dir = os.path.join("reports", "data_processing")
    os.makedirs(report_dir, exist_ok=True)
    gerar_relatorio(df, os.path.join(report_dir, "data_processing_report.txt"))
    
    logger.info("Processamento de dados concluído com sucesso.\nMódulo data_processing executado com sucesso.")

if __name__ == "__main__":
    main()
