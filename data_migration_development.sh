#!/bin/bash
docker exec -it administration_app_development bash -c "flask db_dev recreate"
docker exec -it administration_app_development bash -c "flask db_dev create_postgis_extension"
docker exec -it administration_app_development bash -c "flask db upgrade"
docker exec -it administration_app_development bash -c "flask db_migrations regular_data"
docker exec -it administration_app_development bash -c "flask db_migrations fake_data"