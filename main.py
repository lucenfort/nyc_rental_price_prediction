"""
main.py
-------
Este script orquestra a execução de todas as etapas do pipeline:
  1. EDA
  2. Processamento de Dados
  3. Engenharia de Atributos
  4. Treinamento dos Modelos
  5. Avaliação do Modelo

Cada módulo é executado de forma ordenada utilizando o interpretador Python.
Caso alguma etapa apresente erro, o pipeline será interrompido para facilitar a depuração.
"""

import os
import subprocess
import sys


def run_module(module_name: str) -> None:
    module_path = os.path.join("src", module_name + ".py")
    result = subprocess.run([sys.executable, module_path])
    if result.returncode != 0:
        print(f"Erro na execução do módulo {module_name}.")
        sys.exit(result.returncode)
    else:
        print(f"Módulo {module_name} executado com sucesso.")

def main() -> None:
    etapas = ["eda", "data_processing", "feature_engineering", "model_training", "evaluation", "predict_price"]
    print("Iniciando execução do pipeline completo...\n")
    for etapa in etapas:
        run_module(etapa)
    print("\nPipeline completo executado com sucesso!")

if __name__ == '__main__':
    main()