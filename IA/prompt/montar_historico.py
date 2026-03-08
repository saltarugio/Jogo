
def montar_historico(historico, npc, avatar, limite):
# Limitar histórico
        if len(historico) > limite:
            historico = historico[-limite:]

        # Montar contexto
        linha = []
        for item in historico:
            linha.append(f"{avatar}: {item.jogador}")
            linha.append(f"{npc}: {item.npc}")
        return "\n".join(linha)