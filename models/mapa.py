import banco.conection as db

class Mapa:
    def __init__(self, id=None, nome=None, descricao=None, epoca=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.epoca = epoca

    @staticmethod
    def listar():
        with db.Banco() as banco:
            try:
                query = "SELECT id, nome, descricao, epoca FROM mapas ORDER BY id ASC"
                banco.cursor.execute(query)
                results = banco.cursor.fetchall()
                return [Mapa(**row) for row in results]
            except Exception as e:
                print(f"Erro ao listar mapas: {e}")
                return []
