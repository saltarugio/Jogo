import json
import re
from services.limpeza import limpar_resposta_final
from services.normalizacao import remover_acentos

def processar_resposta(resposta_crua: str, prompt: str, npc_nome: str) -> str:
    resposta = limpar_resposta_final(resposta_crua)

    if remover_acentos(resposta).lower().strip() == remover_acentos(prompt).lower().strip():
        return f"{npc_nome} parece pensativo, mas decide mudar de assunto."

    return resposta.strip()

def processar_avaliacao(resposta: str) -> str:
    conteudo = resposta.strip()

    # Remove blocos de código tipo ```json ... ```
    if conteudo.startswith("```"):
        conteudo = re.sub(r"^```[a-zA-Z]*", "", conteudo)
        conteudo = conteudo.strip("`").strip()

    try:
        return json.loads(conteudo)
    except json.JSONDecodeError:
        # Se não for JSON, embrulha em um JSON padrão
        return {"erro": "Resposta inválida", "conteudo": conteudo}
