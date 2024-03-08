# Información de la materia: ST0263 Topicos Especiales en Telematica
#
# Estudiante(s): Daniel Ricardo Palacios Diego, drpalaciod@eafit.edu.co
#
# Profesor: Juan Carlos Montoya Mendoza, [jcmontoy@eafit.edu.co]
#
# PeerIT
#
# 1. Breve descripción de la actividad
#
PeerIT es un sistema P2P para la compartición de archivos de forma descentralizada y no estructurada. La interacción con el sistema es a través de consola. El usuario final deberá iniciar el servicio que luego de la configuración de este correrá en background. El usuario interactuará con el sistema a través de la línea de comandos con el programa (peerctl).

## 1.1. Aspectos cumplidos o desarrollados de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- Inicialización del servicio: El sistema busca un archivo llamado peerConf.json en el directorio actual. Si no existe![image](https://github.com/DanielPalacios05/DanielPalacios05-st026/assets/82727314/23815c88-228a-4ff7-9d58-d5dadcbb0440), notifica al usuario para que lo cree con la notación mencionada.
- Mostrar estado: El sistema muestra el estado del servicio del Peer, la cantidad de peers en la lista de contactos y los archivos que está compartiendo.

- Descarga de archivos: El sistema permite descargar archivos de la red PeerIT por su nombre y por id.
- Subida de archivos: El sistema permite al usuario ingresar el directorio del archivo que quiere subir a la red para que otros peers lo descarguen.
- Conexión/Desconexión de Peers: El sistema permite conectar y desconectar peers a través de su url, actualizando la lista de contactos.

## 1.2. Aspectos NO cumplidos o desarrollados de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
- Búsqueda de archivos: El sistema permite buscar un archivo de la red PeerIT por nombre y por formato.
- Desconexión de Peers: desconectar peers a través de su url, actualizando la lista de contactos.
- Descarga de peers: El sistema permite descargar un archivo de el peer especificadp
- Peer fetching: El sistema permite buscar en la red peerIT los archivos que tienen los peers a traves de flooding.
  

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

El sistema fue diseñado utilizando el modelo C4. Que permite modelar los componentes software y los contenedores que corren estos componentes.

## Diagrama de contexto

