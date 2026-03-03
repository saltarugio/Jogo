import banco.conection as db
from rich.console import Console
from models.historico import Historico, DialogoHistorico
from models.interage_avatar_npc_historico_chats import InterageAvatarNpcHistoricoChats as Interage
from repositorios.historico_chat_rep import HistoricoChatRep
from repositorios.interage_avatar_npc_historico_chats_rep import InterageAvatarNpcHistoricoChatsRep as InterageRep

console = Console()

class HistoricoService:
    def registrar_interacao(fk_avatar_id, fk_npc_id, prompt_usuario, resposta_ia):
        try:
            with db.Banco() as banco:
                cursor = banco.db.cursor()
                historico_rep = HistoricoChatRep(cursor)
                interage_rep = InterageRep(cursor)

                banco.db.start_transaction()
                
                # Registrar o histórico e obter o ID
                historico_id = historico_rep.registrar_interacao(prompt_usuario, resposta_ia)
                if not historico_id:
                    banco.db.rollback()  # Desfaz qualquer alteração se o registro do histórico falhar
                    console.print("[bold red][HistoricoService] Erro ao registrar histórico.")
                    raise False

                # Registrar a interação na tabela interage
                interage = interage_rep.registrar_interacao(fk_avatar_id, fk_npc_id, historico_id)
                if not interage:
                    banco.db.rollback()  # Desfaz o registro do histórico se a interação falhar
                    console.print(f"[bold red][HistoricoService] Erro ao registrar interação. {interage}")
                    raise False

                banco.db.commit()

                return True
        except Exception as e:
            console.print(f"[bold red][HistoricoService] Erro ao registrar interação: {e}")
            return False

    @staticmethod
    def buscar_por_avatar_e_npc(avatar_id, npc_id, limite=10):
        try:
            with db.Banco() as banco:
                cursor = banco.db.cursor(dictionary=True)
                interage_rep = InterageRep(cursor)

                resultado = interage_rep.buscar_por_avatar_e_npc(avatar_id, npc_id, limite)
                return [DialogoHistorico(
                    jogador = linha['mensagem_usuario'], 
                    npc= linha['resposta_ai']) 
                    for linha in resultado]
                # return [Historico(**linha) for linha in resultado]
        except Exception as e:
            console.print(f"Erro ao buscar histórico: {e}")
            return False
    
    @staticmethod    
    def buscar_parametros_ia(fk_avatar_id, fk_npc_id):
        return Historico.buscar_parametros_ia(fk_avatar_id, fk_npc_id)