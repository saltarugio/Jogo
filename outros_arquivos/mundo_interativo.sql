-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 10/02/2026 às 22:36
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `mundo_interativo`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `avatar`
--

CREATE TABLE `avatar` (
  `Id` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `fk_mapa_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `avatar`
--

INSERT INTO `avatar` (`Id`, `nome`, `criado_em`, `fk_mapa_id`) VALUES
(2, 'conta1', '2026-02-10 09:57:41', 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `contem`
--

CREATE TABLE `contem` (
  `fk_Avatar_Id` int(11) NOT NULL,
  `fk_Usuario_Id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `contem`
--

INSERT INTO `contem` (`fk_Avatar_Id`, `fk_Usuario_Id`) VALUES
(2, 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `contido`
--

CREATE TABLE `contido` (
  `fk_NPC_Id` int(11) NOT NULL,
  `fk_Mapas_Id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `contido`
--

INSERT INTO `contido` (`fk_NPC_Id`, `fk_Mapas_Id`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 2),
(7, 1),
(7, 3),
(8, 5),
(9, 4),
(10, 5);

-- --------------------------------------------------------

--
-- Estrutura para tabela `historico_chats`
--

CREATE TABLE `historico_chats` (
  `Id` int(11) NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `mensagem_usuario` text NOT NULL,
  `resposta_ai` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `historico_chats`
--

INSERT INTO `historico_chats` (`Id`, `criado_em`, `mensagem_usuario`, `resposta_ai`) VALUES
(1, '2026-02-10 14:44:48', 'Olá, quem ', '{\"resposta\":\"Saudações, viajante. Sou Elandor, o guardião destas ruínas ancestrais.\"}'),
(2, '2026-02-10 14:54:02', 'o que faz ', '{\"resposta\":\"Minha tarefa é proteger os segredos ancestrais que repousam nestas pedras. Os ecos da antiga civilização élfica não podem ser esquecidos.\"}');

-- --------------------------------------------------------

--
-- Estrutura para tabela `historico_logon`
--

CREATE TABLE `historico_logon` (
  `id_historico_logon` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `data_login` datetime NOT NULL,
  `data_logout` datetime DEFAULT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `dispositivo` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `historico_logon`
--

INSERT INTO `historico_logon` (`id_historico_logon`, `usuario_id`, `data_login`, `data_logout`, `ip`, `dispositivo`) VALUES
(1, 1, '2026-02-10 09:32:02', NULL, '10.210.5.31', '110073160889140'),
(2, 1, '2026-02-10 09:45:08', NULL, '10.210.5.31', '110073160889140'),
(3, 1, '2026-02-10 09:57:33', NULL, '10.210.5.31', '110073160889140'),
(4, 1, '2026-02-10 10:53:11', NULL, '10.210.5.31', '110073160889140'),
(5, 1, '2026-02-10 10:58:30', NULL, '10.210.5.31', '110073160889140'),
(6, 1, '2026-02-10 11:01:14', NULL, '10.210.5.31', '110073160889140'),
(7, 1, '2026-02-10 11:18:16', NULL, '10.210.5.31', '110073160889140'),
(8, 1, '2026-02-10 11:39:24', '2026-02-10 11:40:14', '10.210.5.31', '110073160889140'),
(9, 1, '2026-02-10 11:44:24', NULL, '10.210.5.31', '110073160889140'),
(10, 1, '2026-02-10 14:28:30', NULL, '192.168.0.103', '110073160889140'),
(11, 1, '2026-02-10 14:43:33', '2026-02-10 14:49:59', '192.168.0.103', '110073160889140'),
(12, 1, '2026-02-10 14:51:02', '2026-02-10 15:25:03', '192.168.0.103', '110073160889140');

-- --------------------------------------------------------

--
-- Estrutura para tabela `interage_avatar_npc_historico_chats`
--

CREATE TABLE `interage_avatar_npc_historico_chats` (
  `fk_avatar_Id` int(11) NOT NULL,
  `fk_npc_Id` int(11) NOT NULL,
  `fk_historico_id` int(11) NOT NULL,
  `data_interacao` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `interage_avatar_npc_historico_chats`
--

INSERT INTO `interage_avatar_npc_historico_chats` (`fk_avatar_Id`, `fk_npc_Id`, `fk_historico_id`, `data_interacao`) VALUES
(2, 1, 1, '2026-02-10 14:44:48'),
(2, 1, 2, '2026-02-10 14:54:02');

-- --------------------------------------------------------

--
-- Estrutura para tabela `localizado`
--

CREATE TABLE `localizado` (
  `fk_Historico_chats_Id` int(11) NOT NULL,
  `fk_Mapas_Id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `mapas`
--

CREATE TABLE `mapas` (
  `Id` int(11) NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `epoca` varchar(100) DEFAULT NULL,
  `descricao` text NOT NULL,
  `nome` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `mapas`
--

INSERT INTO `mapas` (`Id`, `criado_em`, `epoca`, `descricao`, `nome`) VALUES
(1, '2026-02-10 09:54:08', 'Era Antiga', 'Um vale fértil cercado por montanhas antigas e ruínas élficas.', 'Vale de Eldoria'),
(2, '2026-02-10 09:54:08', 'Era do Aço', 'Uma cidade industrial conhecida por suas forjas e comércio intenso.', 'Cidade de Ferrobrum'),
(3, '2026-02-10 09:54:08', 'Era Antiga', 'Floresta densa e mágica, lar de criaturas místicas e povos antigos.', 'Floresta de Nyssara'),
(4, '2026-02-10 09:54:08', 'Era das Areias', 'Um deserto implacável com cidades subterrâneas e segredos perdidos.', 'Deserto de Kal-Zhar'),
(5, '2026-02-10 09:54:08', 'Era Mercantil', 'Cidade costeira movimentada, ponto central de comércio marítimo.', 'Porto de Almaris');

-- --------------------------------------------------------

--
-- Estrutura para tabela `npc`
--

CREATE TABLE `npc` (
  `Id` int(11) NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `historia_pessoal` text NOT NULL,
  `nome` varchar(50) NOT NULL,
  `personalidade` varchar(100) DEFAULT NULL,
  `profissao` varchar(20) DEFAULT NULL,
  `atualizado_em` datetime DEFAULT NULL,
  `raca` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `npc`
--

INSERT INTO `npc` (`Id`, `criado_em`, `historia_pessoal`, `nome`, `personalidade`, `profissao`, `atualizado_em`, `raca`) VALUES
(1, '2026-02-10 09:54:20', 'Antigo guardião élfico que jurou proteger as ruínas de Eldoria.', 'Elandor', 'Sábio e reservado', 'Guardião', NULL, 'Elfo'),
(2, '2026-02-10 09:54:20', 'Cresceu nas forjas de Ferrobrum e virou mestre ferreiro.', 'Brakka Punho-de-Ferro', 'Rude, mas leal', 'Ferreiro', NULL, 'Anão'),
(3, '2026-02-10 09:54:20', 'Criada pela floresta, fala com espíritos antigos.', 'Nymera', 'Calma e misteriosa', 'Druida', NULL, 'Humana'),
(4, '2026-02-10 09:54:20', 'Sobreviveu às tempestades de areia e virou guia do deserto.', 'Zarim', 'Desconfiado e astuto', 'Guia', NULL, 'Humano'),
(5, '2026-02-10 09:54:20', 'Filha de comerciantes, conhece todos os mares.', 'Lysa Almar', 'Carismática e ambiciosa', 'Mercadora', NULL, 'Humana'),
(6, '2026-02-10 09:54:20', 'Ex-gladiador que fugiu para viver como mercenário.', 'Korvak', 'Agressivo e honrado', 'Mercenário', NULL, 'Orc'),
(7, '2026-02-10 09:54:20', 'Estudioso das eras antigas e dos mapas perdidos.', 'Thalion', 'Curioso e metódico', 'Historiador', NULL, 'Elfo'),
(8, '2026-02-10 09:54:20', 'Cresceu entre ladrões nos portos.', 'Mira Sombria', 'Sarcastica e observadora', 'Ladra', NULL, 'Humana'),
(9, '2026-02-10 09:54:20', 'Ex-escravo do deserto que se tornou líder de caravana.', 'Ruk', 'Protetor e firme', 'Caravaneiro', NULL, 'Meio-Orc'),
(10, '2026-02-10 09:54:20', 'Aprendiz de magia que busca conhecimento proibido.', 'Selene', 'Impulsiva e inteligente', 'Maga', NULL, 'Humana');

-- --------------------------------------------------------

--
-- Estrutura para tabela `parametros_ia`
--

CREATE TABLE `parametros_ia` (
  `id` int(11) NOT NULL,
  `hostilidade` int(11) DEFAULT NULL,
  `lealdade` int(11) DEFAULT NULL,
  `proximidade` int(11) DEFAULT NULL,
  `reputacao` int(11) DEFAULT NULL,
  `observacao` text DEFAULT NULL,
  `ultimo_evento` datetime NOT NULL DEFAULT current_timestamp(),
  `fk_npc_id` int(11) NOT NULL,
  `fk_avatar_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `parametros_ia`
--

INSERT INTO `parametros_ia` (`id`, `hostilidade`, `lealdade`, `proximidade`, `reputacao`, `observacao`, `ultimo_evento`, `fk_npc_id`, `fk_avatar_id`) VALUES
(1, 0, 0, 0, 0, 'A interacao foi neutra e breve. O jogador fez uma pergunta simples e o NPC respondeu de forma padrao, alinhada com seu papel de guardiao. Nao houve acao que alterasse os parametros emocionais.', '2026-02-10 14:53:52', 1, 2);

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuario`
--

CREATE TABLE `usuario` (
  `Id` int(11) NOT NULL,
  `criado_em` datetime DEFAULT current_timestamp(),
  `nome_usuario` varchar(30) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `logado` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuario`
--

INSERT INTO `usuario` (`Id`, `criado_em`, `nome_usuario`, `senha`, `logado`) VALUES
(1, '2026-02-10 09:28:08', 'teste', '46070d4bf934fb0d4b06d9e2c46e346944e322444900a435d7d9a95e6d7435f5', 0);

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `avatar`
--
ALTER TABLE `avatar`
  ADD PRIMARY KEY (`Id`),
  ADD UNIQUE KEY `nome` (`nome`),
  ADD KEY `fk_mapa_id` (`fk_mapa_id`);

--
-- Índices de tabela `contem`
--
ALTER TABLE `contem`
  ADD PRIMARY KEY (`fk_Avatar_Id`,`fk_Usuario_Id`),
  ADD KEY `FK_Contem_2` (`fk_Usuario_Id`);

--
-- Índices de tabela `contido`
--
ALTER TABLE `contido`
  ADD PRIMARY KEY (`fk_NPC_Id`,`fk_Mapas_Id`),
  ADD KEY `FK_Contido_2` (`fk_Mapas_Id`);

--
-- Índices de tabela `historico_chats`
--
ALTER TABLE `historico_chats`
  ADD PRIMARY KEY (`Id`);

--
-- Índices de tabela `historico_logon`
--
ALTER TABLE `historico_logon`
  ADD PRIMARY KEY (`id_historico_logon`),
  ADD KEY `FK_Historico_logon_1` (`usuario_id`);

--
-- Índices de tabela `interage_avatar_npc_historico_chats`
--
ALTER TABLE `interage_avatar_npc_historico_chats`
  ADD PRIMARY KEY (`fk_avatar_Id`,`fk_npc_Id`,`fk_historico_id`),
  ADD KEY `FK_Interage_2` (`fk_npc_Id`),
  ADD KEY `FK_Interage_3` (`fk_historico_id`);

--
-- Índices de tabela `localizado`
--
ALTER TABLE `localizado`
  ADD PRIMARY KEY (`fk_Historico_chats_Id`,`fk_Mapas_Id`),
  ADD KEY `FK_Localizado_2` (`fk_Mapas_Id`);

--
-- Índices de tabela `mapas`
--
ALTER TABLE `mapas`
  ADD PRIMARY KEY (`Id`),
  ADD UNIQUE KEY `nome` (`nome`);

--
-- Índices de tabela `npc`
--
ALTER TABLE `npc`
  ADD PRIMARY KEY (`Id`);

--
-- Índices de tabela `parametros_ia`
--
ALTER TABLE `parametros_ia`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `fk_npc_id` (`fk_npc_id`,`fk_avatar_id`),
  ADD KEY `FK_Parametros_ia_1` (`fk_avatar_id`);

--
-- Índices de tabela `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`Id`),
  ADD UNIQUE KEY `nome_usuario` (`nome_usuario`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `avatar`
--
ALTER TABLE `avatar`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `historico_chats`
--
ALTER TABLE `historico_chats`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `historico_logon`
--
ALTER TABLE `historico_logon`
  MODIFY `id_historico_logon` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de tabela `mapas`
--
ALTER TABLE `mapas`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `npc`
--
ALTER TABLE `npc`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de tabela `parametros_ia`
--
ALTER TABLE `parametros_ia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `usuario`
--
ALTER TABLE `usuario`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `avatar`
--
ALTER TABLE `avatar`
  ADD CONSTRAINT `fk_mapa_id` FOREIGN KEY (`fk_mapa_id`) REFERENCES `mapas` (`Id`);

--
-- Restrições para tabelas `contem`
--
ALTER TABLE `contem`
  ADD CONSTRAINT `FK_Contem_1` FOREIGN KEY (`fk_Avatar_Id`) REFERENCES `avatar` (`Id`),
  ADD CONSTRAINT `FK_Contem_2` FOREIGN KEY (`fk_Usuario_Id`) REFERENCES `usuario` (`Id`);

--
-- Restrições para tabelas `contido`
--
ALTER TABLE `contido`
  ADD CONSTRAINT `FK_Contido_1` FOREIGN KEY (`fk_NPC_Id`) REFERENCES `npc` (`Id`),
  ADD CONSTRAINT `FK_Contido_2` FOREIGN KEY (`fk_Mapas_Id`) REFERENCES `mapas` (`Id`);

--
-- Restrições para tabelas `historico_logon`
--
ALTER TABLE `historico_logon`
  ADD CONSTRAINT `FK_Historico_logon_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`Id`);

--
-- Restrições para tabelas `interage_avatar_npc_historico_chats`
--
ALTER TABLE `interage_avatar_npc_historico_chats`
  ADD CONSTRAINT `FK_Interage_1` FOREIGN KEY (`fk_avatar_Id`) REFERENCES `avatar` (`Id`),
  ADD CONSTRAINT `FK_Interage_2` FOREIGN KEY (`fk_npc_Id`) REFERENCES `npc` (`Id`),
  ADD CONSTRAINT `FK_Interage_3` FOREIGN KEY (`fk_historico_id`) REFERENCES `historico_chats` (`Id`);

--
-- Restrições para tabelas `localizado`
--
ALTER TABLE `localizado`
  ADD CONSTRAINT `FK_Localizado_1` FOREIGN KEY (`fk_Historico_chats_Id`) REFERENCES `historico_chats` (`Id`),
  ADD CONSTRAINT `FK_Localizado_2` FOREIGN KEY (`fk_Mapas_Id`) REFERENCES `mapas` (`Id`);

--
-- Restrições para tabelas `parametros_ia`
--
ALTER TABLE `parametros_ia`
  ADD CONSTRAINT `FK_Parametros_ia_1` FOREIGN KEY (`fk_avatar_id`) REFERENCES `avatar` (`Id`),
  ADD CONSTRAINT `FK_Parametros_ia_2` FOREIGN KEY (`fk_npc_id`) REFERENCES `npc` (`Id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
