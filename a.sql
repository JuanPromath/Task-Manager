CREATE database TK;
USE TK;

CREATE TABLE ciclo(
	codigo INTEGER primary key auto_increment,
    nome text,
	tempoTotal TIME,
    tempoTotalDecimal real
);

CREATE TABLE atividade(
	codigo INTEGER primary key auto_increment,
    nome text
);

CREATE TABLE ciclo_atividade(
	codigo INTEGER primary key auto_increment,
    codigoAtividade integer not null,
    codigoCiclo integer not null,
    gp text,
    porcentagemTempoTotal real,
    foreign key (codigoAtividade) references atividade(codigo),
    foreign key (codigoCiclo) references ciclo(codigo)
);

CREATE TABLE sessao(

	codigo INTEGER PRIMARY KEY auto_increment,
	codigoCiclo integer,
    nome text,
    nome_ciclo text,
    foreign key (codigoCiclo) references ciclo(codigo)
    
);

ALTER TABLE sessao add column status text not null;
ALTER TABLE sessao add column inicioData date not null;
ALTER TABLE sessao add column fimData date;
ALTER TABLE sessao add column ultimaSessao integer;
ALTER TABLE sessao add constraint fk_lastSession foreign key (ultimaSessao) references sessao(codigo);
select * from sessao;

CREATE TABLE sessao_atividade(
	codigo integer primary key auto_increment,
	nomeAtividade text,
	codigoAtividade integer,
    codigoSessao integer
);

CREATE TABLE registro(
	codigo integer PRIMARY KEY auto_increment,
    codigoSessaoAtividade integer,
    inicio TIME,
    fim TIME,
    data DATE,
    nomeAtividade text,
	tempoAFazer time,
    tempoAFazerD real,
    codigoRA integer,
    codigoRAnd integer
);

ALTER TABLE registro
add constraint sessaoAtividade_fk 
foreign key (codigoSessaoAtividade) references sessao_Atividade(codigo);
ALTER TABLE registro
ADD CONSTRAINT codigoRA_fk 
foreign key (codigoRA) REFERENCES registro(codigo),
ADD constraint codigoRAnd_fk
foreign key(codigoRAnd) REFERENCES registro(codigo);

ALTER TABLE sessao_atividade
ADD CONSTRAINT atividade_fk
FOREIGN KEY (codigoAtividade) REFERENCES atividade(codigo);
ALTER TABLE sessao_atividadecodigo
ADD CONSTRAINT codigoSessao_fk
FOREIGN KEY (codigoSessao) REFERENCES sessao(codigo);
ALTER TABLE sessao add column tempoTotal time;
ALTER TABLE sessao add column tempoTotalDecimal real;
ALTER TABLE sessao ADD COLUMN filled text;

SELECT * from sessao_Atividade;
select * from registro;

ALTER TABLE sessao_Atividade add column tempoAFazer time;
ALTER TABLE sessao_Atividade add column tempoAFazerdecimal real;
alter table sessao_Atividade add column porcentagemTempoTotal real;
alter table sessao_Atividade add column ultimoRegistro integer;
ALTER TABLE sessao_Atividade add constraint last_register foreign key (ultimoRegistro) REFERENCES registro(codigo);
ALTER TABLE sessao_Atividade add column gp text;

SELECT * FROM ciclo_atividade where codigoCiclo=4;

insert into ciclo(nome, tempoTotal, tempoTotalDecimal) VALUES ('faculdade', '09:59:32', 9.9923);
insert into atividade(nome) VALUES ('Banco de dados'),('logica e programação'),('projeto TK');
insert into ciclo_atividade(codigoAtividade, codigoCiclo, gp, porcentagemTempoTotal) VALUES (3, 4, 'facul',0.25),
(5, 4, 'facul',0.25)
,(6, 4, 'facul',0.25),
(7, 4, 'facul',0.25);

SELECT * FROM ciclo_atividade INNER JOIN ciclo on codigoCiclo = ciclo.codigo;
SELECT * FROM sessao where status='finalizada' and codigoCiclo=4 order by fimData desc;

SELECT ciclo_atividade.codigo, codigoAtividade, atividade.nome, gp, porcentagemTempoTotal FROM ciclo_atividade INNER JOIN atividade on codigoAtividade=atividade.codigo where codigoCiclo=4;
select * from sessao_atividade;
select * from sessao;
select * from registro;

UPDATE sessao_atividade set ultimoRegistro = null;
update registro set codigoSessaoAtividade = null,  codigoRA = null;

DELETE FROM sessao where codigo=20;
DELETE FROM sessao_atividade where codigoSessao=20;
DELETE FROM registro;
DELETE FROM ciclo_atividade;
DELETE FROM ciclo;
DELETE from atividade where codigo IN (3, 4, 5, 6, 7);
SELECT codigo FROM registro where codigoSessaoAtividade = 15 order by data desc, inicio desc limit 1;

select * from registro where codigoSessaoAtividade = 13 order by data desc, inicio desc;

SELECT * FROM atividade;
select sum(porcentagemTempoTotal) from ciclo_atividade;
SELECT * FROM ciclo;

SELECT * FROM sessao;
SELECT * FROM sessao_atividade;
SELECT * FROM registro;

SELECT sum(tempoAFazer), sum(tempoAFazerdecimal) FROM sessao_atividade;
SELECT * FROM sessao where status='finalizada' and codigoCiclo=5 order by fimData desc limit 0;
update sessao set status = 'pausada' where codigo=15;

UPDATE sessao_atividade set tempoAFazerdecimal=0, tempoAFazer='00:00:00' where codigo= 24;

INSERT INTO registro(codigoSessaoAtividade, inicio, fim, data, nomeAtividade, tempoAFazer, tempoAFazerD) VALUES
(24, '16:33:09', '17:03:49', '2026-02-19', 'violão', '00:00:00', 0.0);
SELECT * FROM sessao_atividade;
SELECT count(*), codigo from sessao_atividade where codigoSessao in (16,20) group by codigoAtividade having count(*) > 1;

SELECT * FROM sessao_atividade inner join registro on registro.codigo = ultimoRegistro where codigoSessao = 16 and codigoAtividade=8;
SELECT * FROM sessao_atividade inner join registro on registro.codigo = ultimoRegistro where codigoSessao = 16 and codigoAtividade=8;