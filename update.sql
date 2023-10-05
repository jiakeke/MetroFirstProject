# Please add all the modification to the database here.

drop table goal_reached;
drop table game;
drop table goal;

create table user(
    id int not null auto_increment,
    name varchar(40),
    password varchar(40),
    status boolean default true,
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

create table user_aircraft(
    id int not null auto_increment,
    user_id int not null,
    aircraft_id int not null,
    primary key (id),
    foreign key (user_id) references user(id),
    foreign key (aircraft_id) references aircraft(id)
);

delete from aircraft
where name = 'Stealth jet';

alter table aircraft
modify column carbon_emission FLOAT;

update aircraft
set passenger_capacity = 10, flight_range = 500, price = 0, carbon_emission = 1.5
where name = 'Basic plane';

update aircraft
set name = 'SkyHawk100'
where passenger_capacity = 10;

update aircraft
set passenger_capacity = 20, flight_range = 700, price = 30, carbon_emission = 1.45
where name = 'Advanced plane';

update aircraft
set name = 'Phoenix Glide'
where passenger_capacity = 20;

update aircraft
set passenger_capacity = 30, flight_range = 1000, price = 100, carbon_emission = 1.4
where name = 'Eco plane';

update aircraft
set name = 'AeroWing X-200'
where passenger_capacity = 30;

update aircraft
set passenger_capacity = 50, flight_range = 1200, price = 200, carbon_emission = 1.3
where name = 'Super plane';

update aircraft
set name = 'StarStrider Zephyr'
where passenger_capacity = 50;

update aircraft
set passenger_capacity = 75, flight_range = 1500, price = 500, carbon_emission = 1.2
where name = 'Ultimate plane';

update aircraft
set name = 'SilverArrow 500'
where passenger_capacity = 75;

update aircraft
set passenger_capacity = 100, flight_range = 1800, price = 1000, carbon_emission = 1.1
where name = 'Turbo jet';

update aircraft
set name = 'Aurora Seraphim'
where passenger_capacity = 100;

update aircraft
set passenger_capacity = 150, flight_range = 2500, price = 1800, carbon_emission = 1.0
where name = 'Eco jet';

update aircraft
set name = 'Quantum Skystreamer'
where passenger_capacity = 150;

update aircraft
set passenger_capacity = 300, flight_range = 3500, price = 2500, carbon_emission = 0.9
where name = 'Luxury liner';

update aircraft
set name = 'Neptune Voyager'
where passenger_capacity = 300;

update aircraft
set name = 'Elysium Celestial', passenger_capacity = 500, flight_range = 5000, carbon_emission = 0.75
where price = 20000;

update aircraft
set price = 5000
where name = 'Elysium Celestial';






