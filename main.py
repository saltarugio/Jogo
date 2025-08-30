from rich.console import Console
from models.usuario import Usuario
from models.avatar import Avatar
from models.npc import NPC
from models.historico import Historico

console = Console()

console.print("🎮 Bem-vindo ao [bold green]Mundo Interativo[/]!")
login = input("Digite seu login: ")
senha = input("Digite sua senha: ")

usuario = Usuario.buscar_por_login(login, senha)

if usuario:
    print(f"✅ Bem-vindo de volta, {usuario.nome_usuario}!")

    avatares = usuario.listar_avatar()

    if not avatares:
        print("Você ainda não tem avatares, crie um novo")
        nome_avatar = input("Digite o nome do seu avatar: ")
        avatar = Avatar.criar(usuario.id, nome_avatar)
    else:
        print("Escolha um avatar para jogar:")
        for i, avatar in enumerate(avatares, start=1):
            print(f"{i}. {avatar.nome}")
        escolha = int(input("Digite o número do avatar escolhido: ")) - 1
        avatar = avatares[escolha] if 0 <= escolha < len(avatares) else None
        print(f"Avatar escolhido: {avatar.nome}" if avatar else "Avatar inválido.")
else:
    print("⚠️ Usuário não encontrado!")
    opcao = input("Deseja cadastrar? (s/n): ").lower()
    if opcao == "s":
        novo_usuario = Usuario.criar(login, senha)
        print(f"🎉 Usuário {novo_usuario} criado com sucesso!")
    else:
        print("🚪 Saindo do sistema.")

# Listar NPCs
npcs = NPC.listar()
for npc in npcs:
    print(f"NPC: {npc.nome} ({npc.raca})")

# Registrar uma interação
if avatar and npcs:
    Historico.registrar_interacao(
        fk_avatar_id=avatar.id,
        fk_npc_id=npcs[0].id,
        prompt_usuario="Olá NPC!",
        resposta_ia='{"resposta":"Oi, viajante!"}',
        fk_mapa_id=npcs[0].fk_mapa_id
    )