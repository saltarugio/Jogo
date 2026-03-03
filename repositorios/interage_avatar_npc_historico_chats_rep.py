from datetime import datetime

class InterageAvatarNpcHistoricoChatsRep:
    def __init__(self, cursor):
        self.cursor = cursor

    def registrar_interacao(self, fk_avatar_id, fk_npc_id, fk_historico_id):
        try:
            # cursor = self.banco.cursor()
            query = """
                INSERT INTO interage_avatar_npc_historico_chats (fk_avatar_id, fk_npc_id, fk_historico_id, data_interacao)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (fk_avatar_id, fk_npc_id, fk_historico_id, datetime.now()))
            if self.cursor.rowcount != 1:
                raise Exception("Insert não afetou nenhuma linha")
            return True
        except Exception as e:
            print(f"Erro ao registrar interação: {e}")
            return False
    
    def buscar_por_avatar_e_npc(self, avatar_id, usuario_id, limite=10):
        try:
            query = """
                SELECT *
                    FROM (
                        SELECT hc.id, hc.mensagem_usuario, hc.resposta_ai
                        FROM historico_chats hc
                        JOIN interage_avatar_npc_historico_chats ianhc
                        ON ianhc.fk_historico_id = hc.Id
                        WHERE ianhc.fk_avatar_id = %s
                        AND ianhc.fk_npc_id = %s
                        ORDER BY hc.Id DESC
                        LIMIT %s
                    ) t
                    ORDER BY Id ASC;
            """
            self.cursor.execute(query, (avatar_id, usuario_id, limite))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []