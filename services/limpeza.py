import re

def limpar_resposta_final(texto: str) -> str:
    texto = re.sub(
        r"<think.*?</think>",
        "",
        texto,
        flags=re.DOTALL | re.IGNORECASE
    )

    lixo = ["Thinking...", "...done thinking.", "<think>", "</think>"]
    for l in lixo:
        texto = texto.replace(l, "")

    linhas = list(dict.fromkeys(texto.splitlines()))
    texto = "\n".join(linhas)

    return texto.strip()
