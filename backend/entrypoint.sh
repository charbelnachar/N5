#!/bin/bash

# Esperar a que la base de datos esté lista
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  echo >&2 "Postgres is unavailable - sleeping"
  sleep 1
done

echo >&2 "Postgres is up - executing command"

# Ejecutar migraciones
python manage.py migrate

# Crear usuario de la aplicación (si no existe)
python manage.py create_user admin "Admin" admin@example.com admin admin_identifier

# Ejecutar script SQL para insertar datos
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f /app/data.sql
# Ejecutar el servidor
python manage.py runserver