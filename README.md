# 💬 ChatNPCs - Diálogo Dinâmico com NPCs usando IA

Projeto experimental de **interação dinênmica entre jogador e NPCs** utilizando modelos de linguagem.

O sistema permite que NPCs respondam de forma contextualizada com base em:

- histórico de interações

- parâmetros emocionais

- personalidade do NPC

- contexto do ambiente

As conversas são persistidas em banco de dados e utilizadas para influenciar interações futuras.

---

## 🧠 Conceito

Diferente de sistemas tradicionais de diálogo em jogos (baseados em árvores de decisão), este projeto utiliza IA generativa para produzir respostas dinâmicas.

Cada NPC possui:

- personalidade

- histórico de interações com o jogador

- parâmetros emocionais que evoluem com o tempo

Isso permite criar interações menos previsíveis e mais adaptativas.

---

## ⚙️ Arquitetura

O sistema utiliza uma arquitetura híbrida:

Jogador (CLI)
     │
     ▼
Motor do jogo (Python)
     │
     ▼
Servidor IA
     │
     ▼
Ollama API
     │
     ▼
Modelo DeepSeek (Cloud)

| Componente         | Funcionalidade                          |
| ------------------ | --------------------------------------- |
| Python Game Engine | lógica do jogo e interações             |
| Servidor IA        | montagem de prompt e processamento      |
| Ollama             | gateway de acesso ao modelo             |
| DeepSeek           | geração de linguagem natural            |
| MySQL              | armazenamento de histórico e parâmetros |

---

## 🚀 Tecnologias Utilizadas

- **Python** — Servidor da IA, lógica de processamento de respostas e motor principal do jogo  
- **MySQL / phpMyAdmin** — Banco de dados de usuários, NPCs e histórico de interações  
- **Ollama + DeepSeek** — Modelo de linguagem híbrido (requisições locais, mas processamento em nuvem devido à limitação de hardware)  
- **Rich Console** — Interface de linha de comando aprimorada para visualização e testes  

---

## 🧠 Funcionalidades Principais

- Diálogo dinâmico entre jogador e NPCs

- Armazenamento de histórico de conversas

- Parâmetros emocionais entre jogador e NPC

- Contexto persistente entre interações

- Execução via CLI para testes rápidos

---

## 📦 Estrutura do Projeto

/Jogo

├── /IA

│   ├── Ollama                 

│   │     └── ollama_client.py                     # Gerencia envio do chat pronto para IA

│   ├── prompt

│   │     ├── montar_historico.py                  # Monta o histórico que esta no Banco de dados

│   │     └── montar_prompt.py                     # Monta o prompt que será enviado para IA

│   ├── service_ia                 

│   │     └── chat_service.py                      # Coordena toda parte de montagem/envia do prompt

│   ├── config.py                                  # Configração da IA que será usada

│   ├── contexto_parametro.py                      # Converte os INT para textos expecificos para IA

│   ├── modelo.py                                  # Especifica o modelo que será usado

│   └── parametro_ia.py                            # Registra os parametros da interação

│

├── /models

│   ├── usuario.py                                 # Representação dos jogadores/usuários

│   ├── avatar.py                                  # Representação do Avatar(Boneco do jogo do Jogador)

│   ├── npc.py                                     # Representação dos NPCs (Bonecos não jogaveis)

│   ├── interage_avatar_npc_historico_chat.py      # Representação da interação entre Avatar/NPC

│   ├── mapa.py                                    # Estrutura do mundo e localização dos NPCs

│   └── historico.py                               # Histórico da interação do Jogador/NPC

│

├── /repositorios

│   ├── avatar_rep.py                              # Registra e atualiza Avatar

│   ├── historico_chat_rep.py                      # Registra e atualiza histórico entre jogador e NPC

│   ├── historico_logon_rep.py                     # Registra e atualiza histírico de acesso do jogador

│   ├── interacao_avatar_npc_historico_chat_rep.py # Registra e atualiza interações do jogador/NPC/historico

