import requests
<<<<<<< HEAD
from IA.config import OLLAMA_API_DEEPSEEK_V3, OLLAMA_API_QWEN3_CODER, OLLAMA_API_DEEPSEEK_R1
from rich.console import Console



=======
import json
import re
from IA.config import OLLAMA_API_DEEPSEEK_V3, OLLAMA_API_QWEN3_CODER, OLLAMA_API_DEEPSEEK_R1
import unicodedata
from rich.console import Console

>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac
console = Console()


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

<<<<<<< HEAD
=======
def remover_acentos(texto: str) -> str:
    """Converte caracteres acentuados para suas formas não acentuadas."""
    nfkd_form = unicodedata.normalize('NFD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def limpar_resposta_final(texto: str) -> str:
    """Limpeza pesada (incluindo remoção de acentos) para o texto FINAL."""
    # Remove blocos <think>...</think>
    texto = re.sub(r"<think.*?</think>", "", texto, flags=re.DOTALL | re.IGNORECASE)

    # Remove "Hmm..." ou repetições iniciais
    # texto = re.sub(r"^(Hmm+|Ah+|Uh+)[. ]*", "", texto, flags=re.IGNORECASE)

    # Remove marcações internas
    lixo = ["Thinking...", "...done thinking.", "<think>", "</think>"]
    for l in lixo:
        texto = texto.replace(l, "")

    # # NOVIDADE: Chama a função para remover acentos
    # texto = remover_acentos(texto)
    
    # # Remove caracteres inválidos (agora sem acentos)
    # texto = re.sub(r"[^\w\s.,!?;:()-]", "", texto, flags=re.UNICODE) 

    # Evita respostas idênticas repetidas (loop)
    linhas = list(dict.fromkeys(texto.splitlines()))
    texto = "\n".join(linhas)

    return texto.strip()

>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac

class DeepSeekIA:
    @staticmethod
    def gerar_resposta(npc, usuario, historico, prompt, mapa, contexto_parametros):
        # Limitar histórico
        if len(historico) > OLLAMA_CONFIG["MAX_HISTORICO"]:
            historico = historico[-OLLAMA_CONFIG["MAX_HISTORICO"]:]

        # Montar contexto
        # ... (código mantido, pois não é o foco do problema)
        if isinstance(historico, list) and len(historico) > 0 and isinstance(historico[0], dict):
            historico = [f"{k}: {v}" for msg in historico for k, v in msg.items()]
        contexto = "\n".join(historico)

        # Prompt otimizado: Remova o excesso de formatação do terminal
<<<<<<< HEAD
        entrada = f"""
            ### SYSTEM INSTRUCTIONS ###
            REGRA ABSOLUTA:
            - Responda EXCLUSIVAMENTE em português brasileiro
            - Nunca mencione IA, modelo ou sistema
            - Nunca use outros idiomas ou símbolos estranhos
            - Responda SEMPRE como o NPC, dentro do universo do jogo

            Você é o NPC {npc.nome}.

            Identidade do NPC:
            - Personalidade: {npc.personalidade}
            - História: {npc.historia_pessoal}
            - Local atual: {mapa.nome} — {mapa.descricao}

            Comportamento:
            - Responda APENAS com fala direta
            - Não descreva ações, emoções internas ou pensamentos
            - Não use aspas, colchetes ou parênteses
            - Não seja narrador

            Uso do estado emocional:
            {contexto_parametros}

            Formato da resposta:
            - Entre 1 e 3 frases curtas
            - Tom coerente com a personalidade e o estado emocional

            ### HISTÓRICO DE DIÁLOGO ###
            {contexto}
            ### FIM DO HISTÓRICO ###

            Fala do jogador:
            {usuario}: {prompt}

            Resposta do NPC:
            """

=======
        entrada = (
            f"### SYSTEM INSTRUCTIONS ###\n"
            f"REGRA INEGOCIÁVEL 1: Responda SEMPRE, EXCLUSIVAMENTE e APENAS em PORTUGUÊS BRASILEIRO.\n"
            f"REGRA INEGOCIÁVEL 2: NUNCA gere ou use caracteres chineses, símbolos ou qualquer outro idioma.\n"
            f"REGRA INEGOCIÁVEL 3: NUNCA mencione que você é uma IA, um modelo de linguagem ou similar.\n"
            f"REGRA INEGOCIÁVEL 4: SEMPRE responda como se fosse o NPC, dentro do universo do jogo.\n"
            f"REGRA DE CONTEÚDO: Sua resposta deve conter SOMENTE a fala do NPC. NUNCA gere blocos de raciocínio como <think>...</think> ou qualquer anotação entre parênteses. NUNCA descreva ações ou emoções (ex: *sorri*, (pensando)).\n"
            f"Você é o NPC {npc.nome}. Sua única tarefa é responder ao Jogador.\n"
            f"- Mantenha a personalidade: {npc.personalidade}.\n"
            f"- Considere a história: {npc.historia_pessoal}.\n"
            f"- Local: {mapa.nome}: {mapa.descricao}\n"
            f"- REGRA PRINCIPAL: Responda APENAS o que o NPC diria. Nunca mostre raciocínio interno.\n"
            f"- REGRA DE FORMATO: Responda em 1 a 3 frases curtas. Não repita a pergunta do Jogador.\n"
            f"- REGRA DE CONTEXTO: Caso a pergunta do Jogador não tenha relação com o contexto, responda que não tem conhecimento sobre o assunto, mantendo a personalidade do NPC.\n"
            f"- REGRA DE CONTEÚDO FORA DE CONTEXTO: Responda algo do tipo: 'Desculpe, não tenho conhecimento sobre isso.' ou 'Não sei nada sobre esse assunto.' ou '...' ou 'Isso não faz parte do meu conhecimento.'\n"
            f"- Contexto adicional (parâmetros IA): {contexto_parametros}\n"
            f"### END INSTRUCTIONS ###\n\n"
            
            f"### DIALOG HISTORY ###\n"
            f"{contexto}\n"
            f"### END HISTORY ###\n\n"
            
            f"{usuario} diz: {prompt}\n"
            f"{npc.nome}: "
        )
        
>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac
        # Crie o payload com base na documentação
        payload = {
            "model": OLLAMA_CONFIG["MODEL_NAME"],
            "messages": [{"role": "user", "content": entrada}],
            "stream": False,
            "options": {
                "temperature": OLLAMA_CONFIG["TEMPERATURE"],
<<<<<<< HEAD
                "num_predict": OLLAMA_CONFIG["MAX_TOKENS"],
=======
                "num_ctx": OLLAMA_CONFIG["MAX_TOKENS"],
>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac
                "repeat_penalty": OLLAMA_CONFIG["REPEAT_PENALTY"],
            }
        }
        try:
            # Requisição SEM stream=True e SEM o parâmetro stream=True no requests.post
<<<<<<< HEAD
            response = requests.post(OLLAMA_URL, headers=OLLAMA_HEADERS, json=payload)
=======
            response = requests.post(OLLAMA_URL, headers=OLLAMA_HEADERS, data=json.dumps(payload))
>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac
            response.raise_for_status() # Levanta erro para códigos de status HTTP ruins
            
            # 1. Obtém o JSON completo
            data = response.json()
                
            # 2. Extrai o conteúdo da resposta de uma só vez
<<<<<<< HEAD
            resposta_completa = data["message"]["content"]
            return resposta_completa
=======
            resposta_completa = data["choices"][0]["message"]["content"]
                
            # 3. Aplica a limpeza pesada (remove tags, acentos, formata)
            resposta_final = limpar_resposta_final(resposta_completa)

            # Anti-loop
            if resposta_final.lower().strip() == remover_acentos(prompt).lower().strip():
                resposta_final = f"{remover_acentos(npc.nome)} parece pensativo, mas decide mudar de assunto."

            return resposta_final
>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac
        
        except requests.exceptions.HTTPError as e:
            return None
        
        except Exception as e:
            return None
    
    @staticmethod
    def avaliacao_emocional(npc, usuario, prompt, mapa):
<<<<<<< HEAD
        # entrada = (
        #     f"### SYSTEM INSTRUCTIONS ###\n"
        #     f"Você é um sistema de avaliação emocional para NPCs em um jogo. Sua tarefa é analisar a interação entre o Jogador e o NPC e fornecer uma avaliação emocional quantitativa.\n"
        #     f"- Considere os seguintes parâmetros: proximidade, reputação, lealdade, hostilidade.\n"
        #     f"- Cada parâmetro deve ser avaliado em uma escala de -2 a +2, onde:\n"
        #     f"  - -2 indica uma mudança muito negativa,\n"
        #     f"  - -1 indica uma mudança negativa,\n"
        #     f"  - 0 indica nenhuma mudança,\n"
        #     f"  - +1 indica uma mudança positiva,\n"
        #     f"  - +2 indica uma mudança muito positiva.\n"
        #     f"- Forneça uma justificativa breve para cada avaliação.\n"
        #     f"- Responda no seguinte formato JSON:\n"
        #     f'{{"proximidade": int, "reputacao": int, "lealdade": int, "hostilidade": int, "justificativa": "string"}}\n'
        #     f"- REGRA INEGOCIÁVEL: NUNCA use caracteres chineses, símbolos ou qualquer outro idioma. Responda EXCLUSIVAMENTE em PORTUGUÊS BRASILEIRO.\n"
        #     f"- REGRA INEGOCIÁVEL: NUNCA mencione que você é uma IA ou modelo de linguagem.\n"
        #     f"### END INSTRUCTIONS ###\n\n"
            
        #     f"O Jogador {usuario} disse ao NPC {npc.nome}: {prompt}\n"
        #     f"Contexto do NPC: {npc.personalidade}. História: {npc.historia_pessoal}. Local: {mapa.nome}: {mapa.descricao}\n\n"
        #     f"Forneça sua avaliação emocional agora."
        # )
        entrada = f"""
            ### SYSTEM INSTRUCTIONS ###
            Você é um sistema de avaliação emocional para NPCs em um jogo.
            
            Tarefa:
            - Avaliar a interação entre Jogador e NPC
            - Retornar alterações emocionais quantitativas

            Parâmetros:
            - proximidade
            - reputacao
            - lealdade
            - hostilidade

            Escala (obrigatória):
            - -2 = mudança muito negativa
            - -1 = mudança negativa
            -  0 = nenhuma mudança
            - +1 = mudança positiva
            - +2 = mudança muito positiva

            Regras:
            - Responder SOMENTE em JSON válido
            - Usar APENAS português brasileiro
            - Não usar símbolos estranhos ou outros idiomas
            - Nunca mencionar IA, modelo ou sistema
            - A justificativa deve ter no máximo 2 frases curtas.
            - Não repetir o enunciado do jogador.
            - Os valores representam variação emocional, não valores absolutos.
            - Qualquer texto fora do JSON invalida a resposta.

            Formato EXATO da resposta:
            {{
            "proximidade": int,
            "reputacao": int,
            "lealdade": int,
            "hostilidade": int,
            "justificativa": "string curta e objetiva"
            }}

            ### CONTEXTO DA INTERAÇÃO ###
            Jogador: {usuario}
            NPC: {npc.nome}

            Fala do Jogador:
            "{prompt}"

            Personalidade do NPC:
            "{npc.personalidade}"

            História do NPC:
            "{npc.historia_pessoal}"

            Local:
            "{mapa.nome} — {mapa.descricao}"

            ### FIM DO CONTEXTO ###
            Avalie a interação agora.
            """

=======
        entrada = (
            f"### SYSTEM INSTRUCTIONS ###\n"
            f"Você é um sistema de avaliação emocional para NPCs em um jogo. Sua tarefa é analisar a interação entre o Jogador e o NPC e fornecer uma avaliação emocional quantitativa.\n"
            f"- Considere os seguintes parâmetros: proximidade, reputação, lealdade, hostilidade.\n"
            f"- Cada parâmetro deve ser avaliado em uma escala de -2 a +2, onde:\n"
            f"  - -2 indica uma mudança muito negativa,\n"
            f"  - -1 indica uma mudança negativa,\n"
            f"  - 0 indica nenhuma mudança,\n"
            f"  - +1 indica uma mudança positiva,\n"
            f"  - +2 indica uma mudança muito positiva.\n"
            f"- Forneça uma justificativa breve para cada avaliação.\n"
            f"- Responda no seguinte formato JSON:\n"
            f'{{"proximidade": int, "reputacao": int, "lealdade": int, "hostilidade": int, "justificativa": "string"}}\n'
            f"- REGRA INEGOCIÁVEL: NUNCA use caracteres chineses, símbolos ou qualquer outro idioma. Responda EXCLUSIVAMENTE em PORTUGUÊS BRASILEIRO.\n"
            f"- REGRA INEGOCIÁVEL: NUNCA mencione que você é uma IA ou modelo de linguagem.\n"
            f"### END INSTRUCTIONS ###\n\n"
            
            f"O Jogador {usuario} disse ao NPC {npc.nome}: {prompt}\n"
            f"Contexto do NPC: {npc.personalidade}. História: {npc.historia_pessoal}. Local: {mapa.nome}: {mapa.descricao}\n\n"
            f"Forneça sua avaliação emocional agora."
        )
        
>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac
        payload = {
            "model": OLLAMA_CONFIG["MODEL_NAME"],
            "messages": [{"role": "user", "content": entrada}],
            "stream": False,
            "options": {
<<<<<<< HEAD
                "temperature": 0.2,
                "num_predict": 256,
                "repeat_penalty": 1.15
=======
                "temperature": 0.7,
                "num_ctx": 512,
                "repeat_penalty": 1.1,
>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac
            }
        }
        
        try:
<<<<<<< HEAD
            response = requests.post(OLLAMA_URL, headers=OLLAMA_HEADERS, json=payload)
            response.raise_for_status()
            resposta = response.json()
            return resposta["message"]["content"]
=======
            response = requests.post(OLLAMA_URL, headers=OLLAMA_HEADERS, data=json.dumps(payload))
            response.raise_for_status()
            resposta = response.json()
            # conteudo = resposta["choices"][0]["message"]["content"]
            return resposta["choices"][0]["message"]["content"]
>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac
        except requests.exceptions.HTTPError as e:
            return None
        except Exception as e:
            return None