# sgil-proveedores-service
Sistema de Gestión Integral de Logística y Comercio (SGIL) , backend service


### Crear y activar el entorno virtual
```
make venv
```

### Instalar dependencias

```
make install
```

### Ejecutar el proyecto desde el folder raiz `sgil-proveedores-service`
```
make run
```

### Ejecutar pruebas
```
make test
```

### Formatear el codigo con Black
```
make format
```

### Revisar errores de linting con Flake8:
```
make lint
```

### Eliminar entorno virtual y reinstalar todo 
```
make reset
```

### Estructura del proyecto


```
📂 sgil-proveedores-service/       # Folder raiz
│
│── 📂 app/                    # Contains the main application files
│   │── 📂 models/             # Modelos SQLAlchemy
│   │── 📂 repositories/       # Lógica de acceso a BD
│   │── 📂 routers/            # Endpoints de la API
│   │── 📂 schemas/            # Esquemas Pydantic
│   │── 📂 services/           # Lógica de negocio
│   │── main.py                # Punto de entrada de FastAPI
│── 📂 k8s/                    # Configuración de kubernetes
│── 📂 Postman/                # Pruebas sobre el servicio
│── requirements.txt           # Dependencias del proyecto
│── .env                       # Variables de entorno (si usas PostgreSQL, MySQL, etc.)
│── alembic/                   # Migraciones de base de datos (opcional)
```


### Correr contenedor
 - ### Construir image de docker
    ```
        docker build --no-cache -t sgil-proveedores-service .
    ```

 - ### Correr conteedor
    ```
        docker run -it --name sgil-proveedores-service  sgil-proveedores-service
    ```

 - ### Ver las redes disponibles
    ```
    docker network ls
    ```

## Docker compose

### 🚀 Ejecutar el proyecto desde docker-compose
```
docker-compose up --build
```

### Eliminar volúmenes y contenedores antiguos 
```
docker system prune
```

### Eliminar los contennedores & volumenes
```
docker-compose down -v
```
