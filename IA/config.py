"""
Este módulo contém a configuração que vai para IA.
"""
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"  # URL do servidor Ollama
OLLAMA_HEADERS = {"Content-Type": "application/json"}
AI_CONFIG = { 
    "max_historico": 10, #Numero de mensagens anterioes a se considerar 
    "temperatura": 0.7, #criatividade da IA (se usar modelo real depois) 
    "max_tokens": 512 #maximo de tokens a serem retornados (se usar modelo real depois)
}
OLLAMA_MODEL = "deepseek-r1"  # Nome do modelo Ollama a ser usado