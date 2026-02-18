import unicodedata

def remover_acentos(texto: str) -> str:
    nfkd_form = unicodedata.normalize("NFD", texto)
    return "".join(
        c for c in nfkd_form if not unicodedata.combining(c)
    )