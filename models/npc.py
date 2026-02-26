from rich.console import Console

console = Console()

class NPC:
    def __init__(self, id=None, nome=None, raca=None, personalidade=None, profissao=None, historia_pessoal=None):

        self.id = id
        self.nome = nome
        self.raca = raca
        self.personalidade = personalidade
        self.profissao = profissao
        self.historia_pessoal = historia_pessoal
    
    def __repr__(self):
        return f"<NPC id={self.id} nome={self.nome}>"