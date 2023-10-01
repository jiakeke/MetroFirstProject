# Please add all the modification to the database here.

drop table goal_reached;
drop table game;

create table user(
ID int not null auto_increment,
name varchar(40),
password varchar(40),
primary key (id)
);