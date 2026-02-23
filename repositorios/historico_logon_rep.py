import banco.conection as db
from datetime import datetime
from rich.console import Console

console = Console()

class HistoricoLogonRep:
    @staticmethod
    def registrar_historico_login(usuario_id,ip, dispositivo):
        try:
            with db.Banco() as banco:
                query = """
                    INSERT INTO historico_logon (usuario_id, data_login, ip, dispositivo)
                    VALUES (%s, %s, %s, %s)
                """
                banco.cursor.execute(query, (usuario_id, datetime.now(), ip, dispositivo))
                banco.db.commit()
                return True
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao registrar: {e}")
            return None
    
    @staticmethod
    def registrar_historico_logout(usuario_id):
        """
        Atualiza o ultimo registro de login e marca usuário como deslogado.
        """
        try:
            with db.Banco() as banco:
                query = """
                    UPDATE historico_logon SET data_logout = %s
                    WHERE usuario_id = %s AND data_logout IS NULL
                    ORDER BY id_historico_logon DESC LIMIT 1
                """
                banco.cursor.execute(query, (datetime.now(), usuario_id))
                banco.db.commit()
                
                return True
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao buscar usuário logado: {e}")
            return None