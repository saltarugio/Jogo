class UsuarioRep:
    @staticmethod
    def existe_login(banco, login):
        query = """
                SELECT Id FROM usuario WHERE nome_usuario = %s
            """
        banco.cursor.execute(query, (login,))
        return banco.cursor.fetchone() is not None
    
    @staticmethod
    def criar(banco, login, senha):
        query = """
                INSERT INTO usuario (nome_usuario, senha, logado) VALUES (%s, %s, %s)
            """
        banco.cursor.execute(query, (login, senha, 0))
        banco.db.commit()
        return banco.cursor.lastrowid
    
    @staticmethod
    def atualiza_logado(banco, logado, usuario_id):
        query = """
                UPDATE usuario SET logado = %s WHERE Id = %s
            """
        banco.cursor.execute(query,(logado, usuario_id))
    
    @staticmethod
    def esta_logado(banco, usuario_id):
        query = """
                SELECT Id FROM usuario WHERE Id = %s AND logado = %s
            """
        banco.cursor.execute(query, (usuario_id, 0))
        return banco.cursor.fetchone() is not None
    
    @staticmethod
    def buscar_por_login(banco, login):
        query = """
                SELECT Id, nome_usuario, senha FROM usuario WHERE nome_usuario = %s
            """
        banco.cursor.execute(query, (login,))
        return banco.cursor.fetchone()