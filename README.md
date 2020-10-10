# Cloe Semestre i

## Estructura del proyecto
```
.
├── api                     # Back-end
│   ├── main.py             # Punto de entrada back-end
│   ├── .flaskenv           # Carga variables de entorno de flask
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

```NOTA: Todo lo comentado aqui es dentro de la carpeta api```

Se requiere instalar paquetes de `requirements.txt`

### Instalar ambiente de desarrollo

Primero se requiere crear el ambiente:
```
$ python3 -m venv env
```

### Iniciar ambiente de desarrollo

Una vez creado se inicia en `Linux` (supongo que mac es igual, googlear como se hace en windows) con:

``` $ source env/bin/activate```

### Intalar paquetes

Una vez iniciado el ambiente de desarrollo ejecutar:

``` $ pip install -r requirements.txt ```

### Iniciar servidor

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