#!/bin/bash
wget -O app/static/js/htmx.js https://raw.githubusercontent.com/bigskysoftware/htmx/master/src/htmx.js
echo "Run migrations"
alembic upgrade head

echo "Create initial data in DB"
python -m app.initial_data
