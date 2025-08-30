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
        query = "INSERT INTO avatares (nome, usuario_id) VALUES (%s, %s)"
        db.cursor.execute(query, (nome, usuario_id))
        db.db.commit()
        avatar_id = db.cursor.lastrowid
        db.close()
        return Avatar(avatar_id, nome, usuario_id)

    @staticmethod
    def listar_por_usuario(usuario_id):
        if not db.open():
            return []
        query = "SELECT id, usuario_id, nome FROM avatares WHERE usuario_id = %s"
        db.cursor.execute(query, (usuario_id,))
        results = db.cursor.fetchall()
        db.close()
        return [Avatar(**row) for row in results]
