create table Locais(
    ID int auto_increment,
    Nome varchar(50) not null,
    Endereco varchar(100) not null,
    primary key (ID)
);

create table Itens(
    ID int auto_increment,
    Nome varchar(50) not null,
    primary key (ID)
);

create table Inventario(
    ID int auto_increment,
    LocalID int,
    ItemID int,
    Qnt int,
    UltimoMov date,
    primary key (ID),
    foreign key (LocalID) references Locais(ID) on delete no action on update cascade,
    foreign key (ItemID) references Itens(ID) on delete no action on update cascade
);

create table Log(
    ID int auto_increment,
    LocalID int,
    ItemID int,
    Delta int,
    Quando datetime,
    primary key (ID),
    foreign key (LocalID) references Locais(ID) on delete no action on update cascade
);