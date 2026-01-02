FROM postgres:16

# Scripts de inicialización
COPY sql/*.sql /docker-entrypoint-initdb.d/
