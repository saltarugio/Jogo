import banco.conection as db
from datetime import datetime

class ParametrosIA:
    @staticmethod
    def atualizar(fk_avatar_id, fk_npc_id, evento, observacao=""):
        impactos = {
            "elogio": {"aproximidade": +5, "reputacao": +2, "lealdade": +3, "hostilidade": -2},
            "ajuda": {"aproximidade": +10, "reputacao": +5, "lealdade": +7, "hostilidade": -5},
            "mentira": {"aproximidade": -10, "reputacao": -5, "lealdade": -7, "hostilidade": +5},
            "ameaca": {"aproximidade": -15, "reputacao": -10, "lealdade": -12, "hostilidade": +10},
            "presente": {"aproximidade": +8, "reputacao": +4, "lealdade": +6, "hostilidade": -3},
            "ingnorar": {"aproximidade": -5, "reputacao": -2, "lealdade": -3, "hostilidade": +2},
        }
        impacto = impactos.get(evento, {})
        if not impacto:
            console.print(f"Evento desconhecido: {evento}")
            return False
        
        if not db.open_connection():
            return False
        
        try:
            query = f"""
                INSERT INTO parametros_ia (fk_avatar_id, fk_npc_id, proximidade, reputacao, lealdade, hostilidade, ultimo_evento, observacao)
                VALUES ({fk_avatar_id}, {fk_npc_id}, {impacto['proximidade']}, {impacto['reputacao']}, {impacto['lealdade']}, {impacto['hostilidade']}, NOW(), '{observacao}')
                ON DUPLICATE KEY UPDATE
                    proximidade = proximidade + {impacto['proximidade']},
                    reputacao = reputacao + {impacto['reputacao']},
                    lealdade = lealdade + {impacto['lealdade']},
                    hostilidade = hostilidade + {impacto['hostilidade']},
                    ultimo_evento = NOW(),
                    observacao = CONCAT(observacao, '\n', '{observacao}');
            """
            db.cursor.execute(query)
            db.db.commit()
            return True

        except Exception as e:
            print("Erro ao atualizar parâmetros IA:", e)
            db.db.rollback()
            return False