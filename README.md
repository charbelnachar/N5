
# Proyecto N5

Este proyecto es una aplicación web que utiliza Django para el backend y React para el frontend. Está containerizado utilizando Docker y puede ser orquestado con Docker Compose. La aplicación viene con datos precargados y un usuario administrador con las credenciales `admin` / `admin` para acceder al sistema.

## Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Ejecución de las Migraciones](#ejecución-de-las-migraciones)
- [Creación de un Superusuario](#creación-de-un-superusuario)
- [Acceso al Panel de Administración de Django](#acceso-al-panel-de-administración-de-django)
- [Creación del Primer Oficial](#creación-del-primer-oficial)
- [Rutas de la API](#rutas-de-la-api)
- [Posibles Errores de la API](#posibles-errores-de-la-api)
- [Ver los Logs de la Aplicación](#ver-los-logs-de-la-aplicación)
- [Ejecutar Pruebas](#ejecutar-pruebas)
- [Estructura del Proyecto](#estructura-del-proyecto)

## Requisitos Previos

Asegúrate de tener instalados los siguientes componentes en tu máquina de desarrollo:

- Docker
- Docker Compose

## Instalación

1. Clona el repositorio:

   ```sh
   git clone git@github.com:charbelnachar/N5.git
   cd N5
   ```

2. Crea un archivo `.env` en el directorio raíz del proyecto y configura las variables de entorno necesarias. Puedes usar el siguiente contenido como plantilla para tu archivo `.env`:

   ```env
   DB_NAME=your-database-name
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_HOST=db
   DB_PORT=5432
   ```

3. Construye y levanta los contenedores usando Docker Compose:

   ```sh
   docker-compose up --build
   ```

## Uso

Una vez que los contenedores estén en funcionamiento, puedes acceder a la aplicación:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

## Ejecución de las Migraciones

Para crear las tablas en la base de datos y cargar los datos iniciales, debes ejecutar las migraciones. Puedes hacerlo con el siguiente comando:

   ```sh
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py loaddata initial_data.json
   ```

## Creación de un Superusuario

Para poder acceder al panel de administración de Django, debes crear un superusuario. Puedes hacerlo con el siguiente comando:

   ```sh
   docker-compose exec backend python manage.py createsuperuser
   ```

Sigue las instrucciones en la línea de comandos para crear el superusuario.

## Acceso al Panel de Administración de Django

Una vez que hayas creado un superusuario, puedes acceder al panel de administración de Django en `http://localhost:8000/admin/`. Utiliza el nombre de usuario y la contraseña del superusuario que creaste para iniciar sesión.

## Creación del Primer Oficial

El proyecto incluye un comando personalizado para crear el primer usuario oficial. Este comando facilita la creación de un oficial con los detalles necesarios. Para ejecutar este comando, sigue estos pasos:

1. Asegúrate de que los contenedores estén en funcionamiento.
2. Ejecuta el siguiente comando:

   ```sh
   docker-compose exec backend python manage.py create_officer --username your-username --email your-email --identifier your-identifier --password your-password --name your-name
   ```

   Reemplaza `your-username`, `your-email`, `your-identifier`, `your-password`, y `your-name` con los detalles correspondientes para el nuevo oficial.

## Rutas de la API

Este proyecto incluye las siguientes rutas de API:

- `/api/token/`: Obtiene un par de tokens de acceso y refresco.
- `/api/token/refresh/`: Refresca el token de acceso.
- `/person_by_email/<str:email>/`: Obtiene los detalles de una persona por su correo electrónico.
- `/person/<int:identifier>/`: Obtiene, actualiza o elimina los detalles de una persona específica por su identificador.
- `/person/`: Crea una nueva persona.
- `/all_person/`: Obtiene los detalles de todas las personas.
- `/all_officer/`: Obtiene todos los oficiales.
- `/officer/`: Crea un nuevo oficial.
- `/officer/<str:identifier>/`: Obtiene, actualiza o elimina un oficial específico por su identificador.
- `/vehicle/`: Crea un nuevo vehículo.

## Posibles Errores de la API

La API puede devolver los siguientes códigos de error:

- **200 OK**: La solicitud se procesó correctamente.
- **400 Bad Request**: La solicitud tiene un formato incorrecto o falta algún parámetro necesario.
- **401 Unauthorized**: La autenticación falló o el token es inválido.
- **403 Forbidden**: El usuario no tiene permisos para realizar esta acción.
- **404 Not Found**: No se encontró el recurso solicitado.
- **500 Internal Server Error**: Ocurrió un error inesperado en el servidor.

## Ver los Logs de la Aplicación

Para ver los logs de la aplicación en el backend, puedes acceder a los archivos de log que se encuentran en el directorio `backend/logs/`. También puedes ver los logs en tiempo real utilizando el siguiente comando:

   ```sh
   docker-compose logs -f backend
   ```

## Ejecutar Pruebas

Para ejecutar pruebas para el backend, ejecuta el siguiente comando dentro del contenedor del backend:

   ```sh
   docker-compose exec backend python manage.py test
   ```

## Estructura del Proyecto

```
N5/
├── backend/
│   ├── Dockerfile
│   ├── manage.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   ├── production.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   ├── models.py
│   │   ├── src/
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── logic/
│   │   │   │   ├── officer_logic.py
│   │   ├── migrations/
│   │   ├── management/
│   │   │   ├── commands/
│   │   │   │   ├── my_custom_command.py
│   ├── logs/
│   ├── tests/
│   │   ├── test_officer_logic.py
│   ├── requirements.txt
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
├── .dockerignore
├── .env
├── docker-compose.yml
└── README.md
```
```