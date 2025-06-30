CREATE SCHEMA IF NOT EXISTS raw;

-- departments
DROP TABLE IF EXISTS raw.departments;

CREATE TABLE IF NOT EXISTS raw.departments
(
    id            SERIAL,
    name          varchar(50)        DEFAULT NULL,
    code          varchar(200)       DEFAULT NULL,
    email         varchar(50) UNIQUE DEFAULT NULL,
    head          varchar(200)       DEFAULT NULL,
    budget        varchar(20)        DEFAULT NULL,
    location      varchar(50)        DEFAULT NULL,
    phone         varchar(20)        DEFAULT NULL,
    manager       varchar(50)        DEFAULT NULL,
    size          INTEGER,
    creation_date varchar(10)        DEFAULT NULL,
    date_created  timestamp          default current_timestamp,
    date_updated  timestamp,
    PRIMARY KEY (id)
);

CREATE OR REPLACE FUNCTION update_department_date_updated_column()
    RETURNS TRIGGER AS
$$
BEGIN
    NEW.date_updated = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE OR REPLACE TRIGGER update_department_modtime
    BEFORE UPDATE
    ON raw.departments
    FOR EACH ROW
EXECUTE PROCEDURE update_department_date_updated_column();


-- people
DROP TABLE IF EXISTS raw.people;
CREATE TABLE IF NOT EXISTS raw.people
(
    id                  SERIAL,
    source_id           integer,
    first_name          varchar(50) DEFAULT NULL,
    last_name           varchar(50) DEFAULT NULL,
    email               varchar(50) DEFAULT NULL,
    department          varchar(50) DEFAULT NULL,
    phone_number        varchar(20) DEFAULT NULL,
    gender              varchar(50) DEFAULT NULL,
    job_title           varchar(50) DEFAULT NULL,
    address             varchar(50) DEFAULT NULL,
    city                varchar(50) DEFAULT NULL,
    state               varchar(50) DEFAULT NULL,
    country             varchar(50) DEFAULT NULL,
    postal_code         varchar(50) DEFAULT NULL,
    start_time          varchar(50) DEFAULT NULL,
    end_time            varchar(50) DEFAULT NULL,
    manager_id          integer,
    salary              varchar(20) DEFAULT NULL,
    hire_date           varchar(20) DEFAULT NULL,
    age                 integer,
    years_of_experience integer,
    date_created        timestamp   default current_timestamp,
    date_updated        timestamp,
    PRIMARY KEY (id)
);

CREATE OR REPLACE FUNCTION update_department_people_date_updated_column()
    RETURNS TRIGGER AS
$$
BEGIN
    NEW.date_updated = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE OR REPLACE TRIGGER update_department_people_modtime
    BEFORE UPDATE
    ON raw.people
    FOR EACH ROW
EXECUTE PROCEDURE update_department_people_date_updated_column();