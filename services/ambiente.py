"""
    Classe para com seguir dispositivo esta efetuando o login
"""
import socket
import uuid
from rich.console import Console

console = Console()

class AmbienteService:
    def __init__(self):
        pass

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