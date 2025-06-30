CREATE SCHEMA IF NOT EXISTS raw;

DROP TABLE IF EXISTS raw.sites;

CREATE TABLE IF NOT EXISTS raw.sites
(
    id           SERIAL,
    source_id    varchar(50)  DEFAULT NULL,
    name         varchar(200) DEFAULT NULL,
    cid          varchar(26)  DEFAULT NULL,
    manager      varchar(36)  DEFAULT NULL,
    submanager   varchar(36)  DEFAULT NULL,
    devteam      varchar(100) DEFAULT NULL,
    host         boolean,
    lifetime     INTEGER,
    state        varchar(100) DEFAULT NULL,
    url          TEXT         DEFAULT NULL,
    date_created timestamp    default current_timestamp,
    date_updated timestamp,
    PRIMARY KEY (id)
);

CREATE OR REPLACE FUNCTION update_site_date_updated_column()
    RETURNS TRIGGER AS
$$
BEGIN
    NEW.date_updated = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE OR REPLACE TRIGGER update_sites_modtime
    BEFORE UPDATE
    ON raw.sites
    FOR EACH ROW
EXECUTE PROCEDURE update_site_date_updated_column();