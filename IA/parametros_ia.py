import banco.conection as db
import json
from rich.console import Console

console = Console()

class ParametrosIA:
    @staticmethod
    def atualizar(fk_avatar_id, fk_npc_id, resposta_ia_json):
        try:
            data = json.loads(resposta_ia_json)
            with db.Banco() as banco:
                query = f"""
                    INSERT INTO parametros_ia (
                        fk_avatar_id, fk_npc_id, proximidade, reputacao, lealdade, hostilidade, ultimo_evento, observacao
                    )
                VALUES ({fk_avatar_id}, {fk_npc_id}, {data['proximidade']}, {data['reputacao']},
                        {data['lealdade']}, {data['hostilidade']}, NOW(), '{data['justificativa']}')
                ON DUPLICATE KEY UPDATE
                    proximidade = proximidade + {data['proximidade']},
                    reputacao = reputacao + {data['reputacao']},
                    lealdade = lealdade + {data['lealdade']},
                    hostilidade = hostilidade + {data['hostilidade']},
                    ultimo_evento = NOW(),
                    observacao = CONCAT(observacao, '\n', '{data['justificativa']}');
            """
                banco.cursor.execute(query)
                banco.db.commit()
                return True

        except Exception as e:
            console.print("[bold red]Erro ao atualizar parâmetros IA:", e)
            banco.db.rollback()
            return False