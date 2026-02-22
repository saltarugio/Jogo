"""
    Centralização da leitura do arquivo de abrviação
"""
import json
import os
def caminho():
    diretorio_atual = os.path.dirname(__file__)
    caminho_json = os.path.join(diretorio_atual, "abreviacoes.json")

    try:
        with open(caminho_json, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON")

    except FileNotFoundError:
        print("Arquivo não encontrado")

    return {}  # evita None e previne erros depois
