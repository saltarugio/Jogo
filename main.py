import subprocess
import time
import requests
import logging
import getpass
from rich.console import Console
from models.usuario import Usuario
from models.avatar import Avatar
from models.npc import NPC
from models.mapa import Mapa

#------------------- CONFIGURAÇÃO --------------------
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MAX_WAIT = 10  # segundos

console = Console()
logging.basicConfig(filename="game.log", level=logging.ERROR)

#----------------- Utilitários de Mensagens -----------------
def msg_sucesso(texto):
    console.print(f"[bold green]✅ {texto}[/]")

def msg_info(texto):
    console.print(f"[bold blue]ℹ️ {texto}[/]")

def msg_alerta(texto):
    console.print(f"[bold yellow]⚠️ {texto}[/]")

def msg_erro(texto):
    console.print(f"[bold red]❌ {texto}[/]")

# --------------------- OLLAMA -------------------------------
def ollama():
    """Garante que o Ollama está rodando, tentando iniciar se necessário."""
    try:
        requests.get(OLLAMA_URL, timeout=3)
        return True
    except requests.exceptions.RequestException:
        msg_alerta("Ollama não encontrado. Tentando iniciar o servidor...")
    
    try:
        subprocess.Popen(['ollama', 'serve'])
        for i in range(OLLAMA_MAX_WAIT):
            time.sleep(1)
            try:
                requests.get(OLLAMA_URL, timeout=2)
                return True
            except requests.exceptions.RequestException:
                continue
        msg_erro("Tempo esgotado ao tentar iniciar o Ollama.")
        return False
    except Exception as e:
        msg_erro(f"Erro ao iniciar o Ollama: {e}")
        logging.error(f"Erro ao iniciar o Ollama: {e}")
        return False
    
# ----------------- LOGIN LOOP -----------------
def menu_login():
    usuario = None

    while not usuario:
        msg_alerta("🔐 Por favor, faça o login ou cadastre-se.")
        opcao = input("Deseja [l]ogin, [c]adastrar ou [s]air? ").lower()
        if opcao == "c":
            login = input("Escolha um login: ")
            senha = getpass.getpass("Escolha uma senha: ")
            conf_senha = getpass.getpass("Confirme sua senha: ")
            if senha != conf_senha:
                msg_erro("As senhas não coincidem.")
                continue
            elif opcao == "s":
                msg_info("🚪 Saindo do sistema.")
                exit()
            else:
                usuario = Usuario.criar(login, senha)
                msg_info(f"🎉 Usuário {usuario.nome_usuario} criado com sucesso!")
            continue
        elif opcao == "l":
            login = input("Digite seu login: ")
            senha = getpass.getpass("Digite sua senha: ")
            usuario = Usuario.buscar_por_login(login, senha)

            if not usuario:
                msg_erro("Usuário não encontrado ou senha incorreta!")
                usuario = None
                continue
        else:
            msg_erro("Opção inválida.")
            continue
    msg_info(f"✅ Bem-vindo de volta, {usuario.nome_usuario}!")
    return usuario

# ----------------- AVATAR -----------------
def menu_avatar(usuario):
    """Gerencia a seleção ou criação de avatar."""
    avatares = usuario.listar_avatar()

    if not avatares:
        msg_alerta("⚠️ Você ainda não tem avatares, crie um novo para jogar.")
        nome_avatar = input("Digite o nome do seu avatar: ")
        avatar = Avatar.criar(nome_avatar, usuario.id)
        if not avatar:
            msg_erro("Erro ao criar avatar. Tente novamente.")
            return menu_avatar(usuario)
        else:
            msg_sucesso(f"🎉 Avatar {avatar.nome} criado com sucesso!")
        return avatar
    while True:
        console.print("\nEscolha um avatar para jogar:")
        for i, avatar_item in enumerate(avatares, start=1):
            console.print(f"{i}. {avatar_item.nome}")
        
        escolha = input("Escolha um avatar da lista, ou digite 0 para criar um novo: ")
        
        try:
            escolha = int(escolha)
        except ValueError:
            msg_erro("Escolha inválida. Tente novamente.")
            continue

        if escolha == 0:
            nome_avatar = input("Digite o nome do seu avatar: ")
            avatar = Avatar.criar(nome_avatar, usuario.id)
            if not avatar:
                msg_erro("Erro ao criar avatar. Tente novamente.")
                continue
            else:
                msg_sucesso(f"🎉 Avatar {avatar.nome} criado com sucesso!")
                return avatar
        elif 1 <= escolha <= len(avatares):
            avatar = avatares[escolha - 1]
            msg_sucesso(f"🎭 Avatar escolhido: {avatar.nome}")
            return avatar
        else:
            msg_erro("Escolha inválida. Tente novamente.")

