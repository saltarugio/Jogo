from IA.Ollama.ollama_client import OllamaClient
from IA.prompt.montar_prompt import MontarPrompt
from IA.modelo_ia import obter_modelo
from services.postprocesso_resposta import processar_avaliacao, validar_json

class ChatService:

    def __init__(self, modelo="deepseek_v3"):
        self.config = obter_modelo(modelo)
        self.client = OllamaClient(self.config)

    def enviar_resposta(self, npc, avatar, historico, prompt, mapa, contexto_parametros):

        mensagens = MontarPrompt.montar_prompt_resposta(
            npc,
            avatar,
            historico,
            prompt,
            mapa,
            contexto_parametros,
            self.config
        )

        resposta = self.client.chat(
            mensagens,
            self.config["TEMPERATURE"],
            self.config["MAX_TOKENS"]
        )

        return resposta

    def enviar_avaliacao(self, npc, avatar, texto, resposta_ia, mapa):

        mensagens = MontarPrompt.montar_prompt_avaliacao(
            npc,
            avatar,
            texto,
            resposta_ia,
            mapa,
        )
        tentativa = 3
        for _ in range(tentativa):

            resposta = self.client.chat(
                mensagens,
                0.2,
                self.config["MAX_TOKENS"]
            )

            avaliacao = processar_avaliacao(resposta)

        if "erro" not in avaliacao and validar_json(avaliacao):
            return avaliacao
        
        #Caso todas as tentativas falharem
        return {
            "proximidade": 0,
            "reputacao": 0,
            "lealdade": 0,
            "hostilidade": 0,
            "justificativa": "falha na avaliação"
        }