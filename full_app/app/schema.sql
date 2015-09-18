drop table if exists ip_logger;
    create table ip_logger (
    id integer primary key autoincrement,
    ip_address text not null,
    timestamp text not null
);

drop table if exists phone_number_logger;
    create table phone_number_logger(
    id integer primary key autoincrement,
    phone_number text not null,
    timestamp text not null
);

drop table if exists address_logger;
    create table address_logger(
    id integer primary key autoincrement,
    address text not null,
    timestamp text not null
);


