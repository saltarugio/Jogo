import banco.conection as db

class Historico:
    @staticmethod
    def registrar_interacao(fk_avatar_id, fk_npc_id, prompt_usuario, resposta_ia, fk_mapa_id):
        if not db.open():
            return False
        query = """
        INSERT INTO historico_chats (fk_avatar_id, fk_npc_id, mensagem_usuario, resposta_ia, fk_mapa_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        db.cursor.execute(query, (fk_avatar_id, fk_npc_id, prompt_usuario, resposta_ia, fk_mapa_id))
        db.db.commit()
        db.close()
        return True
