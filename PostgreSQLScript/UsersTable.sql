DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    id              SERIAL,
    email           varchar(200) DEFAULT NULL,
    username        varchar(45)  DEFAULT NULL,
    first_name      varchar(45)  DEFAULT NULL,
    last_name       varchar(45)  DEFAULT NULL,
    hashed_password varchar(200) DEFAULT NULL,
    is_active       boolean      DEFAULT NULL,
    role            varchar(45)  DEFAULT NULL,
    PRIMARY KEY (id)
);