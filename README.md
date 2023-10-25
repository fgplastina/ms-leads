## MS-LEADS

##### Descargar el repo
```bash
git clone https://github.com/fgplastina/ms-leads.git
```

##### Buildear la imagen
```bash
docker-compose up --build
```
Opcional para usar detach
```bash
docker-compose up --build -d
```

##### Cargar data inicial
```bash
docker-compose exec -T leads-postgresql psql -U postgres -d leads-db < load_data.sql
```

##### Attachear el contenedor de FastAPI
```bash
docker attach leads-fastapi
```

#### API docs
http://localhost:8000/docs

#### Frontend
http://localhost:3000


