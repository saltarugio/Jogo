import json
from click import prompt
import banco.conection as db
from  IA.ia import DeepSeekIA
from models.historico import Historico
from IA.parametros_ia import atualizar as atualizar_parametros_ia
from IA.contexto_parametro import montar_contexto_parametros
import time

class NPC:
    def __init__(self, id=None, nome=None, raca=None, personalidade=None, profissao=None, historia_pessoal=None, fk_mapa_id=None):
        self.id = id
        self.nome = nome
        self.raca = raca
        self.personalidade = personalidade
        self.profissao = profissao
        self.historia_pessoal = historia_pessoal
        self.fk_mapa_id = fk_mapa_id

    @staticmethod
    def listar_por_mapa(mapa_id):
        if not db.open():
            return []
        try:
            query = """
                        SELECT n.id, n.nome, n.raca, n.personalidade, n.profissao, n.historia_pessoal
                        FROM npc n
                        JOIN contido c ON n.id = c.fk_npc_id
                        WHERE c.fk_mapas_id = %s
                    """
            db.cursor.execute(query, (mapa_id,))
            results = db.cursor.fetchall()
            db.close()
            return [NPC(**row) for row in results]
        except Exception as e:
            db.close()
            print(f"Erro ao listar NPCs: {e}")
            return []     

    @staticmethod
    def responder(npc, prompt, avatar_id, historico, mapa):
        try:
            resposta = DeepSeekIA.gerar_resposta(npc, avatar_id, historico, prompt, mapa)
            return resposta
        except Exception as e:
            print(f"[NPC] Erro ao responder: {e}")
            return "O NPC ficou em silêncio..."

    @staticmethod
    def executar_interacao_completa(avatar, npc, mapa_atual):
        prompt = input("Você: ").strip()[:200]
        if prompt.lower() in ["sair", "exit", "quit"]:
            print("🚪 Encerrando conversa.")
            return False

        historico = Historico.buscar_por_avatar_e_npc(avatar.id, npc.id, limite=10)
        parametros_ia = Historico.buscar_parametros_ia(avatar.id, npc.id)

        contexto_parametros = montar_contexto_parametros(parametros_ia, avatar, npc)
        resposta = NPC.responder(npc, prompt, avatar.nome, historico, mapa_atual, contexto_parametros)

        for letra in resposta:
            console.print(f"{letra}", end='', style="white")
            time.sleep(0.02)  # Ajuste o tempo para controlar a velocidade da "digitação"
            console.print()  # Nova linha após a resposta

        avaliacao = DeepSeekIA.avaliacao_emocional(
            npc.nome,
            avatar.nome,
            f"O jogador disse: {prompt}. O NPC respondeu: {resposta}.",
            mapa_atual
        )

        if avaliacao:
            atualizar_parametros_ia(avatar.id, npc.id, json.dumps(avaliacao, ensure_ascii=False))

        Historico.registrar_interacao(
            fk_avatar_id=avatar.id,
            fk_npc_id=npc.id,
            prompt_usuario=prompt,
            resposta_ia=f'{{"resposta":"{resposta}"}}'
        )

        return True
  
    # @staticmethod
    # def executa_interacao(avatar, npc, mapa):

        # prompt = input("Você: ").strip()[:200]  # Limita a 200 caracteres
        # if  prompt.lower() in ["sair", "exit", "quit"]:
        #     console.print("🚪 Encerrando conversa.")
        #     Avatar.atualiza_posicao_avatar(avatar, mapa.id)  # Atualiza a posição do avatar ao sair da conversa
        #     return

        # # busca histórico
        # historico = Historico.buscar_por_avatar_e_npc(avatar.id, npc_escolhido.id, limite=10)
        # # busca parâmetros IA
        # parametros_ia = Historico.buscar_parametros_ia(avatar.id, npc_escolhido.id)

        # if parametros_ia:
        #     proximidade, reputacao, lealdade, hostilidade, observacao = parametros_ia
        #     contexto_parametros = (
        #         f"Parâmetros atuais entre {avatar.nome} e {npc_escolhido.nome}:\n"
        #         f"- Proximidade: {proximidade}\n"
        #         f"- Reputação: {reputacao}\n"
        #         f"- Lealdade: {lealdade}\n"
        #         f"- Hostilidade: {hostilidade}\n"
        #         f"- Observações anteriores: {observacao}\n"
        #         )
        # else:
        #     contexto_parametros = "Parâmetros iniciais neutros entre jogador e NPC."

        #     # obtém resposta do NPC via IA
        #     resposta = NPC.responder(npc_escolhido, prompt, avatar.nome, historico, mapa_atual, contexto_parametros)
        #     console.print(f"[bold yellow]{npc_escolhido.nome}[/]: ", end='')
        #     if resposta:
        #         
        #         avaliacao = DeepSeekIA.avaliacao_emocional(npc_escolhido.nome, avatar.nome, f"O jogador disse: {prompt}. O NPC respondeu: {resposta}.", mapa_atual)

        #     if avaliacao:
        #         resposta_ia_json = json.dumps(avaliacao, ensure_ascii=False)
        #         atualizar_parametros_ia(avatar.id, npc_escolhido.id, resposta_ia_json)

        #         # registra no histórico
        #         Historico.registrar_interacao(
        #                 fk_avatar_id=avatar.id,
        #                 fk_npc_id=npc_escolhido.id,
        #                 prompt_usuario=prompt,
        #                 resposta_ia=f'{{"resposta":"{resposta}"}}',
        #         )
        #     else:
        #         console.print("⚠️ O NPC está ocupado e não pode responder no momento. Tente novamente.")
        # return True