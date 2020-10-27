# Cloe Semestre i

## Estructura del proyecto
```
.
├── api                     # Back-end
│   ├── main.py             # Punto de entrada back-end
│   ├── .flaskenv           # Carga variables de entorno de flask
│   ├── .env                # IMPORTANTE: archivo no incluido ver mas adelante para instrucciones de configuracion
│   ├── requirements.txt    # Lista de dependencias del proyecto (actualizar con "pip freeze > requirements.txt")
│   ├── app                 # Codigo fuente back-end
|   |   ├── __init__.py     # Configuracion servidor Flask    
|   |   ├── config.py       # Archivo configuracion del proyecto   
|   |   ├── models.py       # Modelos en BDD    
|   |   ├── middleware      # carpetas con funciones middleware para los request  
|   |   ├── decorators      # carpetas con decoradores para funciones de todo el proyect
|   |   └── routes          # Carpeta de rutas
|   └── tests               # Carpeta con archivos de pruebas unitarias
|   
|
├── node_modules            # Librerias React
├── package.json            # Manejador proyecto npm
├── package-lock.json
├── public                  # Contenido "publico" del sitio (ej. multimedia)
│   ├── favicon.ico
│   ├── index.html
│   ├── logo192.png
│   ├── logo512.png
│   ├── manifest.json
│   └── robots.txt
├── README.md               # El archivo que se esta leyendo
└── src                     # Codigo fuente react
    ├── App.css
    ├── App.js
    ├── App.test.js
    ├── index.css
    ├── index.js
    ├── logo.svg
    ├── serviceWorker.js
    └── setupTests.js
```
## Python

```NOTA: Todo lo comentado aqui aplica solamente para el  path dentro de la carpeta api```

Se requiere instalar paquetes de `requirements.txt`

### Instalar ambiente de desarrollo

#### Linux/MacOs
Primero se requiere crear el ambiente:
```
$ python3 -m venv env
```
#### Windows
Comprueba que tu instalación de python tenga instalado pip. Para ello inserta el siguiente comando:
``` 
pip -h
```
Si aparece el manual de ayuda de pip, tienes instalada la libreria. En caso contrario, descarga e instala pip.

Con pip, instala la librería virtualenv:

``` 
pip install virtualenv
```

##### Crea el virtual environment
En el path (/semestrei-cloe/api) crea el virtual enviroment
virtualenv <nameOfYourEnv>

### Iniciar ambiente de desarrollo

### Variables del entorno (Environment Variables .env)

Para que el servidor corra de manera correcta es necesario la configuración de
multiples variables de entorno:

```
LD_LIBRARY_PATH
DATABASE_ORACLE_USER
DATABASE_ORACLE_PASSWORD
DATABASE_ORACLE_SERVICE
```

Estas variables pueden configurarse directo en servidor o en un archivo .env

#### archivo .env

Para configurar las variables directo en un archivo, se requiere crear 
el archivo `.env` dentro del directorio `./api/` (podemos observar como quedaria
en el arbol de directorios en la parte inicial de este README).

Una vez creado el archivo solo es necesario establecer las variables dentro del
mismo:
```
LD_LIBRARY_PATH={Directorio de intalacion de oracle instant client}
DATABASE_ORACLE_USER={usuario de la base de datos oracle}
DATABASE_ORACLE_PASSWORD={contraseña del usuario de la bdd}
DATABASE_ORACLE_SERVICE={nombre del servicio de oracle (se obtiene del archivo tnsnames.ora del wallet proporcionado por oracle, se encuentra como "service_name")}
# Mail configuration 
MAIL_SERVER={Servidor de correo electronico}
MAIL_PORT={puerto del servicio}
MAIL_USERNAME={usuario de email}
MAIL_PASSWORD={contraseña de email}
```
En el ejemplo anterior es necesario sustituir todo lo que esta entre llaves por 
el valor, ejemplo:
```
DATABASE_ORACLE_USER=admin
```

#### Linux/MacOs

``` $ source env/bin/activate```

#### Windows


``` <nameOfYourEnv>\Scripts\activate ```

### Configurar BDD Oracle

Para Flask poder trabajar con la base de datos de Oracle en la nube (OCI), es 
necesario instalar en el servidor el cliente 
[*Oracle Instant Client*](https://www.oracle.com/database/technologies/instant-client.html)
, debido a que este contiene las librerias requeridas para la conexión.

Despues de instalar este cliente, es necesario añadir todos los archivos del 
wallet de oracle en la carpeta /network/admin del cliente, quedando una 
estructura de archivos similar a esta:

```
instantclient/
├── network
│   └── admin
│       ├── cwallet.sso
│       ├── ewallet.p12
│       ├── keystore.jks
│       ├── ojdbc.properties
│       ├── README
│       ├── sqlnet.ora
│       ├── tnsnames.ora
│       └── truststore.jks
└── ... {archivos del instant client como libclntshcore.so.19.1, xstreams.jar}
```

#### Windows

Después de instalar el client se requiere agregar su directorio de instalación 
al `PATH` 

#### Linux & Mac

Dentro del directorio donde se instalo/descomprimio el cliente se requiere 
correr:

```
sudo sh -c "echo ./instantclient > /etc/ld.so.conf.d/oic.conf"
sudo ldconfig
```

Después de esto solo es necesario establecer la variable del ambiente 
`LD_LIBRARY_PATH ` a que apunte al directorio de instalación/descompresión. Ej.

```export LD_LIBRARY_PATH=/home/ubuntu/instantclient```

IMPORTANTE: Es necesario agregar la variable manualmente como se indica
 a demás de en el .env

### Intalar paquetes

Una vez activado el ambiente de desarrollo ejecutar:

``` $ pip install -r requirements.txt ```

**NOTA:** si este comando genera el error *Could not find a version that satisfies the requirement pkg-resources==0.0.0* ve al archivo requeriments.txt y borra la linea *pkg-resources==0.0.0*. Aparentemente es un bug al generar este archivo.

### Iniciar servidor (win / linux / macOS)

Dentro del ambiente ejecutar:

``` flask run ```   

### Ejecutar unit testing

Dentro del ambiente ejecutar:

``` python3 -m unittesting ```   

## React

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.