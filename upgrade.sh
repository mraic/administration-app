#!/bin/bash
docker container exec -it administration_app_development bash -c "flask db upgrade"