# ----------------- CONVERSA COM NPC -----------------
def conversar_com_npc(avatar, mapa_atual):
    """Gerencia a seleção de NPC e a conversa."""
    npcs = NPC.listar_por_mapa(mapa_atual.id)

    if not npcs:
        msg_alerta("⚠️ Não há NPCs neste mapa.")
        return
    
    console.print("\nEscolha um NPC para conversar:")
    for i, npc in enumerate(npcs, start=1):
        console.print(f"{i}. {npc.nome} ({npc.raca})")
    
    try:
        escolha_npc = int(input("Digite o número do NPC: ")) - 1
        npc_escolhido = npcs[escolha_npc] if 0 <= escolha_npc < len(npcs) else None
    except ValueError:
        npc_escolhido = None
    
    if not npc_escolhido:
        msg_erro("NPC inválido.")
        return
    msg_info(f"💬 Conversando com {npc_escolhido.nome}...\n")
    while True:
        resposta = NPC.executa_interacao(avatar, npc_escolhido, mapa_atual)
        if resposta is False:
            break

# ----------------- MAPAS E LOOP PRINCIPAL -----------------
def loop_principal(avatar):
    """Gerencia a navegação entre mapas e interações."""
    mapas = Mapa.listar()  # precisa retornar todos os mapas em ordem (id crescente)
    if not mapas:
        msg_erro("⚠️ Nenhum mapa cadastrado!")
        exit()
    indice_mapa = avatar.fk_mapa_id - 1  # começa no mapa do avatar

    while True:
        mapa_atual = mapas[indice_mapa]
        console.print(f"\n🗺️ Você está no mapa: [bold green]{mapa_atual.nome}[/] \n")
        npcs = NPC.listar_por_mapa(mapa_atual.id)

        msg_info("Ações disponíveis:")
        if npcs:
            console.print("c. Conversar com NPC")
        console.print("m. Mudar de mapa")
        console.print("q. Sair do jogo")
        
        escolha = input("Escolha uma opção: ").lower()

        if escolha == "c" and npcs:
            conversar_com_npc(avatar, mapa_atual)
        elif escolha == "m":
            if indice_mapa == 0:  # primeiro mapa
                msg_info("Você só pode ir para o [p]róximo mapa.")
                if input("Ir para o próximo? (s/n) ").lower() == "s":
                    indice_mapa += 1
            elif indice_mapa == len(mapas) - 1:  # último mapa
                msg_info("Você só pode voltar para o [a]nterior.")
                if input("Voltar para o anterior? (s/n) ").lower() == "s":
                    indice_mapa -= 1
            else:
                msg_info("Você pode ir para o [a]nterior ou [p]róximo.")
                if input("Escolha [a] ou [p]: ").lower() == "a":
                    indice_mapa -= 1
                else:
                    indice_mapa += 1
            avatar.atualiza_posicao_avatar(avatar.id, mapas[indice_mapa].id)
        elif escolha == "q":
            msg_info("🚪 Saindo do jogo. Até a próxima!")
            break
        else:
            msg_erro("Opção inválida. Tente novamente.")

# ----------------- INÍCIO DO JOGO -----------------
def main():
    console.print("🎮 Bem-vindo ao [bold green]Mundo Interativo[/]!")
    if not ollama():
        msg_erro("Não foi possível conectar ao Ollama. Verifique se o Ollama está instalado e configurado corretamente.")
        exit()
    
    usuario = menu_login()
    avatar = menu_avatar(usuario)
    loop_principal(avatar)

if __name__ == "__main__":
    main()