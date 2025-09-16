from IA.config import AI_CONFIG
from models import Historico

def gerar_resposta(npc, avatar_id, mapa_id, prompt_usuario):
    """
    Função que gera uma resposta do NPC.
    Por enquanto é mock, depois entra a IA real.
    """
    # 1. Buscar histórico de conversas com esse NPC
    historico = Historico.buscar_por_avatar_e_npc(avatar_id, npc.id, limite=AI_CONFIG["max_historico"])

    # 2. Montar contexto básico (mock por enquanto)
    contexto = f"O NPC {npc.nome}, um {npc.raca} {npc.profissao}, tem a seguinte personalidade: {npc.personalidade}. "
    contexto += f"História pessoal: {npc.historia_pessoal}. "
    contexto += f"Você está no mapa {mapa_id}. "

    if historico:
        contexto += "Histórico recente: "
        for h in historico:
            contexto += f"Jogador: {h['mensagem_usuario']} | NPC: {h['resposta_ai']} "

    # 3. Gerar resposta (mock simples)
    resposta = f"{npc.nome} diz: 'Ainda não tenho respostas dinâmicas, mas recebi: {prompt_usuario}'"

    return resposta
