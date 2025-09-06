import banco.conection as db

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
    def listar():
        if not db.open():
            return []
            
        query = "SELECT id, nome, raca, personalidade, profissao, historia_pessoal, fk_mapa_id FROM npcs"
        db.cursor.execute(query)
        results = db.cursor.fetchall()
        db.close()
        return [NPC(**row) for row in results]
