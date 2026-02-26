import banco.conection as db
from rich.console import Console
from repositorios.avatar_rep import AvatarRep
from models.avatar import Avatar

console = Console()

class AvatarService:

    @staticmethod
    def criar(usuario_id, avatar):
        # avatar = input("Nome do avatar: ")
        try:
            with db.Banco() as banco:
                if AvatarRep.buscar_avatar(banco, avatar):
                    console.print(f"[bold yellow]Nome já em uso!")
                    return None
            
                avatar_id = AvatarRep.criar_avatar(banco, avatar, 1)
                AvatarRep.registra_contem(banco, avatar_id, usuario_id)
                
                banco.db.commit()
                return Avatar(avatar_id, avatar, usuario_id, 1)
        except Exception as e:
            console.print(f"Erro ao registrar avatar: {e}")
            return None
    
    @staticmethod
    def posicao_avatar(mapa_id, avatar_id):
        try:
            with db.Banco() as banco:
                AvatarRep.atualizar(banco, mapa_id, avatar_id)
                banco.db.commit()
                return True
        except Exception as e:
            console.print(f"Erro ao atualizar posição do avatar: {e}")
            return None
    
    @staticmethod
    def lista(usuario_id):
        try:
            with db.Banco() as banco:
               resultado = AvatarRep.listar_avatares(banco, usuario_id)
               return [Avatar(**linha) for linha in resultado]
        except Exception as e:
            console.print(f"Erro em listar avatares: {e}")
            return []
        
    @staticmethod
    def valida_Avatar(avatar_nome: str) -> None:
        if avatar_nome is None:
            return False

        nome = avatar_nome.strip()
        if not nome:
            return False
        
        if " " in avatar_nome:
            return False
        
        return True