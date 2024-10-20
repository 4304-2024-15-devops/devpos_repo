# Proyecto DevOps 
## Integrantes
### PERSPICAPPS Grupo #13
- Wilson Andres Alarcon Cuchigay (w.alarconc@uniandes.edu.co)
- Jairo Ivan Bernal Acosta (ji.bernal27@uniandes.edu.co)
- Andrés Clavijo Rodríguez (a.clavijo1@uniandes.edu.co)
- Fabio Camilo Lopez Castellanos (fc.lopez@uniandes.edu.co)
## Documentación
https://documenter.getpostman.com/view/2331986/2sAXxS7r7R
## Ejecución
Require pippenv y python 3.12
Requiere las siguientes variables de entorno
```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
BEARER_TOKEN=
```
```bash
pipenv install
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Tests

```
pytests tests
pytest --cov=. -v -s --cov-fail-under=70
```
