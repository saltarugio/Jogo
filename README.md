# 💬 Chat Dinâmico com NPCs

Um projeto experimental de **inteligência artificial com API híbrida** para gerar diálogos dinâmicos entre o jogador e NPCs em um ambiente de jogo via linha de comando (CLI).  
O objetivo é permitir interações únicas, com respostas adaptáveis baseadas no histórico e nos parâmetros emocionais entre o jogador e cada NPC.

---

## 🚀 Tecnologias Utilizadas

- **Python** — Servidor da IA, lógica de processamento de respostas e motor principal do jogo  
- **MySQL / phpMyAdmin** — Banco de dados de usuários, NPCs e histórico de interações  
- **Ollama + DeepSeek** — Modelo de linguagem híbrido (requisições locais, mas processamento em nuvem devido à limitação de hardware)  
- **Rich Console** — Interface de linha de comando aprimorada para visualização e testes  

---

## 🧠 Funcionalidades Principais

- Diálogo dinâmico entre jogador e NPCs  
- IA híbrida: execução local com processamento em nuvem  
- Parâmetros emocionais que evoluem conforme as interações  
- Histórico de conversas armazenado no banco de dados  

---

## ⚙️ Como Executar

1. **Instale o Ollama**  
   👉 [https://ollama.com/download](https://ollama.com/download)

2. **Baixe e execute o modelo DeepSeek (versão cloud)**  
   ```bash
   ollama run deepseek-v3.1:671b-cloud

3. Instale as dependências **Python**:
   
  pip install requests rich mysql-connector-python
  
4. Configure o banco de dados **MySQL/phpMyAdmin**

   Crie o banco de dados com as tabelas necessárias (usuários, NPCs, parâmetros de IA e histórico).

   Ajuste as credenciais no arquivo de conexão (banco/conection.py).
   
5. **Execute o servidor principal:**
   
   python main.py

---

## 🧩 Estrutura do Projeto

/ChatNPCs

├── /IA

│   ├── ia.py                 # Classe principal de comunicação com o modelo de IA

│   ├── parametros_ia.py      # Sistema de parâmetros emocionais (proximidade, reputação, etc.)

│

├── /models

│   ├── usuario.py            # Representação dos jogadores/usuários

│   ├── avatar.py             # Dados do avatar do jogador

│   ├── npc.py                # Dados e personalidade dos NPCs

│   ├── mapa.py               # Estrutura do mundo e localização dos NPCs

│   └── historico.py          # Registro das interações entre jogador e NPCs

│

├── /python

│   └── servidor.py           # Servidor de comunicação entre jogo e IA

│

├── /banco

│   └── conection.py          # Conexão com o banco MySQL/phpMyAdmin

│

├── main.py                   # Script principal que inicializa o jogo e a IA

└── README.md                 # Documentação do projeto

---

# 💡 Observações

## ⚙️ Sobre a IA:
  O projeto utiliza o Ollama como servidor intermediário para comunicação com o modelo DeepSeek v3.1 (cloud).
  Embora a execução principal do código e a gestão de contexto sejam realizadas localmente, o modelo em si é processado em nuvem.
  Essa abordagem híbrida foi escolhida por limitações de hardware, mantendo o mesmo formato de integração utilizado para execução local completa.
