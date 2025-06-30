-- Create DW schema
CREATE SCHEMA IF NOT EXISTS dw;

-- Departments dimension table
CREATE TABLE IF NOT EXISTS dw.dim_departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100),
    department_code VARCHAR(50),
    department_email VARCHAR(100),
    department_head VARCHAR(100),
    budget_currency VARCHAR(50),
    location VARCHAR(100),
    phone VARCHAR(20),
    manager VARCHAR(100),
    size INT,
    creation_date DATE,
    dw_create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(20) DEFAULT 'CSV'
);

-- People dimension table
CREATE TABLE IF NOT EXISTS dw.dim_people (
    person_id INT PRIMARY KEY,
    source_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    department VARCHAR(100),
    phone_number VARCHAR(20),
    gender VARCHAR(20),
    job_title VARCHAR(100),
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    start_time VARCHAR(20),
    end_time VARCHAR(20),
    manager_id INT,
    salary_currency VARCHAR(50),
    hire_date DATE,
    age INT,
    years_of_experience INT,
    dw_create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(20) DEFAULT 'CSV'
);

-- Sites dimension table
CREATE TABLE IF NOT EXISTS dw.dim_sites (
    site_id INT PRIMARY KEY,
    source_id VARCHAR(100),
    site_name VARCHAR(100),
    cid VARCHAR(100),
    manager VARCHAR(100),
    submanager VARCHAR(100),
    devteam VARCHAR(100),
    host BOOLEAN,
    lifetime INT,
    state VARCHAR(100),
    url TEXT,
    dw_create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ETL SQL to Move Data from Raw to DW Without Duplicates
-- Departments ETL
INSERT INTO dw.dim_departments (
    department_id, department_name, department_code, department_email,
    department_head, budget_currency, location, phone, manager, size,
    creation_date
)
SELECT
    id, name, code, email, head, budget, location, phone, manager, size,
    TO_DATE(creation_date, 'MM/DD/YYYY')
FROM raw.departments
WHERE id NOT IN (SELECT department_id FROM dw.dim_departments);

-- People ETL
INSERT INTO dw.dim_people (
    person_id, source_id, first_name, last_name, email, department,
    phone_number, gender, job_title, address, city, state, country,
    postal_code, start_time, end_time, manager_id, salary_currency,
    hire_date, age, years_of_experience
)
SELECT
    id, source_id, first_name, last_name, email, department,
    phone_number, gender, job_title, address, city, state, country,
    postal_code, start_time, end_time, manager_id, salary,  -- Changed from salary_currency to salary
    TO_DATE(hire_date, 'MM/DD/YYYY'), age, years_of_experience
FROM raw.people
WHERE id NOT IN (SELECT person_id FROM dw.dim_people);

-- Sites ETL
INSERT INTO dw.dim_sites (
    site_id, source_id, site_name, cid, manager, submanager,
    devteam, host, lifetime, state, url
)
SELECT
    id, source_id, name, cid, manager, submanager,
    devteam, host, lifetime, state, url
FROM raw.sites
WHERE id NOT IN (SELECT site_id FROM dw.dim_sites);