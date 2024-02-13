# Antotador personal

> Concepto: seguimiento peso corporal y otras mediciones,
> así como otros eventos que me gusta registar como pinchaduras
> de las ruedas de la bicicleta.

## Desafíos
- Conseguir un ejecutable `.apk` con **buildozer**. Lograr que funcione efectivamente en android otro nivel de reto.
- ~~Lograr simultaneamente una conexión funcional con el sevicio de *Aiven* con la base de dato posgreSQL.~~ 
    - **NOTA:** debido a los inconvenientes que trajo el módulo `psycopg2` se terminó recurriendo [Firebase](https://firebase.google.com/) como alternativa.
    - Usar módulo `pyrebase` para gestionar base de datos. (la versión que es compatible con resto de ambiente se instala con `pip install pyrebase4`)

### Firebase
Archivo *db.ini* con credenciales. Estructura:

    [pyrebase]
    apikey = 
    authdomain = 
    databaseurl = 
    projectid = 
    storagebucket = 
    messagingsenderid = 
    appid = 
    measurementid = 

    [user]
    mail = 
    pwd = 

Sección `[pyrebase]` almacena credenciales de proyecto generado en la [consola](https://firebase.google.com/?gad_source=1&gclid=Cj0KCQiAw6yuBhDrARIsACf94RXf0kYtLQi1VXGKcQjdRAERym439QaPZuP69PPp_h0v1sRq9AzOVZMaAt0REALw_wcB&gclsrc=aw.ds&hl=es-419) de **Firebase**


