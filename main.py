from rich.console import Console
from models.usuario import Usuario
from models.avatar import Avatar
from models.npc import NPC
from models.historico import Historico
from models.mapa import Mapa  # precisa existir

console = Console()

console.print("🎮 Bem-vindo ao [bold green]Mundo Interativo[/]!")

# ----------------- LOGIN LOOP -----------------
usuario = None
while not usuario:
    login = input("Digite seu login: ")
    senha = input("Digite sua senha: ")

    usuario = Usuario.buscar_por_login(login, senha)

    if not usuario:
        console.print("⚠️ Usuário não encontrado ou senha incorreta!")
        opcao = input("Deseja [l]ogin novamente, [c]adastrar ou [s]air? ").lower()

        if opcao == "c":
            novo_usuario = Usuario.criar(login, senha)
            console.print(f"🎉 Usuário {novo_usuario.nome_usuario} criado com sucesso!")
            usuario = novo_usuario
        elif opcao == "s":
            console.print("🚪 Saindo do sistema.")
            exit()
        else:
            usuario = None

console.print(f"✅ Bem-vindo de volta, {usuario.nome_usuario}!")

# ----------------- AVATAR -----------------
avatar = None
avatares = usuario.listar_avatar()

if not avatares:
    console.print("⚠️ Você ainda não tem avatares, crie um novo para jogar.")
    nome_avatar = input("Digite o nome do seu avatar: ")
    avatar = Avatar.criar(nome_avatar, usuario.id)
else:
    while not avatar:
        console.print("\nEscolha um avatar para jogar:")
        for i, avatar_item in enumerate(avatares, start=1):
            print(f"{i}. {avatar_item.nome}")

        try:
            console.print("Escolha um avatar da lista, ou digite 0 para criar um novo:")
            escolha = int(input("Digite o número do avatar escolhido: ")) - 1
            if escolha == -1:
                console.print("Criação de um novo avatar...")
                nome_avatar = input("Digite o nome do seu avatar: ")
                avatar = Avatar.criar(nome_avatar, usuario.id)
                avatares = usuario.listar_avatar()

            avatar = avatares[escolha] if 0 <= escolha < len(avatares) else None
            
        except ValueError:
            avatar = None
            
        if not avatar:
            console.print("⚠️ Avatar inválido. Tente novamente.")

console.print(f"🎭 Avatar escolhido: [bold cyan]{avatar.nome}[/]")

# ----------------- MAPAS E LOOP PRINCIPAL -----------------
mapas = Mapa.listar()  # precisa retornar todos os mapas em ordem (id crescente)
indice_mapa = 0  # começa no primeiro mapa
mapa_atual = mapas[indice_mapa]
while True:
    console.print(f"\n🗺️ Você está no mapa: [bold green]{mapa_atual.nome}[/]")

    # listar NPCs do mapa
    npcs = NPC.listar_por_mapa(mapa_atual.id)

    # menu principal
    if npcs:
        console.print("Escolha uma ação:")
        console.print("c. Conversar com NPC")
        console.print("m. Mudar de mapa")
    else:
        console.print("⚠️ Não há NPCs neste mapa.")
        console.print("Você só pode [m]udar de mapa")
    if(len(mapas) < 1):
        console.print("⚠️ Nenhum mapa cadastrado!")

    escolha = input("Digite sua escolha: ").lower()

    if escolha == "c" and npcs:
        console.print("\nEscolha um NPC para conversar:")
        for i, npc in enumerate(npcs, start=1):
            print(f"{i}. {npc.nome} ({npc.raca})")

        try:
            escolha_npc = int(input("Digite o número do NPC: ")) - 1
            npc_escolhido = npcs[escolha_npc] if 0 <= escolha_npc < len(npcs) else None
        except ValueError:
            npc_escolhido = None

        if npc_escolhido:
            console.print(f"\n💬 Conversando com [bold yellow]{npc_escolhido.nome}[/]...\n")
            while True:
                prompt = input("Você: ")
                if prompt.lower() in ["sair", "exit", "quit"]:
                    console.print("🚪 Encerrando conversa.")
                    Avatar.atualiza_posicao_avatar(avatar.id, mapa_atual.id)
                    break

                
                # busca histórico
                historico = Historico.buscar_por_avatar_e_npc(avatar.id, npc_escolhido.id, limite=10)
                # obtém resposta do NPC via IA
                resposta = NPC.responder(npc_escolhido, prompt, avatar.id, historico, mapa_atual)
                print(resposta)

                # registra no histórico
                Historico.registrar_interacao(
                    fk_avatar_id=avatar.id,
                    fk_npc_id=npc_escolhido.id,
                    prompt_usuario=prompt,
                    resposta_ia=f'{{"resposta":"{resposta}"}}',
                )
        else:
            console.print("⚠️ NPC inválido.")

    elif escolha == "m":
        # navegação entre mapas
        if indice_mapa == 0:  # primeiro mapa
            console.print("Você só pode ir para o [p]róximo mapa.")
            if input("Ir para o próximo? (s/n) ").lower() == "s":
                indice_mapa += 1
        elif indice_mapa == len(mapas) - 1:  # último mapa
            console.print("Você só pode voltar para o [a]nterior.")
            if input("Voltar para o anterior? (s/n) ").lower() == "s":
                indice_mapa -= 1
        else:
            console.print("Você pode ir para o [a]nterior ou [p]róximo.")
            direcao = input("Escolha [a] ou [p]: ").lower()
            if direcao == "a":
                indice_mapa -= 1
            elif direcao == "p":
                indice_mapa += 1

        mapa_atual = mapas[indice_mapa]

    else:
        console.print("⚠️ Opção inválida.")
