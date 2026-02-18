import requests
from IA.config import OLLAMA_API_DEEPSEEK_V3, OLLAMA_API_QWEN3_CODER, OLLAMA_API_DEEPSEEK_R1
from rich.console import Console



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

        # Crie o payload com base na documentação
        payload = {
            "model": OLLAMA_CONFIG["MODEL_NAME"],
            "messages": [{"role": "user", "content": entrada}],
            "stream": False,
            "options": {
                "temperature": OLLAMA_CONFIG["TEMPERATURE"],
                "num_predict": OLLAMA_CONFIG["MAX_TOKENS"],
                "repeat_penalty": OLLAMA_CONFIG["REPEAT_PENALTY"],
            }
        }
        try:
            # Requisição SEM stream=True e SEM o parâmetro stream=True no requests.post
            response = requests.post(OLLAMA_URL, headers=OLLAMA_HEADERS, json=payload)
            response.raise_for_status() # Levanta erro para códigos de status HTTP ruins
            
            # 1. Obtém o JSON completo
            data = response.json()
                
            # 2. Extrai o conteúdo da resposta de uma só vez
            resposta_completa = data["message"]["content"]
            return resposta_completa
        
        except requests.exceptions.HTTPError as e:
            return None
        
        except Exception as e:
            return None
    
    @staticmethod
    def avaliacao_emocional(npc, usuario, prompt, mapa):
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

        payload = {
            "model": OLLAMA_CONFIG["MODEL_NAME"],
            "messages": [{"role": "user", "content": entrada}],
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 256,
                "repeat_penalty": 1.15
            }
        }
        
        try:
            response = requests.post(OLLAMA_URL, headers=OLLAMA_HEADERS, json=payload)
            response.raise_for_status()
            resposta = response.json()
            return resposta["message"]["content"]
        except requests.exceptions.HTTPError as e:
            return None
        except Exception as e:
            return None