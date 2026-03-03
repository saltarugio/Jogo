import banco.conection as db
import json
import re
from rich.console import Console

console = Console()

class ParametrosIA:
    @staticmethod
    def atualizar(fk_avatar_id, fk_npc_id, resposta_ia_json):
        try:
            # json_str = ParametrosIA.extrair_json(resposta_ia_json)
            # json_str = ParametrosIA.limpar_json(json_str)
            if not resposta_ia_json:
                return None
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
                    resposta_ia_json['proximidade'], resposta_ia_json['reputacao'],
                    resposta_ia_json['lealdade'], resposta_ia_json['hostilidade'],
                    resposta_ia_json['justificativa'],
                    resposta_ia_json['proximidade'], resposta_ia_json['reputacao'],
                    resposta_ia_json['lealdade'], resposta_ia_json['hostilidade'],
                    resposta_ia_json['justificativa']
                ))
                banco.db.commit()
                return True

        except Exception as e:
            console.print("[bold red]Erro ao atualizar parâmetros IA:", e)
            # banco.db.rollback()
            return False
    
    # @staticmethod
    # def extrair_json(texto):
    #     match = re.search(r'\{.*\}', texto, re.DOTALL)
    #     if not match:
    #         raise ValueError("Nenhum JSON encontrado na resposta da IA")
    #     return match.group()

    # @staticmethod
    # def limpar_json(json_str):
    #     return re.sub(r':\s*\+(\d+)', r': \1', json_str)