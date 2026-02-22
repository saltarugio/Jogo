"""
    Autenticação do Login dos usuários
"""
from services.ambiente import AmbienteService
from models.usuario import Usuario
from repositorios.historico_logon import HistoricoLogon
from rich.console import Console

console = Console()

class UsuarioJaLogado(Exception):
    pass

class AuthService:
    @staticmethod
    def autenticar(login, senha):
        usuario = Usuario.buscar_por_login(login, senha)

        if not usuario:
            return None
        
        if usuario.logado:
            raise UsuarioJaLogado("Usuário já está logado")
        
        ip = AmbienteService.endereco_ip()
        dispositivo = AmbienteService.obter_dispositivo()

        HistoricoLogon.registrar_historico_login(usuario.id, ip, dispositivo)
        Usuario.marcar_logado(usuario.id)

        return usuario
    
    @staticmethod
    def logout(usuario_id):
        HistoricoLogon.registrar_historico_logout(usuario_id)
        Usuario.marcar_deslogado(usuario_id)