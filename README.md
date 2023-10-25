## MS-LEADS

### Descargar el repo
git clone https://github.com/fgplastina/ms-leads.git

### Buildear la imagen
docker-compose up 

### Cargar data inicial
docker-compose exec -T leads-postgresql psql -U postgres -d leads-db < load_data.sql