│   ├── mapa_rep.py                                # Registra a localidades do JOGO

│   ├── npc_rep.py                                 # Registra os NPCs do JOGO

│   └── usuario_rep.py                             # Registra os Jogadores

│

├── /services

│   ├── abreciacoes.json                           # Dataset de abreciações e significado

│   ├── ambiente.py                                # Captura o dispositivo e IP do jogador

│   ├── autenticacao.py                            # Autentica o login do jogador

│   ├── avatar_service.py                          # Coordena Criações/Atualização do Avatar

│   ├── caminho_json.py                            # Centraliza a utilização do Dataset

│   ├── historico_service.py                       # Coordena o Registro do historico do chats

│   ├── historico_logon_service.py                 # Coordena o Registro de login/logout

│   ├── limpeza.py                                 # Limpa de qualquer possível sujeira da resposta da IA

│   ├── linguistica.py                             # Corrige escrita errada e gramátical

│   ├── interacao.py                               # Coordena todo sistema de interação e exibição Jogador/NPC

│   ├── normalizacao.py                            # Limpeza da acentuação do prompt do Jogador

│   ├── postprocesso_resposta.py                   # Coordena a limpeza respota da IA

│   ├── preprocesso_prompt.py                      # Coordena a limpeza do prompt do Jogador

│   └── usuario_service.py                         # Coordena os Registros/Atualização/Buscas dos Jogadores

│

├── /banco

│   └── conection.py                               # Conexão com o banco MySQL/phpMyAdmin

│

├── /arquivos_adionais

│   ├── Diagrama_de_entidades.brM3                 # Diagrama de Entidades feito no brModelo

│   ├── Diagrama_Logico.brM3                       # Diagrama Lógico feito no brModelo

│   ├── Model_Fisico.sql                           # Modelo Fisico para ciaração do Banco

│   └── mundo_interativo.sql                       # Banco Exportado do phpMyAdmin

│

├── main.py                                        # Script principal que inicializa o jogo e a IA

└── README.md                                      # Documentação do projeto

---

## ⚙️ Como Executar

1. **Instale o Ollama**  
  👉 [https://ollama.com/download]
  
   Efetue o login no site do **OLLAMA** e crie uma Api para poder usar o modelo do tipo cloud

2. **Baixe e execute o modelo DeepSeek (versão cloud)**  

   ollama run deepseek-v3.1:671b-cloud

3. Instale as dependências **Python**:
   
  pip install requests rich mysql-connector-python
  
4. Configure o banco de dados **MySQL/phpMyAdmin**

   4.1. Baixe XAMPP.
      https://www.apachefriends.org/pt_br/download.html

   4.2. Execute em **modo Adminstrador** e inicie o **Apache e Mysql**
      Obs.: Para outras formas de banco tera que mexer no arquivo de 
      conexão do banco para efetuar as credenciais de conexão
      de sua preferencia.
   
   4.3. Importe o modelo SQL chamado mundo_interativo.sql dentro do phpmyadmin.

   Ajuste as credenciais no arquivo de conexão (banco/conection.py).
   
5. **Execute o servidor principal:**
   
   python main.py

---

# 💡 Observações

## ⚙️ Sobre a IA:
  O projeto utiliza o **Ollama como servidor intermediário para comunicação com o modelo DeepSeek v3.1 (cloud).**
  Embora o jogo e o gerenciamento de contexto ocorram localmente, o processamento do modelo pode ocorrer em nuvem dependendo da configuração.
  Essa abordagem permite:
- desenvolvimento em máquinas com hardware limitado

- compatibilidade futura com execução totalmente local

- troca simples de modelos

---

## 🔮 Possíveis Evoluções

memória de longo prazo dos NPCs

sistema de reputação global

emoções persistentes

NPCs presentes em múltiplos mapas

treinamento de comportamento específico por NPC

---

## 📜 Licença

Projeto experimental para fins educacionais e de pesquisa em IA aplicada a jogos.

---
