from rich.console import Console
from models.usuario import Usuario
from models.avatar import Avatar
from models.npc import NPC
from models.historico import Historico

console = Console()

console.print("🎮 Bem-vindo ao [bold green]Mundo Interativo[/]!")

usuario = None

# ----------------- LOGIN LOOP -----------------
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
            usuario = None  # força nova tentativa no loop

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
            console.print("Escolha um avatar da lista, caso queira criar um novo avatar digite 0:")
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

# ----------------- NPC CHAT -----------------
npcs = NPC.listar()
npc_escolhido = None

while not npc_escolhido:
    if not npcs:
        console.print("⚠️ Nenhum NPC disponível no momento.")
        exit()

    console.print("\nEscolha um NPC para conversar:")
    for i, npc in enumerate(npcs, start=1):
        print(f"{i}. {npc.nome} ({npc.raca})")

    try:
        escolha_npc = int(input("Digite o número do NPC: ")) - 1
        npc_escolhido = npcs[escolha_npc] if 0 <= escolha_npc < len(npcs) else None
    except ValueError:
        npc_escolhido = None

    if not npc_escolhido:
        console.print("⚠️ NPC inválido. Encerrando o jogo.")
        npc_escolhido = None

console.print(f"\n💬 Conversando com [bold yellow]{npc_escolhido.nome}[/]...\n")

while True:
        prompt = input("Você: ")
        if prompt.lower() in ["sair", "exit", "quit"]:
            console.print("🚪 Encerrando conversa.")
            break

        # Aqui futuramente entra a IA
        resposta = f"{npc_escolhido.nome} diz: 'Ainda não tenho respostas dinâmicas.'"

        print(resposta)

        # Registrar no histórico
        Historico.registrar_interacao(
            fk_avatar_id=avatar.id,
            fk_npc_id=npc_escolhido.id,
            prompt_usuario=prompt,
            resposta_ia=f'{{"resposta":"{resposta}"}}',
            fk_mapa_id=npc_escolhido.fk_mapa_id
        )
