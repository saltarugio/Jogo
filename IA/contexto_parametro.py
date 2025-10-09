def montar_contexto_parametros(parametros_ia, avatar, npc):
    """
    Gera uma descrição textual do estado emocional entre o jogador (avatar) e o NPC,
    baseada nos valores numéricos dos parâmetros armazenados no banco.
    """
    
    if not parametros_ia:
        return f"{npc.nome} acabou de conhecer {avatar.nome}. Ainda não há sentimentos definidos entre eles."

    proximidade, reputacao, lealdade, hostilidade, observacao = parametros_ia

    # ✅ Garante os valores dentro do esperado
    proximidade = int(proximidade)
    reputacao = int(reputacao)
    lealdade = int(lealdade)
    hostilidade = int(hostilidade)

    def interpretar(valor, positivo, negativo, neutro="neutro"):
        """Retorna uma frase curta conforme o nível do valor."""
        if valor >= 70:
            return positivo
        elif valor <= -50:
            return negativo
        else:
            return neutro

    # 🧠 Traduções dos parâmetros em termos descritivos
    descricao_proximidade = interpretar(
        proximidade,
        positivo=f"{npc.nome} tem grande afeição e sente-se à vontade com {avatar.nome}.",
        negativo=f"{npc.nome} sente antipatia ou distância emocional de {avatar.nome}.",
        neutro=f"A relação entre {npc.nome} e {avatar.nome} é neutra, ainda em desenvolvimento."
    )

    descricao_reputacao = interpretar(
        reputacao,
        positivo=f"{npc.nome} respeita e admira as atitudes de {avatar.nome}.",
        negativo=f"{npc.nome} desconfia das intenções de {avatar.nome}.",
        neutro=f"{npc.nome} ainda está formando uma opinião sobre {avatar.nome}."
    )

    descricao_lealdade = interpretar(
        lealdade,
        positivo=f"{npc.nome} é leal e tende a apoiar {avatar.nome} em decisões futuras.",
        negativo=f"{npc.nome} pode trair ou agir contra {avatar.nome} se for conveniente.",
        neutro=f"A lealdade de {npc.nome} ainda é incerta."
    )

    descricao_hostilidade = interpretar(
        hostilidade,
        positivo=f"{npc.nome} demonstra raiva e pode reagir de forma agressiva a provocações.",
        negativo=f"{npc.nome} é calmo e evita conflitos com {avatar.nome}.",
        neutro=f"{npc.nome} está neutro, sem hostilidade aparente."
    )

    # Observação opcional vinda da IA anterior
    descricao_observacao = (
        f"Observações anteriores da IA sobre a relação: {observacao}"
        if observacao else
        f"Não há observações anteriores sobre o comportamento de {npc.nome}."
    )

    contexto = (
        f"Contexto emocional entre {avatar.nome} (jogador) e {npc.nome} (NPC):\n"
        f"- {descricao_proximidade}\n"
        f"- {descricao_reputacao}\n"
        f"- {descricao_lealdade}\n"
        f"- {descricao_hostilidade}\n"
        f"- {descricao_observacao}\n\n"
        f"Use esse contexto para guiar o tom e o conteúdo das respostas de {npc.nome}."
    )

    return contexto
