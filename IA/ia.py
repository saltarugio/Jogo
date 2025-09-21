import requests
import json
import re
from IA.config import OLLAMA_URL, OLLAMA_HEADERS, OLLAMA_MODEL, AI_CONFIG
import unicodedata # Novo import para manipulação de caracteres

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
        if len(historico) > AI_CONFIG["max_historico"]:
            historico = historico[-AI_CONFIG["max_historico"]:]

        # Montar contexto
        # ... (código mantido, pois não é o foco do problema)
        if isinstance(historico, list) and len(historico) > 0 and isinstance(historico[0], dict):
            historico = [f"{k}: {v}" for msg in historico for k, v in msg.items()]
        contexto = "\n".join(historico)

         # Prompt otimizado: Remova o excesso de formatação do terminal
        entrada = (
            f"### SYSTEM INSTRUCTIONS ###\n"
            f"Você é o NPC {npc.nome}. Sua única tarefa é responder ao Jogador.\n"
            f"- Mantenha a personalidade: {npc.personalidade}.\n"
            f"- Considere a história: {npc.historia_pessoal}.\n"
            f"- Local: {mapa.nome}: {mapa.descricao}\n" # Assumindo que você tem um campo 'mapa' no seu objeto Usuario
            f"- REGRA PRINCIPAL: Responda APENAS o que o NPC diria. Nunca mostre raciocínio interno.\n"
            f"- REGRA DE FORMATO: Responda em 1 a 3 frases curtas. Não repita a pergunta do Jogador.\n"
            f"### END INSTRUCTIONS ###\n\n"
            
            f"### DIALOG HISTORY ###\n"
            f"{contexto}\n"
            f"### END HISTORY ###\n\n"
            
            f"Jogador: {prompt}\n"
            f"{npc.nome}: " # O modelo deve preencher a partir daqui
        )

        payload = {
            "model": OLLAMA_MODEL,
            "messages": [{"role": "user", "content": entrada}],
            "stream": False
        }
        try:
            resposta = requests.post(OLLAMA_URL, headers=OLLAMA_HEADERS, data=json.dumps(payload))
            resposta.raise_for_status()

            data = resposta.json()

            resposta_completa = data["choice"][0]["message"]["content"]

            print(f"[{npc.nome} disse (Cru):] {resposta_completa}")

            resposta_final = limpar_resposta_final(resposta_completa)

            if resposta_final.lower().strip() == remover_acentos(prompt).lower.strip():
                resposta_final = f"{remover_acentos(npc.nome)} parece pensativo, mas decide mudar de assunto"
            
            print("\n--- RESPOSTA FINAL ---\n", resposta_final)
            return resposta_final
        except requests.exceptions.HTTPError as e:
            print(f"[Erro] Falha ao chamar DeepSeek: {e}")
            return f"[IA simulada] {remover_acentos(npc.nome)}: {remover_acentos(prompt)}"
        except Exception as e:
            print(f"[Erro] Ocorreu um erro inesperado: {e}")
            return f"[IA simulada] {remover_acentos(npc.nome)}: {remover_acentos(prompt)}"

        # Código antigo de streaming mantido como comentário para referência futura
        # try:
        #     response = requests.post(OLLAMA_URL, headers=OLLAMA_HEADERS, data=json.dumps(payload), stream=True)

        #     resposta_completa = ""
        #     print(f"\n[{npc.nome} começa a falar...]", end=" ", flush=True) 

        #     for chunk in response.iter_lines(decode_unicode=True):
        #         if chunk:
        #             linha = chunk.strip()
        #             if linha == "[DONE]":
        #                 break
        #             if linha.startswith("data:"):
        #                 linha = linha[len("data:"):].strip()
        #                 if not linha:
        #                     continue
        #                 try:
        #                     data = json.loads(linha)
        #                     delta = data["choices"][0].get("delta", {}).get("content", "")
                            
        #                     if delta:
                                
        #                         # AÇÃO CRÍTICA: PRÉ-LIMPEZA DO DELTA PARA REMOVER APENAS TAGS
        #                         # Isso impede que as tags quebrem o texto no terminal.
        #                         # NÂO REMOVA ACENTOS AQUI!
        #                         delta_limpo_leve = delta.replace("<think>", "").replace("</think>", "").replace("...", "")
                                
        #                         # Acumula o delta *cru* para a limpeza final, mas remove as tags de pensamento
        #                         resposta_completa += delta_limpo_leve
                                
        #                         # Imprime o delta pré-limpo
        #                         print(delta_limpo_leve, end="", flush=True) 

        #                 except json.JSONDecodeError:
        #                     continue

        #     # Quebra de linha após o streaming
        #     print("\n") 
            
        #     # Limpeza pesada (incluindo remoção de acentos) ocorre AGORA
        #     resposta_final = limpar_resposta_final(resposta_completa)
             
        #     # Anti-loop
        #     if resposta_final.lower().strip() == remover_acentos(prompt).lower().strip():
        #         resposta_final = f"{remover_acentos(npc.nome)} parece pensativo, mas decide mudar de assunto."

        #     print("\n--- RESPOSTA FINAL ---\n", resposta_final)

        #     return resposta_final

        # except Exception as e:
        #     print(f"[Erro] Falha ao chamar DeepSeek: {e}")
        #     return f"[IA simulada] {remover_acentos(npc.nome)}: {remover_acentos(prompt)}"