![image](https://github.com/DanielPalacios05/DanielPalacios05-st026/assets/82727314/a875b59d-4f41-43d2-9279-7e89bfda476c)

## Diagrama de contenedores

![PeerITArchitecture drawio](https://github.com/DanielPalacios05/DanielPalacios05-st026/assets/82727314/d13ae712-4940-4d30-a104-26e53092f044)

## Fetching
El fetching consiste en a ultilizar un mecanismo de flooding para descubrir la red PeerIT ultilizando los peers a los cuales el peer que inicia el fetching esta directamente conectado.
Cuando un peer recibe un mensaje en la cola este la procesa y envia un mensaje con los archivos que tiene y su ip asociada a el peer que lo origino.

Cuando un peer genera el proceso de fetching, se genera un uuid para cada fetch que se inicie, con el objetivo evitar el reenvio de mensajes si existen loops en la topología debido a la naturaleza no estructurada
de esta.

El fetching tiene un ttl asociado cuando termina el peer empieza a almacenar los peers y los archivos que permiten descargar

Existe un componente dentro de el microservicio de messaging llamado TimedSet que implementa un conjunto cuyos elementos tienen un tiempo de vida especifico que por defecto es 30 segundos.
Cuando un peer realiza un fetch se genera un uuid para el proceso
Cada vez que el peer reciba un mensaje de fetch, revisa que el uuid de el fetch no esta en el TimedSet, si esta no hace broadcast de el fetch, sino, descarta el mensaje.


En los siguientes diagramas se evidencia como se resuelve este proceso en el sistema.

# Diagrama dinamico de iniciar un fetch

![PeerITArchitecture-Page-3 drawio](https://github.com/DanielPalacios05/DanielPalacios05-st026/assets/82727314/6a889f2a-8dc5-4172-955b-a9dc6f8e162f)

# Diagrama dinamico de recibir un fetch request

![PeerITArchitecture-Page-5 drawio](https://github.com/DanielPalacios05/DanielPalacios05-st026/assets/82727314/b0a6e715-8fbf-4678-b5fc-f6dbecd9da13)

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerías, paquetes, etc, con sus números de versiones.

Estructura de el projecto:

PeerIT
├── peerctl
│   ├── Makefile
│   ├── core
│   │   ├── command.go
│   │   ├── controller.go
│   │   ├── fetchCommand.go
│   │   ├── initCommand.go
│   │   ├── jsonParsing.go
│   │   ├── listCommand.go
│   │   ├── peerClient.go
│   │   ├── stopCommand.go
│   │   └── syncCommand.go
│   ├── go.mod
│   ├── go.sum
│   ├── peerConfig.json
│   ├── peerctl
│   ├── peerctl.go
│   
└── server
    ├── docker-compose.yml
    ├── files
    │   ├── Dockerfile
    │   ├── files.py
    │   └── requirements.txt
    ├── messaging
    │   ├── Dockerfile
    │   ├── linkedPeer.py
    │   ├── linkedPeers.py
    │   ├── messaging.py
    │   ├── queue_server.py
    │   ├── requirements.txt
    │   └── rpc_server.py
    ├── peerit-api-client
    │   ├── Dockerfile
    │   ├── app
    │   │   ├── __init__.py
    │   │   │   └── __init__.cpython-38.pyc
    │   │   └── main.py
    │   └── requirements.txt
    ├── peers
    │   ├── Dockerfile
    │   │   ├── peers_pb2.cpython-311.pyc
    │   │   └── peers_pb2_grpc.cpython-311.pyc
    │   ├── peers.py
    │   └── requirements.txt
    └── protobufs
        ├── files.proto
        ├── messaging.proto
        └── peers.proto

## Peerctl

Programado en Go 1.21

1. encoding/json,bytes para procesamiento de mensajes en json
2. strconv para convertir strings a diferentes tipos
3. os/exec,io, path/filepath para ejecutar comandos e interactuar con el filesystem de el host
4. errors,logs, fmt para imprimir en consola

## Microservicios de el servidor

1. Pika para interactuar con rabbitMQ
2. json para interactuar con json
3. time para implementar el ttl de timedSet
4. grpc,grpcio,grpcio-tools para implementar rpc's
5. sqlite3 para administrar las bases de datos
6. Flask para implemenar servidor API REST

## Descripción y cómo se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
  El servidor de el peer esta completamente contenerizado, basta con clonar el proyecto y modificar el archivo de configuracion peerConfig.json
  Con los siguientes parametros

  {
    "listening_ip": #IP de el cliente de el peer
    "listening_port": #Puerto de el cliente de el perr
    "shared_dir": #Directorio donde se guardan los archivos 
    "download_dir": #Directorio a donde se van los archivos descargados
    "server_path" : "#Directorio donde se encuentra el docker-compose de el servidor"
    "primary_peer_url": #IP de el primer peer con el que el peer se conecta,
    "secondary_peer_url": #IP de el segundo peer con el que el peer se conecta
  }
  

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerías, paquetes, etc, con sus números de versiones.


## Cómo se lanza el servidor.

Para lanzar el servido de el peer se debe llamar docker compose build y docker compose up dentro de el directorio server.
Esto automaticamente levanta todos los microservicios y permite a peerctl conectarse con el peer con la ip y puerto que escucha
el API client.

## Una mini guía de cómo un usuario utilizaría el software o la aplicación
Para ultilizar PeerIT debe cumplir con lo siguiente

1. Instalar Docker, Git, Docker-compose y G2olang 1.21.
2. Clonar el repositorio .[https://github.com/st0263eafit/st0263-241/blob/main/README-template.md]
3. Entrar a la carpeta peerctl y llamar make para compilar el cliente
4. Entrar a la carpeta server y llamar docker-compose build y docker-compose up para levantar el servicio

A su disposicion el cliente tiene los siguientes comandos :

peerctl init: Inicializar el servicio PeerIT y crear la configuración necesaria.
peerctl start: Iniciar el servicio PeerIT en segundo plano.
peerctl stop: Detener el servicio PeerIT.
peerctl status: Ver el estado actual del servicio PeerIT (conectado/desconectado, peers conectados, etc.).
Comandos de búsqueda:
peerctl search <nombre_archivo>: Buscar archivos por nombre.
peerctl search -t <tipo_archivo>: Buscar archivos por tipo (música, videos, documentos, etc.) 
peerctl fetch : Inicia la comunicación entre los peers para hallar los archivos 

Comandos de descarga:

peerctl download  <nombre_archivo>: Descargar un archivo por su nombre.
peerctl download -i <id archivo> … <id archivo>
peerctl download -p <peer_id>: Descargar un archivo desde un peer específico.
Comandos de subida:

Peerctl sync files: Actualiza la lista de archivos que se van a compartir

Comandos de gestión de peers:

peerctl connect <PEER_URL>: Conectarse a un peer específico.
peerctl disconnect <PEER_URL>: Desconectarse de un peer específico.
peerctl list peers: Mostrar una lista de los peers conectados.
La búsqueda se realiza de forma local con los resultados de la búsqueda hecha con peerctl list files: Muestra los archivos


# Referencias:
- [https://www.rabbitmq.com/]
- [https://grpc.io/]-
- https://realpython.com/python-microservices-grpc/
- Distributed systems by Maarten van Steen and Andre S. Tanenbaum

Video de youtube: 
