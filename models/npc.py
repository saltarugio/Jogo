from rich.console import Console
import banco.conection as db

console = Console()

class NPC:
    def __init__(self, id=None, nome=None, raca=None, personalidade=None, profissao=None, historia_pessoal=None):
        self.id = id
        self.nome = nome
        self.raca = raca
        self.personalidade = personalidade
        self.profissao = profissao
        self.historia_pessoal = historia_pessoal

    @staticmethod
    def listar_por_mapa(mapa_id):
        try:
            with db.Banco() as banco:
                query = """
                            SELECT n.id, n.nome, n.raca, n.personalidade, n.profissao, n.historia_pessoal
                            FROM npc n
                            JOIN contido c ON n.id = c.fk_npc_id
                            WHERE c.fk_mapas_id = %s
                        """
                banco.cursor.execute(query, (mapa_id,))
                results = banco.cursor.fetchall()
                return [NPC(**row) for row in results]
        except Exception as e:
            console.print(f"[bold red]Erro ao listar NPCs: {e}")
            return []