CREATE TABLE Usuario (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    nome_usuario VARCHAR(30) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    logado BOOLEAN DEFAULT FALSE,
    UNIQUE (nome_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Avatar (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Mapas (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    epoca VARCHAR(100),
    descricao TEXT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    UNIQUE (nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE NPC (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    historia_pessoal TEXT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    personalidade VARCHAR(100),
    profissao VARCHAR(20),
    atualizado_em DATETIME,
    raca VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Historico_chats (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    menssagem_usuario TEXT NOT NULL,
    resposta_ai TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Contem (
    fk_Avatar_Id INT NOT NULL,
    fk_Usuario_Id INT NOT NULL,
    PRIMARY KEY (fk_Avatar_Id, fk_Usuario_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Contido (
    fk_NPC_Id INT NOT NULL,
    fk_Mapas_Id INT NOT NULL,
    PRIMARY KEY (fk_NPC_Id, fk_Mapas_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Localizado (
    fk_Historico_chats_Id INT NOT NULL,
    fk_Mapas_Id INT NOT NULL,
    PRIMARY KEY (fk_Historico_chats_Id, fk_Mapas_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Interage_Avatar_NPC_Historico_chats (
    fk_Avatar_Id INT NOT NULL,
    fk_NPC_Id INT NOT NULL,
    fk_Historico_chats_Id INT NOT NULL,
    data_interacao DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (fk_Avatar_Id, fk_NPC_Id, fk_Historico_chats_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Parametros_ia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hostilidade INT,
    lealdade INT,
    proximidade INT,
    reputacao INT,
    observacao TEXT,
    ultimo_evento DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fk_npc_id INT NOT NULL,
    fk_avatar_id INT NOT NULL,
    UNIQUE (fk_npc_id, fk_avatar_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Historico_logon (
    id_historico_logon INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    data_login DATETIME NOT NULL,
    data_logout DATETIME NULL,
    ip VARCHAR(45),
    dispositivo VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE Contem
    ADD CONSTRAINT FK_Contem_1 FOREIGN KEY (fk_Avatar_Id) REFERENCES Avatar (Id),
    ADD CONSTRAINT FK_Contem_2 FOREIGN KEY (fk_Usuario_Id) REFERENCES Usuario (Id);

ALTER TABLE Contido
    ADD CONSTRAINT FK_Contido_1 FOREIGN KEY (fk_NPC_Id) REFERENCES NPC (Id),
    ADD CONSTRAINT FK_Contido_2 FOREIGN KEY (fk_Mapas_Id) REFERENCES Mapas (Id);

ALTER TABLE Localizado
    ADD CONSTRAINT FK_Localizado_1 FOREIGN KEY (fk_Historico_chats_Id) REFERENCES Historico_chats (Id),
    ADD CONSTRAINT FK_Localizado_2 FOREIGN KEY (fk_Mapas_Id) REFERENCES Mapas (Id);

ALTER TABLE Interage_Avatar_NPC_Historico_chats
    ADD CONSTRAINT FK_Interage_1 FOREIGN KEY (fk_Avatar_Id) REFERENCES Avatar (Id),
    ADD CONSTRAINT FK_Interage_2 FOREIGN KEY (fk_NPC_Id) REFERENCES NPC (Id),
    ADD CONSTRAINT FK_Interage_3 FOREIGN KEY (fk_Historico_chats_Id) REFERENCES Historico_chats (Id);

ALTER TABLE Parametros_ia
    ADD CONSTRAINT FK_Parametros_ia_1 FOREIGN KEY (fk_avatar_id) REFERENCES Avatar (Id),
    ADD CONSTRAINT FK_Parametros_ia_2 FOREIGN KEY (fk_npc_id) REFERENCES NPC (Id);

ALTER TABLE Historico_logon
    ADD CONSTRAINT FK_Historico_logon_1 FOREIGN KEY (usuario_id) REFERENCES Usuario (Id);
