class AvatarRep:
    @staticmethod
    def listar_avatares(banco, usuario_id):
        query = """
                SELECT av.id, av.nome, av.fk_mapa_id, c.fk_usuario_id AS usuario_id
                    FROM avatar AS av
                    INNER JOIN contem c ON c.fk_avatar_id = av.id
                    WHERE c.fk_usuario_id = %s
            """
        banco.cursor.execute(query, (usuario_id,))
        return  banco.cursor.fetchall()
    
    @staticmethod
    def buscar_avatar(banco, avatar):
        query = """
                SELECT id FROM avatar WHERE nome = %s
            """
        banco.cursor.execute(query, (avatar,))
        return banco.cursor.fetchone() is not None
    
    @staticmethod
    def criar_avatar(banco, nome, mapa_id):
        query = """
                INSERT INTO avatar (nome, fk_mapa_id) VALUES (%s, %s)
            """
        banco.cursor.execute(query,(nome, mapa_id))
        return banco.cursor.lastrowid
    
    @staticmethod
    def registra_contem(banco, avatar_id, usuario_id):
        query = """
                INSERT INTO contem (fk_avatar_id, fk_usuario_id) VALUES (%s, %s)
            """
        banco.cursor.execute(query, (avatar_id, usuario_id))

    @staticmethod
    def atualizar(banco, mapa_id, avatar_id):
        query = """
                UPDATE avatar SET fk_mapa_id = %s WHERE id = %s
            """
        banco.cursor.execute(query,(mapa_id, avatar_id))