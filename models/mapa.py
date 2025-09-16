import banco.conection as db

class Mapa:
    def __init__(self, id=None, nome=None, descricao=None, epoca=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.epoca = epoca

    @staticmethod
    def listar():
        if not db.open():
            return []
        try:
            query = "SELECT id, nome, descricao, epoca FROM mapas ORDER BY id ASC"
            db.cursor.execute(query)
            results = db.cursor.fetchall()
            db.close()
            return [Mapa(**row) for row in results]
        except Exception as e:
            db.close()
            print(f"Erro ao listar mapas: {e}")
            return []

        # mapas = []
        # for row in results:
        #     # se o fetchall for dict
        #     if isinstance(row, dict):
        #         mapas.append(Mapa(
        #             id=row.get("id"),
        #             nome=row.get("nome"),
        #             descricao=row.get("descricao"),
        #             epoca=row.get("epoca")
        #         ))
        #     else:
        #         # se for tuple
        #         mapas.append(Mapa(
        #             id=row[0],
        #             nome=row[1],
        #             descricao=row[2],
        #             epoca=row[3]
        #         ))
        # return mapas