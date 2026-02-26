from repositorios.historico_logon_rep import HistoricoLogonRep
from services.ambiente import AmbienteService

class HistoricoLogonService:

    @staticmethod
    def registrar_login(usuario):
        ip = AmbienteService.endereco_ip()
        dispositivo = AmbienteService.obter_dispositivo()
        HistoricoLogonRep.registrar_historico_login(usuario, ip, dispositivo)

    @staticmethod
    def registrar_logout(usuario_id):
        HistoricoLogonRep.registrar_historico_logout(usuario_id)