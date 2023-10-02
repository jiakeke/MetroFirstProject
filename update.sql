# Please add all the modification to the database here.

drop table goal_reached;
drop table game;

create table user(
id int not null auto_increment,
name varchar(40),
password varchar(40),
primary key (id)
);

create table aircraft(
    id int not null auto_increment,
    name varchar(255) not null,
    passenger_capacity int not null,
    flight_range int not null,
    price int not null,
    carbon_emission int not null,
    PRIMARY KEY (id)
);

insert into aircraft (name, passenger_capacity, flight_range, price, carbon_emission) values ('Basic plane', 50, 500, 0, 1);
insert into aircraft (name, passenger_capacity, flight_range, price, carbon_emission) values ('Advanced plane', 100, 1000, 10000, 1);
insert into aircraft (name, passenger_capacity, flight_range, price, carbon_emission) values ('Eco plane', 60, 800, 7000, 1);
insert into aircraft (name, passenger_capacity, flight_range, price, carbon_emission) values ('Super plane', 150, 1500, 15000, 1);
insert into aircraft (name, passenger_capacity, flight_range, price, carbon_emission) values ('Ultimate plane', 200, 2000, 50000, 1);
insert into aircraft (name, passenger_capacity, flight_range, price, carbon_emission) values ('Turbo jet', 250, 3000, 60000, 1);
insert into aircraft (name, passenger_capacity, flight_range, price, carbon_emission) values ('Eco jet', 180, 2200, 55000, 1);
insert into aircraft (name, passenger_capacity, flight_range, price, carbon_emission) values ('Luxury liner', 300, 3500, 75000, 1);
insert into aircraft (name, passenger_capacity, flight_range, price, carbon_emission) values ('Cargo plane', 20, 1500, 20000, 1);
insert into aircraft (name, passenger_capacity, flight_range, price, carbon_emission) values ('Stealth jet', 100, 2500, 65000, 1);
