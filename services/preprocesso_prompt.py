"""
    Pré processamento do prompt do usuário
"""
import re
from services.camnho_json import caminho

def substituir_abreviacoes(texto):
    ABREVIACAO = caminho()
    def troca(match):
        palavra = match.group(0)
        return ABREVIACAO.get(palavra.lower(), palavra)

    return re.sub(r'\b\w+\b', troca, texto)