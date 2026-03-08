
from IA.prompt.montar_historico import montar_historico
class MontarPrompt:
    def montar_prompt_resposta(npc, avatar, historico, prompt, mapa, contexto_parametros, config):
        contexto = montar_historico(historico, npc.nome, avatar, config["MAX_HISTORICO"])
        entrada_sistema = f"""
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
            - Evite repetir saudações, respostas de cortesia ou estruturas usadas recentemente
            - Se a pergunta do jogador for parecida, varie o foco da resposta
            - Não responda "estou bem" mais de uma vez em interações próximas
            - Quando o jogador repetir perguntas simples, avance o diálogo com novas informações, dicas ou contexto do local

            Uso do estado emocional:
            {contexto_parametros}

            Formato da resposta:
            - Entre 1 e 3 frases curtas
            - Tom coerente com a personalidade e o estado emocional
            """
        entrada_conteudo = f"""
            ### HISTÓRICO DE DIÁLOGO ###
            {contexto}
            ### FIM DO HISTÓRICO ###

            Fala do jogador:
            {avatar}: {prompt}

            Resposta do NPC:
            """
        return [
                {"role": "system", "content": entrada_sistema},
                {"role": "user", "content": entrada_conteudo}
            ]
    def montar_prompt_avaliacao(npc, avatar, texto, resposta, mapa):
        # contexto = montar_historico(historico, npc.nome, avatar, config["MAX_HISTORICO"])
        entrada_sistema = f"""
            ### SYSTEM INSTRUCTIONS ###
            Você é um sistema de avaliação emocional para NPCs em um jogo.
            
            Tarefa:
            - Avaliar como a fala do jogador afetou emocionalmente o NPC.
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

            NÃO inclua nenhuma outra chave além dessas. Se não conseguir, responda com {{"erro":"formato inválido"}}.
        """
        
        entrada_conteudo = f"""    
            ### CONTEXTO DA INTERAÇÃO ###
            Jogador: {avatar}
            NPC: {npc.nome}

            Diálogo:
            Jogador: {texto}
            NPC: {resposta}

            Local: {mapa.nome}

            ### FIM DO CONTEXTO ###
            Avalie como a fala do jogador afetou emocionalmente o NPC.
            """
        return [
                {"role": "system", "content": entrada_sistema},
                {"role": "user", "content": entrada_conteudo}
            ]