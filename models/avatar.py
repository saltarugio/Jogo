import banco.conection as db

class Avatar:
    def __init__(self, id=None, nome=None, usuario_id=None, fk_mapa_id=None):
        self.id = id
        self.nome = nome
        self.usuario_id = usuario_id
        self.fk_mapa_id = fk_mapa_id

    @staticmethod
    def criar(nome, usuario_id):
        if not db.open():
            return None
        try:
            # Inicia transação
            db.db.start_transaction()

            # Inserir avatar
            query = "INSERT INTO avatar (nome, fk_mapa_id) VALUES (%s, %s)"
            db.cursor.execute(query, (nome, 1))  # fk_mapa_id padrão
            avatar_id = db.cursor.lastrowid

            # Criar relação na tabela contem
            query = "INSERT INTO contem (fk_avatar_id, fk_usuario_id) VALUES (%s, %s)"
            db.cursor.execute(query, (avatar_id, usuario_id))

            # Confirma tudo
            db.db.commit()
            return Avatar(avatar_id, nome, usuario_id, 1)

        except Exception as e:
            # Se algo falhar, desfaz
            db.db.rollback()
            print(f"Erro ao criar avatar: {e}")
            return None

        finally:
            db.close()

    @staticmethod
    def listar_por_usuario(usuario_id):
        if not db.open():
            return []
        try:
            query = """
                SELECT av.id, av.nome, av.fk_mapa_id, c.fk_usuario_id AS usuario_id
                FROM avatar AS av
                INNER JOIN contem c ON c.fk_avatar_id = av.id
                WHERE c.fk_usuario_id = %s
            """
            db.cursor.execute(query, (usuario_id,))
            results = db.cursor.fetchall()
            db.close()
            return [Avatar(**row) for row in results]
        except Exception as e:
            db.close()
            print(f"Erro ao listar avatares: {e}")
            return []
    
    @staticmethod
    def atualiza_posicao_avatar(id, fk_mapa_id):
        if not db.open():
            return False  # Consistente: retorna False se não abriu a conexão

        try:
            query = "UPDATE avatar SET fk_mapa_id = %s WHERE id = %s"
            db.cursor.execute(query, (fk_mapa_id, id))
            db.db.commit()

            return True
        except Exception as e:
            print(f"[Avatar] Erro ao atualizar posição do avatar: {e}")
            return False
        finally:
            db.close()

