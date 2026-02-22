from rich.console import Console
from services.postprocesso_resposta import processar_resposta
from services.preprocesso_prompt import substituir_abreviacoes
from  IA.ia import DeepSeekIA
from models.historico import Historico
from IA.parametros_ia import ParametrosIA
from IA.contexto_parametro import montar_contexto_parametros
import time
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from services.linguistica import correcao

console = Console()
COMANDOS_SAIDA = {"sair", "exit", "quit"}

def validador(texto):
    if(len(texto) > 20):
        raise ValidationError(message="Frase muito grande")
    return True


class EncerrarInteracao(Exception):
    pass

class InteracaoService:

    def __init__(self, avatar, npc, mapa_atual):
        self.avatar = avatar
        self.npc = npc
        self.mapa = mapa_atual
    
    def _capturar_texto(self):
        texto = prompt("Você: ", validator=Validator.from_callable(validador)).strip()

        if texto.lower() in COMANDOS_SAIDA:
            console.print("🚪[bold yellow]Encerrando conversa.")
            raise EncerrarInteracao()
        return texto
    
    def _responder_ia(self, texto, historico, contexto_parametros):
        try:
            return DeepSeekIA.gerar_resposta(
                self.npc,
                self.avatar.nome,
                historico,
                texto,
                self.mapa,
                contexto_parametros
            )
        except Exception as e:
            console.print(f"[bold red][NPC] Erro ao responder: {e}")
            return "O NPC ficou em silêncio..."
    
    def _exibir_resposta(self, resposta):
        console.print(f"[bold yellow]{self.npc.nome}: ", end="")
        for letra in resposta:
            console.print(letra, end="", style="white")
            time.sleep(0.02)
        console.print()
        
    def _preprocessar_texto(self, texto):
        verificado = substituir_abreviacoes(texto)
        return correcao(verificado)
    
    def _obter_resposta_npc(self, texto):
        historico = Historico.buscar_por_avatar_e_npc(self.avatar.id, self.npc.id, limite=10)
        parametros_ia = Historico.buscar_parametros_ia(self.avatar.id, self.npc.id)

        contexto = montar_contexto_parametros(parametros_ia, self.avatar, self.npc)

        texto = self._preprocessar_texto(texto)

        resposta_crua = self._responder_ia(texto, historico, contexto)
        resposta =  processar_resposta(resposta_crua, texto, self.npc.nome)
        return texto, resposta
    
    def _avaliar_e_persistir(self, texto, resposta):
        avaliacao = DeepSeekIA.avaliacao_emocional(
            self.npc,
            self.avatar.nome,
            f"O jogador disse: {texto}. O NPC respondeu: {resposta}.",
            self.mapa
        )

        if avaliacao:
            ParametrosIA.atualizar(self.avatar.id, self.npc.id, avaliacao)

        Historico.registrar_interacao(
            fk_avatar_id=self.avatar.id,
            fk_npc_id=self.npc.id,
            prompt_usuario=texto,
            resposta_ia=f'{{"resposta":"{resposta}"}}'
        )
    
    def executar(self):
        try:
            texto = self._capturar_texto()
            texto_corrigido, resposta = self._obter_resposta_npc(texto)
            self._exibir_resposta(resposta)
            self._avaliar_e_persistir(texto_corrigido, resposta)

            return True
        except EncerrarInteracao:
            return False
