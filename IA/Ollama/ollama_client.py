import requests

class OllamaClient:

    def __init__(self, config):
        self.url = config["OLLAMA_URL"]
        self.headers = config["OLLAMA_HEADERS"]
        self.model = config["MODEL_NAME"]

    def chat(self, messages, temperature, max_tokens):
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json=payload
            )

            response.raise_for_status()
            resposta = response.json()

            return resposta["message"]["content"]
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP: {e}")
            return None
        except Exception as e:
            print(f"Erro em conseguir resposta: {e}")
            return None