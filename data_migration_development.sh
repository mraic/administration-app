#!/bin/bash
docker exec -it administracija_app_development bash -c "flask db_dev_recreate"
docker exec -it administracija_app_development bash -c "flask db_dev create_postgis_extension"
docker exec -it administracija_app_development bash -c "flask db upgrade"