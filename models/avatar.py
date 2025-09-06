import banco.conection as db

class Avatar:
    def __init__(self, id=None, nome=None, usuario_id=None):
        self.id = id
        self.nome = nome
        self.usuario_id = usuario_id

    @staticmethod
    def criar(nome, usuario_id):
        if not db.open():
            return None
        try:
            # Inicia transação
            db.db.start_transaction()

            # Inserir avatar
            query = "INSERT INTO avatar (nome) VALUES (%s)"
            db.cursor.execute(query, (nome,))
            avatar_id = db.cursor.lastrowid

            # Criar relação na tabela contem
            query = "INSERT INTO contem (fk_avatar_id, fk_usuario_id) VALUES (%s, %s)"
            db.cursor.execute(query, (avatar_id, usuario_id))

            # Confirma tudo
            db.db.commit()
            return Avatar(avatar_id, nome, usuario_id)

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
        query = """
            SELECT av.id, av.nome, c.fk_usuario_id AS usuario_id
            FROM avatar AS av
            INNER JOIN contem c ON c.fk_avatar_id = av.id
            WHERE c.fk_usuario_id = %s
        """
        db.cursor.execute(query, (usuario_id,))
        results = db.cursor.fetchall()
        db.close()
        return [Avatar(**row) for row in results]
