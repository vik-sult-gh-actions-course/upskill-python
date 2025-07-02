## How to run the Dockerfile locally

```
docker compose up --build --force-recreate --no-deps
```

Application available under URL http://localhost:5007/docs

python3 -m venv fastapienv
source fastapienv/bin/activate

pip install -r requirements.txt

### SQLAlchemy

1. Enter source virtual environment ```fastapienv/bin/activate```
2. Run pgsql script ```PostgreSQLScript/UsersTable.sql``` to create db schema and db table
3. Run python script python ```python SQLAlchemy/app.py```

# SitesAPI

SitesAPI is available locally under URL http://localhost:8000/docs#/sites

### Populate table with SitesAPI data

1. Enter source virtual environment ```fastapienv/bin/activate```
2. Run pgsql script ```PostgreSQLScript/SitesApi.sql``` to create db schema and db table
3. Run python script python ```SitesAPI/collect_sites.py```

# SFTPApi

### Sync department data via SFTPApi data

1. Enter source virtual environment ```fastapienv/bin/activate```
2. Run pgsql script ```SFTPApi/SFTPApi.sql``` to create db schema and db table
3. Run python script python ```python SFTPApi/sync_data.py```


# Pytest
1. Enter source virtual environment ```fastapienv/bin/activate```
2. Run command ```pytest app -W ignore::DeprecationWarning```

   
