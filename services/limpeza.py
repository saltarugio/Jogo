import re

def limpar_resposta_final(texto: str) -> str:
    # Remove blocos <think>
    texto = re.sub(r"<think.*?</think>", "", texto, flags=re.DOTALL | re.IGNORECASE)

    # Remove tokens estilo <|...|>
    texto = re.sub(r"<\|.*?\|>", "", texto)

    # Remove tokens estilo <｜...｜> (variação unicode)
    texto = re.sub(r"<｜.*?｜>", "", texto)

    # Remove placeholders com underline especial
    texto = re.sub(r"place▁holder▁no▁\d+", "", texto)

    # Remove qualquer coisa entre <> suspeita
    texto = re.sub(r"<[^>]+>", "", texto)

    # Remove lixo explícito
    lixo = ["Thinking...", "...done thinking."]
    for l in lixo:
        texto = texto.replace(l, "")

    # Remove linhas duplicadas
    linhas = list(dict.fromkeys(texto.splitlines()))
    texto = "\n".join(linhas)

    return texto.strip()
