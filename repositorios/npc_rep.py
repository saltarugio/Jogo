import banco.conection as db
from rich.console import Console
from models.npc import NPC

console = Console()

class NpcRep:
    def listar_npc_por_mapa(mapa_id):
        try:
            with db.Banco() as banco:
                query = """
                        SELECT n.id, n.nome, n.raca
                            FROM npc n
                            JOIN contido c ON n.id = c.fk_npc_id
                            WHERE c.fk_mapas_id = %s
                    """
                banco.cursor.execute(query, (mapa_id,))
                resultado = banco.cursor.fetchall()
                return [NPC(**linha) for linha in resultado]
        except Exception as e:
            console.print(f"Erro ao listar NPC: {e}")
            return  []
    
    def busca_complemento_npc(npc_id):
        try:
            with db.Banco() as banco:
                query = """
                        SELECT id, nome, raca, personalidade, profissao, historia_pessoal
                            FROM npc
                            WHERE Id = %s
                    """
                banco.cursor.execute(query, (npc_id,))
                resultado = banco.cursor.fetchone()
                if not resultado:
                    return None
                return NPC(**resultado)
        except Exception as e:
            console.print(f"Erro ao conseguir complemento: {e}")
            return None