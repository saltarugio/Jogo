class HistoricoChatRep:
    def __init__(self, cursor):
        self.cursor = cursor

    def registrar_interacao(self,prompt_usuario, resposta_ia):
        try:
            query = """
                INSERT INTO historico_chats (mensagem_usuario, resposta_ai)
                VALUES (%s, %s)
            """
            self.cursor.execute(query, (prompt_usuario, resposta_ia))
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erro ao registrar histórico: {e}")
            return None