#!/usr/bin/env python
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
