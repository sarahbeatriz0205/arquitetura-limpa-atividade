CREATE TABLE IF NOT EXISTS Trabalho(
    id integer PRIMARY KEY AUTOINCREMENT,
    titulo varchar(150) NOT NULL,
    descricao text NOT NULL,
    orcamento varchar(50) NOT NULL,
    status integer NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Servico(
    trabalho_id integer PRIMARY KEY,
    metodologia varchar(200) NOT NULL,
    ferramenta varchar(200) NOT NULL,
    FOREIGN KEY(trabalho_id) REFERENCES Trabalho(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Demanda(
    trabalho_id integer PRIMARY KEY,
    exigencias text NOT NULL,
    prazo varchar(50) NOT NULL,
    FOREIGN KEY(trabalho_id) REFERENCES Trabalho(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Proposta(
    id integer PRIMARY KEY AUTOINCREMENT,
    orcamento varchar(50) NOT NULL,
    apresentacao text NOT NULL,
    prazo varchar(50) NOT NULL,
    exigencia text NOT NULL,
    tipo integer NOT NULL,
    status integer NOT NULL DEFAULT 1
);
