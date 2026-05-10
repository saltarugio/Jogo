import requests

class OllamaClient:

    def __init__(self, config):
        self.url = config["OLLAMA_URL"]
        self.headers = config["OLLAMA_HEADERS"]
        self.model = config["MODEL_NAME"]

    def chat(self, messages, temperature, max_tokens, repeat_penalty):
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "repeat_penalty": repeat_penalty
            }
        }
        # Criamos uma sessão para garantir que configurações globais não interfiram
        session = requests.Session()
        session.trust_env = False
        try:
            response = session.post(
                self.url,
                headers=self.headers,
                json=payload
            )

            response.raise_for_status()
            resposta = response.json()

            return resposta.get("message", {}).get("content", "")
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP: {e}")
            return None
        except Exception as e:
            print(f"Erro em conseguir resposta: {e}")
            return None