"""
    Autenticação do Login dos usuários
"""
from services.usuario_service import UsuarioService

class UsuarioJaLogado(Exception):
    pass

class AuthService:
    @staticmethod
    def autenticar(login, senha):
        return UsuarioService.busca_usuario(login, senha)