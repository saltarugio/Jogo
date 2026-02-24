import banco.conection as db

class Avatar:
    def __init__(self, id=None, nome=None, usuario_id=None, fk_mapa_id=None):
        self.id = id
        self.nome = nome
        self.usuario_id = usuario_id
        self.fk_mapa_id = fk_mapa_id

    def __repr__(self):
        return f"Avatar id={self.id} nome={self.nome}"
    
    # @staticmethod
    # def buscar_por_avatar(avatar):
    #     try:
    #         with db.Banco() as banco:
    #             query = "SELECT id FROM avatar WHERE nome = %s"
    #             banco.cursor.execute(query, (avatar,))
    #             row = banco.cursor.fetchone()
    #             if row:
    #                 return True
    #             return None
    #     except Exception as e:
    #         print(f"Erro ao buscar avatar: {e}")
    #         return None
    
    # @staticmethod
    # def criar(nome, usuario_id):
    #     if Avatar.buscar_por_avatar(nome):
    #         return None
    #     else:
    #         try:
    #             with db.Banco() as banco:
    #                 # Inicia transação
    #                 banco.db.start_transaction()

    #                 # Inserir avatar
    #                 query = "INSERT INTO avatar (nome, fk_mapa_id) VALUES (%s, %s)"
    #                 banco.cursor.execute(query, (nome, 1))  # fk_mapa_id padrão
    #                 avatar_id = banco.cursor.lastrowid

    #                 # Criar relação na tabela contem
    #                 query = "INSERT INTO contem (fk_avatar_id, fk_usuario_id) VALUES (%s, %s)"
    #                 banco.cursor.execute(query, (avatar_id, usuario_id))

    #                 # Confirma tudo
    #                 banco.db.commit()
    #                 return Avatar(avatar_id, nome, usuario_id, 1)

    #         except Exception as e:
    #             # Se algo falhar, desfaz
    #             banco.db.rollback()
    #             print(f"Erro ao criar avatar: {e}")
    #             return None

    # @staticmethod
    # def listar_por_usuario(usuario_id):
    #     try:
    #         with db.Banco() as banco:
    #             query = """
    #                 SELECT av.id, av.nome, av.fk_mapa_id, c.fk_usuario_id AS usuario_id
    #                 FROM avatar AS av
    #                 INNER JOIN contem c ON c.fk_avatar_id = av.id
    #                 WHERE c.fk_usuario_id = %s
    #             """
    #             banco.cursor.execute(query, (usuario_id,))
    #             results = banco.cursor.fetchall()
    #             return [Avatar(**row) for row in results]
    #     except Exception as e:
    #         print(f"Erro ao listar avatares: {e}")
    #         return []               
        
    # @staticmethod
    # def atualiza_posicao_avatar(id, fk_mapa_id):
    #     try:
    #         with db.Banco() as banco:
    #             query = "UPDATE avatar SET fk_mapa_id = %s WHERE id = %s"
    #             banco.cursor.execute(query, (fk_mapa_id, id))
    #             banco.db.commit()
    #             return True
    #     except Exception as e:
    #         print(f"[Avatar] Erro ao atualizar posição do avatar: {e}")
    #         return False
