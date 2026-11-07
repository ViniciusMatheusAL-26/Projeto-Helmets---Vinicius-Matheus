DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS categoria;

CREATE TABLE categoria(
   id integer primary key autoincrement,
   nome varchar(50) not null,
   descricao text, 
   ativo boolean,
   imagem blob,
   img varchar(100)
);

CREATE TABLE produto(
   id integer primary key autoincrement,
   nome varchar(50) not null,
   preco float,
   descricao text,
   ativo boolean, 
   imagem blob,
   img varchar(100),
   id_categoria int,
   foreign key ('categoria_id') references categoria('id')
);

insert into categoria(nome, descricao, ativo)
values('Vodka','Orloff', 'True'),
      ('Coca Cola', 'Lata', 'True')      

