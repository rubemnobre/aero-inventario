create table Locais(
    ID int auto_increment,
    Nome varchar(50) not null,
    Endereco varchar(100) not null,
    primary key (ID)
);

create table Itens(
    ID int auto_increment,
    Nome varchar(50) not null,
    UltimoMov date,
    LocalID int,
    primary key (ID),
    foreign key (LocalID) references Locais(ID) on delete no action on update cascade
);