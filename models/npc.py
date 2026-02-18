from rich.console import Console
import banco.conection as db
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


def validador(texto):
    if(len(texto) > 20):
        raise ValidationError(message="Frase muito grande")
    return True

class NPC:
    def __init__(self, id=None, nome=None, raca=None, personalidade=None, profissao=None, historia_pessoal=None, fk_mapa_id=None):
        self.id = id
        self.nome = nome
        self.raca = raca
        self.personalidade = personalidade
        self.profissao = profissao
        self.historia_pessoal = historia_pessoal
        self.fk_mapa_id = fk_mapa_id

    @staticmethod
    def listar_por_mapa(mapa_id):
        try:
            with db.Banco() as banco:
                query = """
                            SELECT n.id, n.nome, n.raca, n.personalidade, n.profissao, n.historia_pessoal
                            FROM npc n
                            JOIN contido c ON n.id = c.fk_npc_id
                            WHERE c.fk_mapas_id = %s
                        """
                banco.cursor.execute(query, (mapa_id,))
                results = banco.cursor.fetchall()
                return [NPC(**row) for row in results]
        except Exception as e:
            console.print(f"[bold red]Erro ao listar NPCs: {e}")
            return []     

    @staticmethod
    def responder(npc, texto, avatar_id, historico, mapa, contexto_parametros):
        try:
            resposta = DeepSeekIA.gerar_resposta(npc, avatar_id, historico, texto, mapa, contexto_parametros)
            return resposta
        except Exception as e:
            console.print(f"[bold red][NPC] Erro ao responder: {e}")
            return "O NPC ficou em silêncio..."
    
    @staticmethod
    def executa_interacao(avatar, npc, mapa_atual):
        texto = prompt("Você: ", validator=Validator.from_callable(validador))
        
        if texto.lower() in ["sair", "exit", "quit"]:
            console.print("🚪[bold yellow]Encerrando conversa.")
            return False

        historico = Historico.buscar_por_avatar_e_npc(avatar.id, npc.id, limite=10)
        parametros_ia = Historico.buscar_parametros_ia(avatar.id, npc.id)

        contexto_parametros = montar_contexto_parametros(parametros_ia, avatar, npc)
        
        #Verificação e subtituição de abreviações
        texto_verificado = substituir_abreviacoes(texto)

        # Corretor de palavras escritas erradas e ortografia
        texto_corrigido = correcao(texto_verificado)

        #IA retorna TEXTO CRU
        resposta_crua = NPC.responder(npc, texto_corrigido, avatar.nome, historico, mapa_atual, contexto_parametros)
        console.print(f"[bold yellow]{npc.nome}: ", end='')
        if resposta_crua == None:
            return console.print(f'não foi possivel uma resposta')
        
        # pós-processamento centralizado
        resposta = processar_resposta(resposta_crua,texto_corrigido, npc.nome)
        
        for letra in resposta:
            console.print(f"{letra}", end='', style="white")
            time.sleep(0.02)  # Ajuste o tempo para controlar a velocidade da "digitação"
        console.print()  # Nova linha após a resposta

        avaliacao = DeepSeekIA.avaliacao_emocional(
            npc,
            avatar.nome,
            f"O jogador disse: {texto_corrigido}. O NPC respondeu: {resposta}.",
            mapa_atual
        )

        if avaliacao:
            ParametrosIA.atualizar(avatar.id, npc.id, avaliacao)

        Historico.registrar_interacao(
            fk_avatar_id=avatar.id,
            fk_npc_id=npc.id,
            prompt_usuario=texto_corrigido,
            resposta_ia=f'{{"resposta":"{resposta}"}}'
        )
        return True