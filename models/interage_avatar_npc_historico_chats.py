class InterageAvatarNpcHistoricoChats:
    def __init__(self, id, fk_avatar_id, fk_npc_id, fk_historico_id):
        self.id = id
        self.fk_avatar_id = fk_avatar_id
        self.fk_npc_id = fk_npc_id
        self.fk_historico_id = fk_historico_id
    
    def __repr__(self):
        return f"InterageAvatarNpcHistoricoChats(id={self.id}, fk_avatar_id={self.fk_avatar_id}, fk_npc_id={self.fk_npc_id}, fk_historico_id={self.fk_historico_id})"