DROP DATABASE IF EXISTS souldiaryconnect;
CREATE DATABASE souldiaryconnect;
\c souldiaryconnect;

DROP TABLE IF EXISTS medico;

CREATE TABLE medico (
    codice_identificativo varchar(12) PRIMARY KEY,
    nome varchar(30) NOT NULL,
    cognome varchar(30) NOT NULL,
    indirizzo_studio varchar(30) NOT NULL,
    citta varchar(30) NOT NULL,
    numero_civico varchar(6) NOT NULL,
    numero_telefono_studio varchar(13) UNIQUE,
    numero_telefono_cellulare varchar(13) UNIQUE,
    email varchar(50) UNIQUE NOT NULL,
    password varchar(50) NOT NULL,
    passwd varchar(50) NOT NULL
);

DROP TABLE IF EXISTS paziente;

CREATE TABLE paziente (
    codice_fiscale char(16) PRIMARY KEY,
    nome varchar(30) NOT NULL,
    cognome varchar(30) NOT NULL,
    data_di_nascita DATE NOT NULL,
    email varchar(50) UNIQUE NOT NULL,
    password varchar(50) NOT NULL,
    med varchar(12) NOT NULL,

    FOREIGN KEY (med) REFERENCES medico(codice_identificativo)
        ON UPDATE CASCADE ON DELETE CASCADE
);


DROP TABLE IF EXISTS nota_diario;

CREATE TABLE nota_diario (
    id serial PRIMARY KEY,
    paz char(16) NOT NULL,
    testo_paziente varchar(1000) NOT NULL,
    testo_supporto varchar(1000),
    testo_clico varchar(1000) NOT NULL,
    testo_medico varchar(1000),
    data_nota date NOT NULL,

    FOREIGN KEY (paz) REFERENCES paziente(codice_fiscale)
        ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TABLE IF EXISTS messaggio;

CREATE TABLE messaggio (
    id serial PRIMARY KEY,
    med varchar(12) NOT NULL,
    paz char(16) NOT NULL,
    testo varchar(1000) NOT NULL,
    data_messaggio date NOT NULL,
    mittente varchar(12) NOT NULL,

    FOREIGN KEY (paz) REFERENCES paziente(codice_fiscale)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (med) REFERENCES medico(codice_identificativo)
        ON UPDATE CASCADE ON DELETE CASCADE
);
