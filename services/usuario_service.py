import banco.conection as db
import hashlib
from rich.console import Console
from models.usuario import Usuario, UsarioRed
from repositorios.usuario_rep import UsuarioRep
from services.historico_logon_service import HistoricoLogonService

console = Console()

def hashing_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

class UsuarioService:

    @staticmethod
    def criar_usuario(login, senha):
        if not UsuarioService.busca_usuario(login, senha):
            try:
                with db.Banco() as banco:
                    hashing = hashing_senha(senha)
                    usuario_id = UsuarioRep.criar(banco, login, hashing)
                    return Usuario(usuario_id, login, None, False)
            except Exception as e:
                console.print(f"Erro ao criar usuario: {e}")
                return None
        return None
    
    @staticmethod
    def busca_usuario(login, senha):
        senha_hash = hashing_senha(senha)
        try:
            with db.Banco() as banco:
                usuario = UsuarioRep.buscar_por_login(banco, login)
                
                if not usuario:
                    return None
                
                logado = UsuarioRep.esta_logado(banco, usuario["Id"])

                if not logado:
                    console.print("[bold red] Usuário já esta logado!")
                    return None

                if usuario["senha"] != senha_hash:
                    return None
            
                UsuarioRep.atualiza_logado(banco, 1, usuario["Id"])
                banco.db.commit()

            HistoricoLogonService.registrar_login(usuario["Id"])
            return UsarioRed(usuario["Id"], usuario["nome_usuario"])
        except Exception as e:
            console.print(f"Erro em buscar usuario: {e}")
            return None
        
    @staticmethod
    def atualiza_logado(logado, usuario_id):
        try:
            with db.Banco() as banco:
                UsuarioRep.atualiza_logado(banco, logado, usuario_id)
                banco.db.commit()
                return True
        except Exception as e:
            console.print(f"Erro em atualizar logado: {e}")
            return False
    
    @staticmethod
    def logout(usuario_id):
        HistoricoLogonService.registrar_logout(usuario_id)
        UsuarioService.atualiza_logado(0, usuario_id)
        return True