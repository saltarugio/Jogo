import banco.conection as db
from rich.console import Console

console = Console()
class Historico:
    @staticmethod
    def registrar_interacao(fk_avatar_id, fk_npc_id, prompt_usuario, resposta_ia):
        try:
            with db.Banco() as banco:
                # Início da transação
                banco.db.start_transaction()

                # Inserção no histórico
                query_historico = """
                    INSERT INTO historico_chats (mensagem_usuario, resposta_ai)
                    VALUES (%s, %s)
                """
                banco.cursor.execute(query_historico, (prompt_usuario, resposta_ia))
                historico_id = banco.cursor.lastrowid
                # Inserção na tabela interage
                query_interage = """
<<<<<<< HEAD
                    INSERT INTO interage_avatar_npc_historico_chats (fk_avatar_id, fk_npc_id, fk_historico_id)
=======
                    INSERT INTO interage_avatar_npc_historico (fk_avatar_id, fk_npc_id, fk_historico_id)
>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac
                    VALUES (%s, %s, %s)
                """
                banco.cursor.execute(query_interage, (fk_avatar_id, fk_npc_id, historico_id))

                # Finaliza a transação (commit)
                banco.db.commit()
                return True
        except Exception as e:
            # Se algo deu errado, desfaz tudo
            banco.db.rollback()
            console.print("[bold red][Histórico] Erro ao registrar interação:", e)
            return False

    @staticmethod
    def buscar_por_avatar_e_npc(fk_avatar_id, fk_npc_id, limite=10):
        try:
            with db.Banco() as banco:
                query = """
                    SELECT hc.mensagem_usuario, hc.resposta_ai FROM historico_chats as hc 
<<<<<<< HEAD
                    INNER JOIN interage_avatar_npc_historico_chats as ianh ON hc.id = ianh.fk_historico_id 
=======
                    INNER JOIN interage_avatar_npc_historico as ianh ON hc.id = ianh.fk_historico_id 
>>>>>>> 5e27a737e49ee1b6b19f09bbc774554e4c6b97ac
                    WHERE ianh.fk_avatar_id = %s AND ianh.fk_npc_id = %s ORDER BY id DESC LIMIT %s;
                """
                banco.cursor.execute(query, (fk_avatar_id, fk_npc_id, limite))
                results = banco.cursor.fetchall()
                return results[::-1]  # inverte para ordem cronológica
        except Exception as e:
            console.print(f"[bold red][Historico] Erro ao buscar histórico: {e}")
            return []
        
    @staticmethod    
    def buscar_parametros_ia(fk_avatar_id, fk_npc_id):
        try:
            with db.Banco() as banco:
                query = """
                    SELECT proximidade, reputacao, lealdade, hostilidade, observacao 
                    FROM parametros_ia 
                    WHERE fk_avatar_id = %s AND fk_npc_id = %s;
                """
                banco.cursor.execute(query, (fk_avatar_id, fk_npc_id))
                result = banco.cursor.fetchone()
                return result
        except Exception as e:
            console.print(f"[bold red][Historico] Erro ao buscar parâmetros IA: {e}")
            return None