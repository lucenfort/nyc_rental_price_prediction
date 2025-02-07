import os
import warnings
from io import StringIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo '{filepath}': {e}")
        raise


def resumo_dados(df: pd.DataFrame) -> None:
    print("=== Resumo dos Dados ===")
    print("\nInformações Gerais:")
    print(df.info())
    print("\nPrimeiras Linhas do Dataset:")
    print(df.head())
    print("\nResumo Estatístico (incluindo variáveis categóricas):")
    print(df.describe(include='all'))


def analise_valores_ausentes(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isnull().sum().reset_index()
    missing.columns = ['Coluna', 'Valores Ausentes']
    print("\n=== Valores Ausentes por Coluna ===")
    print(missing)
    return missing


def plot_histograma(df: pd.DataFrame, coluna: str, bins: int = 30, save_path: str = None) -> None:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[coluna].dropna(), bins=bins, kde=True, color='skyblue')
    plt.title(f"Distribuição de '{coluna}'", fontsize=14)
    plt.xlabel(coluna, fontsize=12)
    plt.ylabel("Frequência", fontsize=12)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()


def plot_boxplot(df: pd.DataFrame, coluna: str, save_path: str = None) -> None:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=df[coluna].dropna(), color='lightgreen')
    plt.title(f"Boxplot de '{coluna}'", fontsize=14)
    plt.xlabel(coluna, fontsize=12)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()


def plot_barplot_room_type(df: pd.DataFrame, save_path: str = None) -> None:
    plt.figure(figsize=(8, 6))
    ordem = df['room_type'].value_counts().index
    sns.countplot(x='room_type', data=df, order=ordem, palette='Set2')
    plt.title("Distribuição dos Tipos de Quarto", fontsize=14)
    plt.xlabel("Tipo de Quarto", fontsize=12)
    plt.ylabel("Contagem", fontsize=12)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()


def plot_geographical(df: pd.DataFrame, save_path: str = None) -> None:
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='longitude', y='latitude', hue='bairro_group',
                    data=df, palette='viridis', alpha=0.6, edgecolor=None)
    plt.title("Distribuição Geográfica dos Imóveis", fontsize=14)
    plt.xlabel("Longitude", fontsize=12)
    plt.ylabel("Latitude", fontsize=12)
    plt.legend(title="Bairro Group", loc='best', fontsize=9)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()


def plot_correlacao(df: pd.DataFrame, save_path: str = None) -> None:
    plt.figure(figsize=(12, 10))
    colunas_numericas = df.select_dtypes(include=[np.number])
    correlacao = colunas_numericas.corr()
    sns.heatmap(correlacao, annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("Matriz de Correlação das Variáveis Numéricas", fontsize=14)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()


def gerar_relatorio_txt(df: pd.DataFrame, missing: pd.DataFrame, caminho_report: str) -> None:
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    desc = df.describe(include='all').to_string()
    missing_str = missing.to_string(index=False)
    texto_relatorio = (
        "RELATÓRIO DE ANÁLISE EXPLORATÓRIA DE DADOS (EDA)\n"
        "--------------------------------------------------\n\n"
        "1. Introdução\n"
        "Este relatório apresenta os dados extraídos da análise exploratória do dataset 'teste_indicium_precificacao.csv'.\n"
        f"O dataset possui {df.shape[0]} registros e {df.shape[1]} colunas.\n\n"
        "2. Estrutura dos Dados\n\n"
        "2.1 Informações Gerais:\n"
        f"{info_str}\n\n"
        "2.2 Valores Ausentes:\n"
        f"{missing_str}\n\n"
        "3. Estatísticas Descritivas:\n"
        f"{desc}\n\n"
        "4. Gráficos Gerados\n"
        "Os gráficos foram salvos no diretório 'reports/eda/figures'.\n"
    )
    with open(caminho_report, 'w', encoding='utf-8') as f:
        f.write(texto_relatorio)
    print(f"\nRelatório EDA gerado com sucesso: {caminho_report}")


def main():
    warnings.filterwarnings("ignore")
    caminho_arquivo = os.path.join("data", "raw", "teste_indicium_precificacao.csv")
    df = load_data(caminho_arquivo)
    resumo_dados(df)
    missing = analise_valores_ausentes(df)
    caminho_figures = os.path.join("reports", "eda", "figures")
    caminho_relatorios = os.path.join("reports", "eda", "relatorios")
    os.makedirs(caminho_figures, exist_ok=True)
    os.makedirs(caminho_relatorios, exist_ok=True)
    sns.set(style="whitegrid", context="notebook")
    
    # Gráficos de variáveis numéricas
    plot_histograma(df, "price", bins=50, save_path=os.path.join(caminho_figures, "eda_distribuicao_price.png"))
    plot_boxplot(df, "price", save_path=os.path.join(caminho_figures, "eda_boxplot_price.png"))
    plot_histograma(df, "minimo_noites", bins=50, save_path=os.path.join(caminho_figures, "eda_distribuicao_minimo_noites.png"))
    plot_boxplot(df, "minimo_noites", save_path=os.path.join(caminho_figures, "eda_boxplot_minimo_noites.png"))
    plot_barplot_room_type(df, save_path=os.path.join(caminho_figures, "eda_barras_room_type.png"))
    plot_geographical(df, save_path=os.path.join(caminho_figures, "eda_distribuicao_geografica.png"))
    plot_correlacao(df, save_path=os.path.join(caminho_figures, "eda_matriz_correlacao.png"))
    
    # Análise da transformação do target
    df["price_log"] = np.log1p(df["price"])
    plot_histograma(df, "price_log", bins=50, save_path=os.path.join(caminho_figures, "eda_distribuicao_price_log.png"))
    plot_boxplot(df, "price_log", save_path=os.path.join(caminho_figures, "eda_boxplot_price_log.png"))
    
    caminho_relatorio = os.path.join(caminho_relatorios, "eda_relatorio.txt")
    gerar_relatorio_txt(df, missing, caminho_relatorio)
    print("\nAnálise Exploratória (EDA) concluída com sucesso!")


if __name__ == '__main__':
    print(f"\n=== Executando eda.py ===")
    main()
