import requests
from IA.config import OLLAMA_API_DEEPSEEK_V3, OLLAMA_API_QWEN3_CODER, OLLAMA_API_DEEPSEEK_R1
from rich.console import Console
from IA.services_ia.chat_service import ChatService
from services.postprocesso_resposta import processar_avaliacao

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
    # chat = ChatService()
    # @staticmethod
    # def gerar_resposta(npc, avatar, historico, prompt, mapa, contexto_parametros):
    #    return ChatService.enviar_resposta(npc, avatar, historico, prompt, mapa, contexto_parametros)
    # @staticmethod
    # def avaliacao_emocional(npc, avatar, historico, prompt, mapa, ):
    #     return ChatService.enviar_avaliacao(npc, avatar, historico, prompt, mapa)
    
    # @staticmethod
    # def gerar_resposta(npc, avatar, historico, prompt, mapa, contexto_parametros):
    #     # Limitar histórico
    #     if len(historico) > OLLAMA_CONFIG["MAX_HISTORICO"]:
    #         historico = historico[-OLLAMA_CONFIG["MAX_HISTORICO"]:]

    #     # Montar contexto
    #     linha = []
    #     for item in historico:
    #         linha.append(f"{avatar}: {item.jogador}")
    #         linha.append(f"{npc.nome}: {item.npc}")
    #     contexto = "\n".join(linha)
        
    #     # Prompt otimizado: Remova o excesso de formatação do terminal
    #     entrada_sistema = f"""
    #         ### SYSTEM INSTRUCTIONS ###
    #         REGRA ABSOLUTA:
    #         - Responda EXCLUSIVAMENTE em português brasileiro
    #         - Nunca mencione IA, modelo ou sistema
    #         - Nunca use outros idiomas ou símbolos estranhos
    #         - Responda SEMPRE como o NPC, dentro do universo do jogo

    #         Você é o NPC {npc.nome}.

    #         Identidade do NPC:
    #         - Personalidade: {npc.personalidade}
    #         - História: {npc.historia_pessoal}
    #         - Local atual: {mapa.nome} — {mapa.descricao}

    #         Comportamento:
    #         - Responda APENAS com fala direta
    #         - Não descreva ações, emoções internas ou pensamentos
    #         - Não use aspas, colchetes ou parênteses
    #         - Não seja narrador
    #         - Evite repetir saudações, respostas de cortesia ou estruturas usadas recentemente
    #         - Se a pergunta do jogador for parecida, varie o foco da resposta
    #         - Não responda "estou bem" mais de uma vez em interações próximas
    #         - Quando o jogador repetir perguntas simples, avance o diálogo com novas informações, dicas ou contexto do local

    #         Uso do estado emocional:
    #         {contexto_parametros}

    #         Formato da resposta:
    #         - Entre 1 e 3 frases curtas
    #         - Tom coerente com a personalidade e o estado emocional
    #         """
    #     entrada_conteudo = f"""
    #         ### HISTÓRICO DE DIÁLOGO ###
    #         {contexto}
    #         ### FIM DO HISTÓRICO ###

    #         Fala do jogador:
    #         {avatar}: {prompt}

    #         Resposta do NPC:
    #         """
    #     # Crie o payload com base na documentação
    #     payload = {
    #         "model": OLLAMA_CONFIG["MODEL_NAME"],
    #         "messages": [
    #             {"role": "system", "content": entrada_sistema},
    #             {"role": "user", "content": entrada_conteudo}
    #         ],
    #         "stream": False,
    #         "options": {
    #             "temperature": OLLAMA_CONFIG["TEMPERATURE"],
    #             "num_predict": OLLAMA_CONFIG["MAX_TOKENS"],
    #             "repeat_penalty": OLLAMA_CONFIG["REPEAT_PENALTY"],
    #         }
    #     }
    #     try:
    #         # Requisição SEM stream=True e SEM o parâmetro stream=True no requests.post
    #         response = requests.post(OLLAMA_URL, headers=OLLAMA_HEADERS, json=payload)
    #         response.raise_for_status() # Levanta erro para códigos de status HTTP ruins
            
    #         # 1. Obtém o JSON completo
    #         data = response.json()
                
    #         # 2. Extrai o conteúdo da resposta de uma só vez
    #         resposta_completa = data["message"]["content"]
    #         return resposta_completa
        
    #     except requests.exceptions.HTTPError as e:
    #         return None
        
    #     except Exception as e:
    #         return None
    
    @staticmethod
    def avaliacao_emocional(npc, usuario, prompt, mapa):
        entrada_sistema = f"""
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
            - IMPORTANTE: Se não conseguir responder em JSON válido, responda com {{"erro":"formato inválido"}}.
            
            Formato EXATO da resposta:
            {{
                "proximidade": int,
                "reputacao": int,
                "lealdade": int,
                "hostilidade": int,
                "justificativa": "string curta e objetiva"
            }}

            NÃO inclua nenhuma outra chave além dessas. Se não conseguir, responda com {{"erro":"formato inválido"}}."""
        entrada_conteudo = f"""    
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
            "messages": [
                {"role": "system", "content": entrada_sistema},
                {"role": "user", "content": entrada_conteudo}
            ],
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
            conteudo = resposta.get("message", {}).get("content")
            if not conteudo:
                return None
            dados = processar_avaliacao(conteudo)

            return dados
        except requests.exceptions.HTTPError:
            return None
        except Exception:
            return None