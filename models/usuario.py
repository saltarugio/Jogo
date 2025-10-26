import banco.conection as db
import hashlib
import socket
import uuid
from datetime import datetime
from models.avatar import Avatar
from rich.console import Console

console = Console()

class Usuario:
    def __init__(self, id, nome_usuario, senha, logado):
        self.id = id
        self.nome_usuario = nome_usuario
        self.senha = senha
        self.logado = logado
    @staticmethod
    def hashing_senha(senha):
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    @staticmethod
    def buscar_por_login(nome_usuario, senha):
        try:
            senha_hash = Usuario.hashing_senha(senha)
            with db.Banco() as banco:
                query = "SELECT id, nome_usuario, senha, logado FROM usuario WHERE nome_usuario = %s AND senha = %s"
                banco.cursor.execute(query, (nome_usuario, senha_hash))
                row = banco.cursor.fetchone()
                if row and row['logado'] == 0:
                    return Usuario(**row)
                else:
                    return None
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao buscar usuário: {e}")
            return None
    
    @staticmethod
    def buscar_por_usuario(nome_usuario):
        try:
            with db.Banco() as banco:
                query = "SELECT id FROM usuario WHERE nome_usuario = %s"
                banco.cursor.execute(query, (nome_usuario,))
                row = banco.cursor.fetchone()
                if row:
                    return True
                return None
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao buscar usuário: {e}")
            return None
    @staticmethod
    def criar(login, senha):
        try:
            existing_user = Usuario.buscar_por_usuario(login)

            if not existing_user:
                senha_hash = Usuario.hashing_senha(senha)
                with db.Banco() as banco:
                    query = "INSERT INTO usuario (nome_usuario, senha) VALUES (%s, %s)"
                    banco.cursor.execute(query, (login, senha_hash))
                    banco.db.commit()
                    usuario_id = banco.cursor.lastrowid
                    return Usuario(usuario_id, login, senha_hash)
            else:
                console.print(f"[bold red]Usuário já existente. Escolha outro nome de usuário.")
                return None
        except Exception as e:
            # 
            console.print(f"[bold red]Erro ao criar usuário: {e}")
            return None

    def listar_avatar(self):
        return Avatar.listar_por_usuario(self.id)
    
    @staticmethod
    def endereco_ip():
        """Obtém o endereço IP do usuário."""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao obter endereço IP: {e}")
            return "Desconhecido"
    
    @staticmethod
    def obter_dispositivo():
        """Obtém uma identificação única do dispositivo do usuário."""
        try:
            dispositivo_id = str(uuid.getnode())
            return dispositivo_id
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao obter dispositivo: {e}")
            return "Desconhecido"

    @staticmethod
    def login_usuario(id_usuario):
        """
        Registra login e marca usuário como logado.
        """
        ip = Usuario.endereco_ip()  
        dispositivo = Usuario.obter_dispositivo()  

        try:
            with db.Banco() as banco:
                #Cria um novo registro de login
                query = """
                    INSERT INTO login_historico (usuario_id, data_login, ip, dispositivo)
                    VALUES (%s, %s, %s, %s)
                """
                banco.cursor.execute(query, (id_usuario, datetime.now(), ip, dispositivo))
                banco.db.commit()

                #Atualiza o status de logado do usuário
                update_query = "UPDATE usuario SET logado = %s WHERE id = %s"
                banco.cursor.execute(update_query, (1, id_usuario))
                banco.db.commit()

                console.print(f"[bold green]✅ Login registrado com sucesso.")
                return True
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao registrar login: {e}")
            return None
    
    @staticmethod
    def logout_usuario(id_usuario):
        """
        Atualiza o ultimo registro de login e marca usuário como deslogado.
        """
        try:
            with db.Banco() as banco:
                query = """
                    UPDATE login_historico SET data_logout = %s
                    WHERE usuario_id = %s AND data_logout IS NULL
                    ORDER BY id DESC LIMIT 1
                """
                banco.cursor.execute(query, (datetime.now(), id_usuario))
                banco.db.commit()
               
                # Atualiza o status de logado do usuário
                update_query = "UPDATE usuario SET logado = %s WHERE id = %s"
                banco.cursor.execute(update_query, (0, id_usuario))
                banco.db.commit()
                
                return True
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao buscar usuário logado: {e}")
            return None