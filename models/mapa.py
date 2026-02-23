import banco.conection as db

class Mapa:
    def __init__(self, id=None, nome=None, descricao=None, epoca=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.epoca = epoca

    def __repr__(self):
        return f"<Mapa id={self.id} nome={self.nome}>"
