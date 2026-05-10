import banco.conection as bd
from repositorios.mapa_rep import MapasRep as mapa
from repositorios.npc_rep import NpcRep as npc
from repositorios.avatar_rep import AvatarRep as avatar
from rich.console import Console

console = Console()

class Nomes:
    def __init__(self):
        self.nomes = self.busca_nomes()
    
    def busca_nomes(self):
        nomes = set()
        with bd.Banco() as banco:
            nomes.update(mapa.buscar_nome_mapa(banco))
            nomes.update(npc.buscar_nome_npc(banco))
            nomes.update(avatar.busca_nome_avatar(banco))
        return nomes
