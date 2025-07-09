CREATE SCHEMA IF NOT EXISTS dw;

DO
$$
    DECLARE
        tbl          RECORD;
        where_clause TEXT;
    BEGIN
        FOR tbl IN SELECT table_name FROM information_schema.tables WHERE table_schema = 'raw'
            LOOP
                EXECUTE format('ALTER TABLE raw.%I SET SCHEMA dw;', tbl.table_name);

                SELECT string_agg(format('a.%1$I = b.%1$I', column_name), ' AND ')
                INTO where_clause
                FROM information_schema.columns
                WHERE table_schema = 'dw'
                  AND table_name = tbl.table_name
                  AND column_name NOT IN ('id', 'raw_create_date');

                EXECUTE format(
                        'DELETE FROM dw.%I a USING dw.%I b WHERE a.id > b.id AND %s;',
                        tbl.table_name, tbl.table_name, where_clause
                        );

                EXECUTE format(
                        'ALTER TABLE dw.%I ADD COLUMN IF NOT EXISTS dw_create_date timestamp;',
                        tbl.table_name
                        );
                EXECUTE format(
                        'UPDATE dw.%I SET dw_create_date = now();',
                        tbl.table_name
                        );
            END LOOP;
    END
$$;