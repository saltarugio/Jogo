import banco.conection as db
from  IA.ia import DeepSeekIA

class NPC:
    def __init__(self, id=None, nome=None, raca=None, personalidade=None, profissao=None, historia_pessoal=None, fk_mapa_id=None):
        self.id = id
        self.nome = nome
        self.raca = raca
        self.personalidade = personalidade
        self.profissao = profissao
        self.historia_pessoal = historia_pessoal
        self.fk_mapa_id = fk_mapa_id

    @staticmethod
    def listar_por_mapa(mapa_id):
        if not db.open():
            return []
        try:
            query = """
                        SELECT n.id, n.nome, n.raca, n.personalidade, n.profissao, n.historia_pessoal
                        FROM npc n
                        JOIN contido c ON n.id = c.fk_npc_id
                        WHERE c.fk_mapas_id = %s
                    """
            db.cursor.execute(query, (mapa_id,))
            results = db.cursor.fetchall()
            db.close()
            return [NPC(**row) for row in results]
        except Exception as e:
            db.close()
            print(f"Erro ao listar NPCs: {e}")
            return []     

    @staticmethod
    def responder(npc, prompt, avatar_id, historico, mapa):
        try:
            resposta = DeepSeekIA.gerar_resposta(npc, avatar_id, historico, prompt, mapa)
            return resposta
        except Exception as e:
            print(f"[NPC] Erro ao responder: {e}")
            return "O NPC ficou em silêncio..."
