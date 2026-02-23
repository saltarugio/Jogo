import banco.conection as db
from models.mapa import Mapa
from rich.console import Console

console = Console()

class MapasRep:
    
    def listar_mapas():
        try:
            with db.Banco() as banco:
                query = """
                        SELECT id, nome, descricao, epoca FROM mapas ORDER BY id ASC
                    """
                banco.cursor.execute(query)
                resultado = banco.cursor.fetchall()
                return [Mapa(**linha) for linha in resultado]
        except Exception as e:
            console.print(f"Erro ao listar mapas: {e}")
            return []