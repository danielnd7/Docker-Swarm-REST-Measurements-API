## Contenedores con Docker: Pasos de la Práctica

### Parte 1: Contenedor Docker y Stack con Grafana

1.  **Desarrollo de la API REST:**
    * Implementar la API REST (usando **Flask** o **FastAPI**).
    * Crear el *endpoint* `/nuevo?dato=valor` para almacenar la medición en **RedisTimeSeries**.
    * Crear el *endpoint* `/listar` para mostrar las mediciones de **Redis** y el *hostname* del contenedor.
    * Asegurar que el código de la API se conecte a Redis utilizando una variable de entorno para el host (`REDIS_HOST`).

2.  **Prueba Local de Redis:**
    * Lanzar una instancia local de **Redis Stack** con `docker run -d --name some-redis...`.
    * Probar la API localmente (sin contenedor) conectándose a la instancia de Redis.

3.  **Contenerización de la API:**
    * Crear un **Dockerfile** para la aplicación API, incluyendo las dependencias y el código.
    * Construir la imagen Docker de tu API (ej. `micontenedor`).
    * Probar la imagen Docker de la API conectándola a la instancia local de Redis (usando `host.docker.internal` como host de Redis y la opción `-e REDIS_HOST=host.docker.internal`).

4.  **Creación del Stack Docker Swarm:**
    * Crear el fichero **`docker-compose.yml`** para Docker Swarm (usando la sintaxis `deploy: mode: replicated`, etc.).
    * Incluir el servicio de tu API (con **5 réplicas**) usando la imagen subida a Docker Hub.
    * Incluir el servicio de **RedisTimeSeries** (ej. `redis/redis-stack`) bajo el nombre de servicio `redis`.
    * Configurar tu servicio API para usar el nombre de servicio `redis` como host a través de una variable de entorno (ej. `REDIS_HOST: redis`).
    * Incluir el servicio de **Grafana** (con el *plugin* `redis-datasource` y montaje de volumen para datos).
    * Definir la red (`webnet`) y los volúmenes (`grafana_data`).

5.  **Despliegue y Monitorización:**
    * Inicializar Docker Swarm (`docker swarm init`).
    * Desplegar el stack Swarm con el fichero `docker-compose.yml` (`docker stack deploy...`).
    * Verificar que las 5 réplicas de tu API estén en ejecución.
    * Acceder a Grafana (puerto 3000) y configurar la fuente de datos Redis.
    * Crear un *dashboard* en Grafana para visualizar las mediciones recibidas en Redis.

---

### Parte 2: Detección de Anomalía

1.  **Preparación de Artefactos:**
    * Asegurar que el modelo de detección de anomalías (`modelo.keras`) y el escalador (`scaler.pkl`) estén guardados.
    * Asegurar que el umbral (*threshold*) utilizado esté guardado en un fichero (si aplica).

2.  **Actualización de la API REST:**
    * Modificar la API para cargar el modelo, el escalador y el umbral al iniciar.
    * Crear el *endpoint* `/detectar?dato=valor`.
    * En `/detectar`, recuperar el valor, almacenarlo en Redis, recuperar las muestras previas necesarias (ventana).
    * Realizar la detección de anomalía con el modelo cargado.
    * Retornar la respuesta en formato **JSON** o texto plano, incluyendo la ventana considerada y si hay anomalía.

3.  **Actualización del Contenedor:**
    * Actualizar el **Dockerfile** para incluir el modelo, el escalador y el umbral, o usar un volumen para acceder a ellos.
    * Construir y subir la nueva versión de la imagen Docker de tu API a Docker Hub.

4.  **Actualización del Stack:**
    * Actualizar el fichero `docker-compose.yml` para usar la nueva imagen de tu API.
    * Actualizar el stack Swarm (`docker stack deploy...`).

---

### Parte 3: Despliegue con Alta Disponibilidad (Opción A)

1.  **Ajuste de Conexión de la API:**
    * Modificar el código de conexión de tu API para usar la librería `redis.sentinel` o `redis-py-cluster` según la opción.
    * Ajustar el código para leer los *hosts* y puertos de Sentinel o Cluster desde variables de entorno.

2.  **Despliegue con Redis Sentinel:**
    * Obtener el fichero `.yml` de Redis con Sentinel.
    * Integrar tu contenedor API en el fichero `.yml` de Sentinel.
    * Lanzar el *stack* de **Redis Sentinel** y tu API con `docker compose -f... up`.
    * Realizar pruebas de fallo (parar el maestro o un Sentinel) y capturar el proceso de promoción a maestro con `redis-cli INFO SENTINEL`.

3.  **Despliegue con Redis Cluster:**
    * Obtener el fichero `.yml` de Redis Cluster.
    * Integrar tu contenedor API en el fichero `.yml` de Cluster.
    * Lanzar el *stack* de **Redis Cluster** y tu API con `docker compose -f... up`.
    * Realizar pruebas de fallo (parar un nodo maestro) y capturar el proceso de promoción a maestro con `redis-cli -c CLUSTER INFO`.

---

### Pasos de Entrega Final

1.  **Documentación:**
    * Escribir la **Memoria en PDF** (incluyendo código, capturas y descripción del funcionamiento).

2.  **Código y Ficheros:**
    * Recopilar el **código fuente** y todos los ficheros **`.yml`** de Docker Swarm/Compose.

3.  **Docker Hub:**
    * Subir la imagen Docker de tu API a **hub.docker.com** para la arquitectura `linux/amd64`.

4.  **Instrucciones:**
    * Crear las **Instrucciones** para la utilización del sistema.

5.  **Opcional:**
    * Grabar un **vídeo** complementario.
    * Desplegar opcionalmente en **Google Cloud**.
