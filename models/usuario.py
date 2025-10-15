import banco.conection as db
import hashlib
from models.avatar import Avatar
from rich.console import Console

console = Console()

class Usuario:
    def __init__(self, id, nome_usuario, senha_hash):
        self.id = id
        self.nome_usuario = nome_usuario
        self.senha = senha_hash
    
    @staticmethod
    def hashing_senha(senha):
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    @staticmethod
    def buscar_por_login(nome_usuario, senha):
        try:
            senha_hash = Usuario.hashing_senha(senha)
            with db.Banco() as banco:
                query = "SELECT id, nome_usuario, senha FROM usuario WHERE nome_usuario = %s AND senha = %s"
                banco.cursor.execute(query, (nome_usuario, senha_hash))
                row = banco.cursor.fetchone()
                if row:
                    return Usuario(**row)
                return None
        except Exception as e:
            console.print(f"[bold red]Erro ao buscar usuário: {e}")
            return None

    @staticmethod
    def criar(login, senha):
        try:
            existing_user = Usuario.buscar_por_login(login, senha)

            if not existing_user:
                senha_hash = Usuario.hashing_senha(senha)
                with db.Banco() as banco:
                    query = "INSERT INTO usuario (nome_usuario, senha) VALUES (%s, %s)"
                    banco.cursor.execute(query, (login, senha_hash))
                    banco.db.commit()
                    usuario_id = banco.cursor.lastrowid
                    return Usuario(usuario_id, login, senha_hash)
        except Exception as e:
            console.print(f"[bold red]Erro ao criar usuário: {e}")
            return None

    def listar_avatar(self):
        return Avatar.listar_por_usuario(self.id)
    
