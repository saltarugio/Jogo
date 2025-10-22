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
                query = """
                    INSERT INTO parametros_ia (
                        fk_avatar_id, fk_npc_id, proximidade, reputacao, lealdade, hostilidade, ultimo_evento, observacao
                    ) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
                    ON DUPLICATE KEY UPDATE
                        proximidade = proximidade + %s,
                        reputacao = reputacao + %s,
                        lealdade = lealdade + %s,
                        hostilidade = hostilidade + %s,
                        ultimo_evento = NOW(),
                        observacao = CONCAT(observacao, '\n', %s);
                """
                banco.cursor.execute(query, (
                    fk_avatar_id, fk_npc_id,
                    data['proximidade'], data['reputacao'],
                    data['lealdade'], data['hostilidade'],
                    data['justificativa'],
                    data['proximidade'], data['reputacao'],
                    data['lealdade'], data['hostilidade'],
                    data['justificativa']
                ))
                banco.db.commit()
                return True

        except Exception as e:
            console.print("[bold red]Erro ao atualizar parâmetros IA:", e)
            banco.db.rollback()
            return False