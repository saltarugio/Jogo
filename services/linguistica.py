"""
    Processamento de prompt para palavras
"""
import language_tool_python

tool = language_tool_python.LanguageTool('pt-BR')

def correcao(texto):
    corrigido = tool.correct(texto)
    
    return corrigido