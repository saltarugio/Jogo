# import banco.conection as db
# import hashlib
# from models.avatar import Avatar
# from rich.console import Console

# console = Console()

class UsarioRed:
    def __init__(self, id, login):
        self.id = id
        self.login = login

class Usuario:
    def __init__(self, id, nome_usuario, senha, logado):
        self.id = id
        self.nome_usuario = nome_usuario
        self.senha = senha
        self.logado = logado
    
    def __repr__(self):
        return f"<Usuário id={self.id} nome={self.nome}>"
    

#     #Passar para usuario_service
#     @staticmethod
#     def hashing_senha(senha):
#         return hashlib.sha256(senha.encode('utf-8')).hexdigest()
#     #-------------------------------------------------------------

#     # Criadas no repositorio
#     @staticmethod
#     def buscar_por_login(login, senha):

#         try:
#             senha_hash = Usuario.hashing_senha(senha)
#             with db.Banco() as banco:
#                 query = "SELECT id, nome_usuario, senha, logado FROM usuario WHERE nome_usuario = %s AND senha = %s"
#                 banco.cursor.execute(query, (login, senha_hash))
#                 row = banco.cursor.fetchone()
#                 if row:
#                     return Usuario(**row)
#                 return None
#         except Exception as e:
#             console.print(f"[bold red]❌ Erro ao buscar usuário: {e}")
#             return None
    
#     @staticmethod
#     def buscar_por_usuario(nome_usuario):
#         try:
#             with db.Banco() as banco:
#                 query = "SELECT id FROM usuario WHERE nome_usuario = %s"
#                 banco.cursor.execute(query, (nome_usuario,))
#                 row = banco.cursor.fetchone()
#                 if row:
#                     return True
#                 return None
#         except Exception as e:
#             console.print(f"[bold red]❌ Erro ao buscar usuário: {e}")
#             return None
#     @staticmethod
#     def criar(login, senha):
#         try:
#             existing_user = Usuario.buscar_por_usuario(login)

#             if not existing_user:
#                 senha_hash = Usuario.hashing_senha(senha)
#                 with db.Banco() as banco:
#                     query = "INSERT INTO usuario (nome_usuario, senha) VALUES (%s, %s)"
#                     banco.cursor.execute(query, (login, senha_hash))
#                     banco.db.commit()
#                     usuario_id = banco.cursor.lastrowid
#                     return Usuario(usuario_id, login, senha_hash)
#             else:
#                 console.print(f"[bold red]Usuário já existente. Escolha outro nome de usuário.")
#                 return None
#         except Exception as e:
#             console.print(f"[bold red]Erro ao criar usuário: {e}")
#             return None

#     def listar_avatar(self):
#         return Avatar.listar_por_usuario(self.id)
    
#     @staticmethod
#     def marcar_logado(usuario_id):
#         try:
#             with db.Banco() as banco:
#                 query = "UPDATE usuario SET logado = %s WHERE id = %s"
#                 banco.cursor.execute(query, (1, usuario_id))
#                 banco.db.commit()
#                 return True
#         except Exception as e:
#             console.print(f"[bold red]Erro ao criar usuário: {e}")
#             return None

#     @staticmethod
#     def marcar_deslogado(usuario_id):
#         try:
#             with db.Banco() as banco:
#                 query = "UPDATE usuario SET logado = %s WHERE id = %s"
#                 banco.cursor.execute(query, (0, usuario_id))
#                 banco.db.commit()
#                 return True
#         except Exception as e:
#             console.print(f"[bold red]Erro ao criar usuário: {e}")
#             return None
# #-------------------------------------------------------------------------------