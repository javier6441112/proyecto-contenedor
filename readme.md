

Descripcion
Aplicación web que permite registrar y consultar puntos de interés geográficos utilizando una base de datos con capacidades espaciales.

Permite:
- Registrar nuevos puntos
- Consultar todos los puntos
- Buscar puntos cercanos por coordenadas
- consultar por categoria

arquitectura

Cliente (Navegador)
↓
Nginx (Proxy)
↓
FastAPI (Backend)
↓
PostgreSQL + PostGIS (Base de datos)

tecnologias utilizadas

- Backend: FastAPI (Python)
- Base de datos: PostgreSQL + PostGIS
- Proxy: Nginx
- Contenedores: Docker + Docker Compose

como ejecutar el proyecto 

en la carpeta en donde se desee guardar el proyecto ejecutar los siguientes comandos

git clone https://github.com/javier6441112/proyecto-contenedor.git
1. cd proyecto-contenedo/proyecto-poi
2. levantar los contenedores con el comando 
    docker compose up --build  
3. en el navegador ir  la direccion http://localhost:80
