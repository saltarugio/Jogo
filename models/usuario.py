import banco.conection as db
from models.avatar import Avatar

class Usuario:
    def __init__(self, id, nome_usuario, senha):
        self.id = id
        self.nome_usuario = nome_usuario
        self.senha = senha

    @staticmethod
    def buscar_por_login(nome_usuario, senha):
        try:
            if not db.open():
                return None
            query = "SELECT id, nome_usuario, senha FROM usuario WHERE nome_usuario = %s AND senha = %s"
            db.cursor.execute(query, (nome_usuario, senha))
            row = db.cursor.fetchone()
            db.close()
            if row:
                return Usuario(**row)
            return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def criar(login, senha):
        if not db.open():
            return None
        try:
            existing_user = Usuario.buscar_por_login(login, senha)
            if existing_user:
                db.close()
                return None  # Usuário já existe
        except Exception as e:
            print(e)
            db.close()
            return None
        query = "INSERT INTO usuario (nome_usuario, senha) VALUES (%s, %s)"
        db.cursor.execute(query, (login, senha))
        db.db.commit()
        usuario_id = db.cursor.lastrowid
        db.close()
        return Usuario(usuario_id, login, senha)
    
    def listar_avatar(self):
        return Avatar.listar_por_usuario(self.id)
