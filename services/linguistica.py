"""
    Processamento de prompt para palavras
"""
import language_tool_python
from repositorios.nome_rep import Nomes

nomes = Nomes().nomes
tool = language_tool_python.LanguageTool('pt-BR')

def correcao(texto):
    palavras = texto.split()
    resultado = []

    for palavra in palavras:
        if palavra in nomes:
            resultado.append(palavra)
        else:
            resultado.append(tool.correct(palavra))
    
    return " ".join(resultado)