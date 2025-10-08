import banco.conection as db

class Historico:
    @staticmethod
    def registrar_interacao(fk_avatar_id, fk_npc_id, prompt_usuario, resposta_ia):
        if not db.open():
            return False

        try:
            # Início da transação
            db.db.start_transaction()

            # Inserção no histórico
            query_historico = """
                INSERT INTO historico_chats (mensagem_usuario, resposta_ai)
                VALUES (%s, %s)
            """
            db.cursor.execute(query_historico, (prompt_usuario, resposta_ia))
            historico_id = db.cursor.lastrowid
            # Inserção na tabela interage
            query_interage = """
                INSERT INTO interage_avatar_npc_historico (fk_avatar_id, fk_npc_id, fk_historico_id)
                VALUES (%s, %s, %s)
            """
            db.cursor.execute(query_interage, (fk_avatar_id, fk_npc_id, historico_id))

            # Finaliza a transação (commit)
            db.db.commit()
            return True

        except Exception as e:
            # Se algo deu errado, desfaz tudo
            db.db.rollback()
            print("[Histórico] Erro ao registrar interação:", e)
            return False

        finally:
            db.close()

    @staticmethod
    def buscar_por_avatar_e_npc(fk_avatar_id, fk_npc_id, limite=10):
        if not db.open():
            return []
        try:
            query = """
                SELECT hc.mensagem_usuario, hc.resposta_ai FROM historico_chats as hc 
                INNER JOIN interage_avatar_npc_historico as ianh ON hc.id = ianh.fk_historico_id 
                WHERE ianh.fk_avatar_id = %s AND ianh.fk_npc_id = %s ORDER BY id DESC LIMIT %s;
            """
            db.cursor.execute(query, (fk_avatar_id, fk_npc_id, limite))
            results = db.cursor.fetchall()
            db.close()
            return results[::-1]  # inverte para ordem cronológica
        except Exception as e:
            db.close()
            print(f"[Historico] Erro ao buscar histórico: {e}")
            return []
        
    @staticmethod    
    def buscar_parametros_ia(fk_avatar_id, fk_npc_id):
        if not db.open():
            return None
        try:
            query = """
                SELECT proximidade, reputacao, lealdade, hostilidade, observacao 
                FROM parametros_ia 
                WHERE fk_avatar_id = %s AND fk_npc_id = %s;
            """
            db.cursor.execute(query, (fk_avatar_id, fk_npc_id))
            result = db.cursor.fetchone()
            db.close()
            return result
        except Exception as e:
            db.close()
            print(f"[Historico] Erro ao buscar parâmetros IA: {e}")
            return None