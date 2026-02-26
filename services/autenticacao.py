"""
    Autenticação do Login dos usuários
"""
from services.ambiente import AmbienteService
# from models.usuario import Usuario
from services.usuario_service import UsuarioService
from repositorios.historico_logon_rep import HistoricoLogonRep
from rich.console import Console

console = Console()

class UsuarioJaLogado(Exception):
    pass

class AuthService:
    @staticmethod
    def autenticar(login, senha):
        # usuario = Usuario.buscar_por_login(login, senha)
        return UsuarioService.busca_usuario(login, senha)

        # if not usuario:
        #     return None
        
        # if usuario.logado:
        #     raise UsuarioJaLogado("Usuário já está logado")
        
        # ip = AmbienteService.endereco_ip()
        # dispositivo = AmbienteService.obter_dispositivo()

        # HistoricoLogonRep.registrar_historico_login(usuario.id, ip, dispositivo)
        # # Usuario.marcar_logado(usuario.id)

        # return usuario
    # @staticmethod
    # def logout(usuario_id):
    #     HistoricoLogonRep.registrar_historico_logout(usuario_id)
    #     UsuarioService.marcar_deslogado(usuario_id)