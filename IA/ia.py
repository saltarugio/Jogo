import requests
import json
import re
from IA.config import OLLAMA_API_DEEPSEEK_V3, OLLAMA_API_QWEN3_CODER, OLLAMA_API_DEEPSEEK_R1
import unicodedata

MODELO_ESCOLHIDO = "deepseekv3" # Opções: "deepseekv3", "qwen3", "deepseekr1"
if MODELO_ESCOLHIDO == "deepseekv3":
    OLLAMA_URL = OLLAMA_API_DEEPSEEK_V3["OLLAMA_URL"]
    OLLAMA_HEADERS = OLLAMA_API_DEEPSEEK_V3["OLLAMA_HEADERS"]
    OLLAMA_CONFIG = OLLAMA_API_DEEPSEEK_V3
elif MODELO_ESCOLHIDO == "qwen3":
    OLLAMA_URL = OLLAMA_API_QWEN3_CODER["OLLAMA_URL"]
    OLLAMA_HEADERS = OLLAMA_API_QWEN3_CODER["OLLAMA_HEADERS"]
    OLLAMA_CONFIG = OLLAMA_API_QWEN3_CODER
elif MODELO_ESCOLHIDO == "deepseekr1":
    OLLAMA_URL = OLLAMA_API_DEEPSEEK_R1["OLLAMA_URL"]
    OLLAMA_HEADERS = OLLAMA_API_DEEPSEEK_R1["OLLAMA_HEADERS"]
    OLLAMA_CONFIG = OLLAMA_API_DEEPSEEK_R1

def remover_acentos(texto: str) -> str:
    """Converte caracteres acentuados para suas formas não acentuadas."""
    nfkd_form = unicodedata.normalize('NFD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def limpar_resposta_final(texto: str) -> str:
    """Limpeza pesada (incluindo remoção de acentos) para o texto FINAL."""
    # Remove blocos <think>...</think>
    texto = re.sub(r"<think.*?</think>", "", texto, flags=re.DOTALL | re.IGNORECASE)

    # Remove "Hmm..." ou repetições iniciais
    texto = re.sub(r"^(Hmm+|Ah+|Uh+)[. ]*", "", texto, flags=re.IGNORECASE)

    # Remove marcações internas
    lixo = ["Thinking...", "...done thinking.", "<think>", "</think>"]
    for l in lixo:
        texto = texto.replace(l, "")

    # NOVIDADE: Chama a função para remover acentos
    texto = remover_acentos(texto)
    
    # Remove caracteres inválidos (agora sem acentos)
    texto = re.sub(r"[^\w\s.,!?;:()-]", "", texto, flags=re.UNICODE) 

    # Evita respostas idênticas repetidas (loop)
    linhas = list(dict.fromkeys(texto.splitlines()))
    texto = " ".join(linhas)

    return texto.strip()


class DeepSeekIA:
    @staticmethod
    def gerar_resposta(npc, usuario, historico, prompt, mapa):
        # Limitar histórico
        if len(historico) > OLLAMA_CONFIG["MAX_HISTORICO"]:
            historico = historico[-OLLAMA_CONFIG["MAX_HISTORICO"]:]

        # Montar contexto
        # ... (código mantido, pois não é o foco do problema)
        if isinstance(historico, list) and len(historico) > 0 and isinstance(historico[0], dict):
            historico = [f"{k}: {v}" for msg in historico for k, v in msg.items()]
        contexto = "\n".join(historico)

        # Prompt otimizado: Remova o excesso de formatação do terminal
        entrada = (
            f"### SYSTEM INSTRUCTIONS ###\n"
            f"REGRA INEGOCIÁVEL 1: Responda SEMPRE, EXCLUSIVAMENTE e APENAS em PORTUGUÊS BRASILEIRO.\n"
            f"REGRA INEGOCIÁVEL 2: NUNCA gere ou use caracteres chineses, símbolos ou qualquer outro idioma.\n"
            f"REGRA DE CONTEÚDO: Sua resposta deve conter SOMENTE a fala do NPC. NUNCA gere blocos de raciocínio como <think>...</think> ou qualquer anotação entre parênteses. NUNCA descreva ações ou emoções (ex: *sorri*, (pensando)).\n"
            f"Você é o NPC {npc.nome}. Sua única tarefa é responder ao Jogador.\n"
            f"- Mantenha a personalidade: {npc.personalidade}.\n"
            f"- Considere a história: {npc.historia_pessoal}.\n"
            f"- Local: {mapa.nome}: {mapa.descricao}\n" # Assumindo que você tem um campo 'mapa' no seu objeto Usuario
            f"- REGRA PRINCIPAL: Responda APENAS o que o NPC diria. Nunca mostre raciocínio interno.\n"
            f"- REGRA DE FORMATO: Responda em 1 a 3 frases curtas. Não repita a pergunta do Jogador.\n"
            f"- REGRA DE CONTEXTO: Caso a pergunta do Jogador não tenha relação com o contexto, responda que não tem conhecimento sobre o assunto, mantendo a personalidade do NPC.\n"
            f"### END INSTRUCTIONS ###\n\n"
            
            f"### DIALOG HISTORY ###\n"
            f"{contexto}\n"
            f"### END HISTORY ###\n\n"
            
            f"{usuario} diz: {prompt}\n"
            f"{npc.nome}: " # O modelo deve preencher a partir daqui
        )
        
        # Crie o payload com base na documentação
        payload = {
            "model": OLLAMA_CONFIG["MODEL_NAME"],
            "messages": [{"role": "user", "content": entrada}],
            "stream": False,
            "options": {
                "temperature": OLLAMA_CONFIG["TEMPERATURE"],
                "num_ctx": OLLAMA_CONFIG["MAX_TOKENS"],
                "repeat_penalty": OLLAMA_CONFIG["REPEAT_PENALTY"],
            }
        }
        try:
            # Requisição SEM stream=True e SEM o parâmetro stream=True no requests.post
            response = requests.post(OLLAMA_URL, headers=OLLAMA_HEADERS, data=json.dumps(payload))
            response.raise_for_status() # Levanta erro para códigos de status HTTP ruins
            
            # 1. Obtém o JSON completo
            data = response.json()
                
            # 2. Extrai o conteúdo da resposta de uma só vez
            resposta_completa = data["choices"][0]["message"]["content"]
                
            # 3. Aplica a limpeza pesada (remove tags, acentos, formata)
            resposta_final = limpar_resposta_final(resposta_completa)

            # Anti-loop
            if resposta_final.lower().strip() == remover_acentos(prompt).lower().strip():
                resposta_final = f"{remover_acentos(npc.nome)} parece pensativo, mas decide mudar de assunto."

            return resposta_final
        
        except requests.exceptions.HTTPError as e:
            return None
        
        except Exception as e:
            return None