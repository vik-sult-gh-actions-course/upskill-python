-- Create dw schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS dw;

-- Function to move data from raw to dw for a given table
CREATE OR REPLACE FUNCTION move_to_dw(raw_table_name text) RETURNS void AS $$
DECLARE
    dw_table_exists boolean;
    column_list text;
    pk_columns text;
    join_conditions text;
    pk_info record;
BEGIN
    -- Check if dw table exists, if not create it
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'dw' AND table_name = raw_table_name
    ) INTO dw_table_exists;

    IF NOT dw_table_exists THEN
        -- Create dw table with same structure as raw table plus dw_create_date
        EXECUTE format('
            CREATE TABLE dw.%I AS
            SELECT *, NULL::timestamp AS dw_create_date
            FROM raw.%I
            WHERE 1=0',
            raw_table_name, raw_table_name);

        -- Add primary key if exists in raw table
        SELECT string_agg(column_name, ', ') INTO pk_columns
        FROM information_schema.key_column_usage
        WHERE table_schema = 'raw'
          AND table_name = raw_table_name
          AND constraint_name LIKE '%pkey%';

        IF pk_columns IS NOT NULL THEN
            EXECUTE format('ALTER TABLE dw.%I ADD PRIMARY KEY (%s)', raw_table_name, pk_columns);
        END IF;
    END IF;

    -- Get all columns except raw_create_date and dw_create_date for insert
    SELECT string_agg(column_name, ', ') INTO column_list
    FROM information_schema.columns
    WHERE table_schema = 'raw'
      AND table_name = raw_table_name
      AND column_name NOT IN ('raw_create_date', 'dw_create_date');

    -- Get primary key columns for duplicate check
    SELECT string_agg('r.' || column_name || ' = d.' || column_name, ' AND ') INTO join_conditions
    FROM information_schema.key_column_usage
    WHERE table_schema = 'raw'
      AND table_name = raw_table_name
      AND constraint_name LIKE '%pkey%';

    -- If no primary key, use all columns for comparison
    IF join_conditions IS NULL THEN
        SELECT string_agg('r.' || column_name || ' = d.' || column_name, ' AND ') INTO join_conditions
        FROM information_schema.columns
        WHERE table_schema = 'raw'
          AND table_name = raw_table_name
          AND column_name NOT IN ('raw_create_date', 'dw_create_date');
    END IF;

    -- Insert new records and update dw_create_date for existing ones
    EXECUTE format('
        WITH new_data AS (
            SELECT %s
            FROM raw.%I r
            WHERE NOT EXISTS (
                SELECT 1 FROM dw.%I d
                WHERE %s
            )
        )
        INSERT INTO dw.%I (%s, dw_create_date)
        SELECT %s, NOW() FROM new_data;

        UPDATE dw.%I d
        SET dw_create_date = NOW()
        FROM raw.%I r
        WHERE %s AND d.dw_create_date IS NULL;
    ',
    column_list, raw_table_name, raw_table_name, join_conditions,
    raw_table_name, column_list, column_list,
    raw_table_name, raw_table_name, join_conditions);

    RAISE NOTICE 'Moved data from raw.% to dw.%', raw_table_name, raw_table_name;
END;
$$ LANGUAGE plpgsql;

-- Procedure to move all tables from raw to dw
CREATE OR REPLACE PROCEDURE move_all_to_dw()
AS $$
DECLARE
    table_record record;
BEGIN
    FOR table_record IN
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'raw'
    LOOP
        PERFORM move_to_dw(table_record.table_name);
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Execute the procedure to move all tables
CALL move_all_to_dw();