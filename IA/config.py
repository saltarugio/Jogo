"""
Este módulo contém a configuração que vai para IA.
"""
# config.py

OLLAMA_API_DEEPSEEK_R1 = {
    "OLLAMA_URL": "http://localhost:11434/v1/chat/completions",
    "OLLAMA_HEADERS": {"Content-Type": "application/json"},
    "MODEL_NAME": "deepseek-r1:8b",
     # Parâmetros que serão enviados diretamente no payload
    "MAX_HISTORICO": 10,
    "TEMPERATURE": 0.7,
    "MAX_TOKENS": 512,
    "MIRASAT": False,
    "REPEAT_PENALTY": 1.1
}

OLLAMA_API_DEEPSEEK_V3 = {
    "OLLAMA_URL": "http://localhost:11434/v1/chat/completions",
    "OLLAMA_HEADERS": {"Content-Type": "application/json"},
    "MODEL_NAME": "deepseek-v3.1:671b-cloud",
    # Parâmetros que serão enviados diretamente no payload
    "MAX_HISTORICO": 10,
    "TEMPERATURE": 0.7,
    "MAX_TOKENS": 512,
    "MIRASAT": False,
    "REPEAT_PENALTY": 1.1
}

OLLAMA_API_QWEN3_CODER = {
    "OLLAMA_URL": "http://localhost:11434/v1/chat/completions",
    "OLLAMA_HEADERS": {"Content-Type": "application/json"},
    "MODEL_NAME": "qwen3-coder:480b-cloud",
    # Parâmetros que serão enviados diretamente no payload
    "MAX_HISTORICO": 10,
    "TEMPERATURE": 0.7,
    "MAX_TOKENS": 512,
    "MIRASAT": False,
    "REPEAT_PENALTY": 1.1
}