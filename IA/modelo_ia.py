from IA.config import (OLLAMA_API_DEEPSEEK_R1,OLLAMA_API_DEEPSEEK_V3,OLLAMA_API_QWEN3_CODER)

MODELOS = {
    "deepseek_r1": OLLAMA_API_DEEPSEEK_R1,
    "deepseek_v3": OLLAMA_API_DEEPSEEK_V3,
    "qwen_coder": OLLAMA_API_QWEN3_CODER
}

def obter_modelo(nome):
    return MODELOS[nome]